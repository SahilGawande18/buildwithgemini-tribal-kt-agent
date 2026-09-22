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

import random
import logging

logger = logging.getLogger(__name__)

# Comprehensive pool of real-world architectural, gotcha, and ADR questions
QUESTION_POOL = [
    {
        "topic": "Data Consistency & Persistence",
        "question": "Why must the Firestore client in this platform be initialized with an explicit alphanumeric string `project='qwiklabs-gcp-02-3932e9061bcb'`?",
        "options": [
            "A) `google.auth.default()` is deprecated in Python 3.11.",
            "B) On Agent Engine, `google.auth.default()` returns numeric project number instead of project ID, breaking Firestore authentication. ✅",
            "C) Firestore requires project IDs to be written in uppercase.",
            "D) To prevent Cloud Run from scaling down instances."
        ]
    },
    {
        "topic": "Memory & Cross-Session Context",
        "question": "How does this platform persist engineer role preferences and team facts across different browser sessions?",
        "options": [
            "A) By storing unencrypted cookies in local storage only.",
            "B) By writing durable user facts into **Vertex AI Memory Bank** via `PreloadMemoryTool` and callbacks. ✅",
            "C) By storing session state in a temporary Redis cache.",
            "D) By creating a new Git branch for every session."
        ]
    },
    {
        "topic": "Microservice Communication",
        "question": "What protocol is used by the Cloud Run frontend proxy to communicate with the Agent Engine runtime?",
        "options": [
            "A) Raw WebSocket connections over port 80.",
            "B) Agent-to-Agent (A2A) JSON-RPC protocol over HTTPS. ✅",
            "C) Plain gRPC without authentication headers.",
            "D) Local file system IPC sockets."
        ]
    },
    {
        "topic": "Security & Secret Management",
        "question": "What is the recommended approach for handling API keys in this production architecture according to our code auditor?",
        "options": [
            "A) Hardcode them in `app/agent.py` as string literals.",
            "B) Store them in GCP Secret Manager and retrieve them via Environment Variables. ✅",
            "C) Write them into public `index.html` scripts.",
            "D) Base64 encode them inside `pyproject.toml`."
        ]
    },
    {
        "topic": "Cloud Storage Assets",
        "question": "How are generated architecture diagrams and Confluence wiki pages made accessible to custom web frontends?",
        "options": [
            "A) Sent as raw base64 strings in every response.",
            "B) Uploaded to a public Cloud Storage bucket with public HTTPS URLs. ✅",
            "C) Saved only on local workstation disk.",
            "D) Emailed to team leads as ZIP attachments."
        ]
    },
    {
        "topic": "Grounding & RAG Retrieval",
        "question": "Why is Vertex AI RAG Engine exposed as a standalone function tool (`consult_reference_docs`) in this ADK agent?",
        "options": [
            "A) To prevent tool schema conflicts with A2UI cards and other custom function tools. ✅",
            "B) Because RAG Engine only supports CLI invocations.",
            "C) To force all queries to run synchronously.",
            "D) Because Gemini 2.5 Flash does not support search."
        ]
    },
    {
        "topic": "A2UI Rich Surfaces",
        "question": "What schema manager handles structured card, row, column, and image rendering for the custom chat UI?",
        "options": [
            "A) `A2uiSchemaManager` with version `0.8` protocol. ✅",
            "B) React Fiber v18.",
            "C) Web Components Shadow DOM v2.",
            "D) TailwindCSS Utility Engine."
        ]
    },
    {
        "topic": "Observability & Tracing",
        "question": "Which environment variable enables telemetry and tracing on Agent Runtime deployments?",
        "options": [
            "A) `GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY=true`. ✅",
            "B) `ENABLE_DEBUG_PRINTS=1`.",
            "C) `TRACE_LEVEL=MAX`.",
            "D) `NO_LOGGING=false`."
        ]
    }
]


def generate_onboarding_quiz(
    project_name: str = "NovaSmart Platform",
    num_questions: int = 3,
    difficulty: str = "medium"
) -> str:
    """Generates a randomized real-time technical onboarding quiz to test an engineer's understanding of a project's architecture, ADRs, and gotchas.

    Args:
        project_name: Name of the project (e.g., 'Billing Service', 'Payment Gateway', 'NovaSmart Platform').
        num_questions: Number of quiz questions to ask (e.g. 3, 4, or 5).
        difficulty: Quiz difficulty level ('easy', 'medium', 'advanced').

    Returns:
        Interactive quiz assessment with randomized architectural questions, multiple-choice options, and score key.
    """
    logger.info(f"Generating dynamic onboarding quiz for project '{project_name}' ({num_questions} questions, {difficulty})")

    # Ensure num_questions is between 1 and pool size
    num_q = max(1, min(int(num_questions), len(QUESTION_POOL)))

    # Select randomized sample of questions from the pool
    selected_questions = random.sample(QUESTION_POOL, num_q)

    quiz_lines = [
        f"📝 **Real-Time Engineer Onboarding Quiz: [{project_name}]**",
        f"📌 **Total Questions**: `{num_q}` | **Difficulty**: `{difficulty.upper()}`",
        "---"
    ]

    for idx, q in enumerate(selected_questions, 1):
        quiz_lines.append(f"### Question {idx}: {q['topic']}")
        quiz_lines.append(f"{q['question']}")
        for opt in q['options']:
            quiz_lines.append(f"- {opt}")
        quiz_lines.append("")

    quiz_lines.append("---")
    quiz_lines.append("💡 **Score Evaluation Key**:")
    quiz_lines.append(f"- **{num_q}/{num_q} Correct**: 🏆 **Senior Architecture Mastery** — Ready to commit code to production!")
    quiz_lines.append(f"- **{num_q - 1}/{num_q} Correct**: 🟡 **Onboarding In Progress** — Review team ADRs and gotcha docs.")
    quiz_lines.append(f"- **<{num_q - 1} Correct**: 🔴 **KT Required** — Consult `consult_reference_docs` or ask the agent for onboarding guidance.")

    return "\n".join(quiz_lines)
