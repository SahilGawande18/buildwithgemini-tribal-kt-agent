# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import glob
import logging
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai import types

from a2ui.schema.manager import A2uiSchemaManager
from a2ui.basic_catalog.provider import BasicCatalog
from app.a2ui_utils import a2ui_callback

from app.knowledge_graph import query_graph, add_entity
from app.firestore_service import (
    search_firestore_knowledge,
    save_firestore_knowledge_item,
)
from app.external_api_tools import (
    get_github_repo_details,
    get_team_location_weather_and_time,
)
from app.rag_service import consult_reference_docs
from app.image_gen_tool import generate_architecture_diagram
from app.doc_generator_tool import generate_synthetic_confluence_doc
from app.code_auditor_tool import audit_codebase_compliance
from app.quiz_generator_tool import generate_onboarding_quiz

logger = logging.getLogger(__name__)


# WRITE: Callback executed at the end of each turn to send durable facts to Vertex AI Memory Bank
async def generate_memories_callback(callback_context: CallbackContext):
    """Write durable user facts, preferences, and onboarding role details to Memory Bank."""
    await callback_context.add_session_to_memory()
    return None


def query_knowledge_graph(query: str) -> dict:
    """Query the Tribal Knowledge Graph for microservice components, maintainers, relationships, and Architecture Decision Records (ADRs).

    Args:
        query: The search term or component name to look up (e.g. 'Authentication Service', 'Redis', 'Memcached', 'PostgreSQL', 'Alice').

    Returns:
        A dictionary containing matching entities, component relationships, maintainer contacts, and architecture decisions.
    """
    logger.info(f"Querying Knowledge Graph for: {query}")
    return query_graph(query)


def ingest_doc(file_path: str) -> str:
    """Read and ingest a documentation file or Confluence page into the Tribal Knowledge Graph.

    Args:
        file_path: Absolute or relative path to the documentation file to ingest.

    Returns:
        Status message summarizing the ingestion.
    """
    if not os.path.exists(file_path):
        docs_dir = os.path.join(os.path.dirname(__file__), "..", "docs")
        candidate = os.path.join(docs_dir, os.path.basename(file_path))
        if os.path.exists(candidate):
            file_path = candidate
        else:
            return f"File not found: {file_path}. Available docs: {os.listdir(docs_dir) if os.path.exists(docs_dir) else []}"

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        doc_name = os.path.basename(file_path)
        add_entity(name=f"Doc: {doc_name}", category="Documentation", owner="Team Docs", description=content[:200])
        return f"Successfully ingested {doc_name} into Knowledge Graph ({len(content)} characters)."
    except Exception as e:
        return f"Error reading document {file_path}: {str(e)}"


def search_repo_history(query: str) -> str:
    """Search repository commits, release notes, and operational gotchas.

    Args:
        query: Search term for repository history or gotchas.

    Returns:
        Summary of relevant commit history or operational gotchas.
    """
    docs_dir = os.path.join(os.path.dirname(__file__), "..", "docs")
    results = []
    if os.path.exists(docs_dir):
        for fpath in glob.glob(os.path.join(docs_dir, "*.md")):
            with open(fpath, "r", encoding="utf-8") as f:
                txt = f.read()
                if query.lower() in txt.lower():
                    results.append(f"Match in {os.path.basename(fpath)}:\n{txt[:400]}...")

    if results:
        return "\n\n".join(results)
    return f"No commit notes or documentation matches found for query: '{query}'."


# 1. Build A2UI System Prompt (v0.8)
schema_manager = A2uiSchemaManager(
    version="0.8",
    catalogs=[BasicCatalog.get_config("0.8")],
)

a2ui_instruction = schema_manager.generate_system_prompt(
    role_description="You are the Tribal Knowledge & KT (Knowledge Transfer) Assistant for the software engineering team.",
    workflow_description="Help engineers, DevOps, and new team members onboard quickly, find component maintainers, understand architecture decision records (ADRs), search Firestore & RAG reference docs, and generate architecture diagrams. Return structured A2UI cards or plain text when appropriate.",
    ui_description=(
        "Keep every surface tiny and flat: ONE Card > ONE Column > a few Text rows. "
        "Never nest a Card inside a Card. "
        "Use ONLY these components: Card, Column, Row, Text, and Image. Do not use "
        "Table or Heading (unsupported), or Buttons, actions, or forms. "
        "You may include one Image component when you have a public https URL for the image (such as the diagram_url returned by generate_architecture_diagram). "
        "Set the Image url to that exact https link. Never point an Image at a bare filename. "
        "No markdown in text; use usageHint ('h1', 'h2', 'body') for headings. "
        "Output ONLY the raw A2UI JSON array when returning UI. "
        "SPEED GUIDANCE: Select the single most relevant tool directly and answer immediately without chaining unnecessary tool calls."
    ),
    include_schema=True,
    include_examples=True,
)


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-flash-latest",
        code_execution=True,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=a2ui_instruction,
    tools=[
        PreloadMemoryTool(),
        query_knowledge_graph,
        ingest_doc,
        search_repo_history,
        search_firestore_knowledge,
        save_firestore_knowledge_item,
        get_github_repo_details,
        get_team_location_weather_and_time,
        consult_reference_docs,
        generate_architecture_diagram,
        generate_synthetic_confluence_doc,
        audit_codebase_compliance,
        generate_onboarding_quiz,
    ],
    after_model_callback=a2ui_callback,
    after_agent_callback=generate_memories_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)
