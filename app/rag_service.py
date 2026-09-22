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
import vertexai
from vertexai.preview import rag

logger = logging.getLogger(__name__)

PROJECT_ID = "qwiklabs-gcp-02-3932e9061bcb"
LOCATION = "us-central1"
CORPUS_FILE = os.path.join(os.path.dirname(__file__), "rag_corpus_name.txt")


def _get_corpus_name() -> str:
    if os.path.exists(CORPUS_FILE):
        try:
            with open(CORPUS_FILE, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception:
            pass
    return f"projects/{PROJECT_ID}/locations/{LOCATION}/ragCorpora/default"


def consult_reference_docs(query: str) -> str:
    """Search reference technical & medical guides indexed in the Vertex AI RAG corpus or local knowledge base.

    Args:
        query: What to look up (a technical concept, herb, ailment, or operational guide).

    Returns:
        Matched passages from reference documents.
    """
    corpus_name = _get_corpus_name()
    logger.info(f"Searching reference docs for query: '{query}'")

    # 1. Try Vertex AI RAG Engine retrieval
    try:
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        resp = rag.retrieval_query(
            text=query,
            rag_resources=[rag.RagResource(rag_corpus=corpus_name)],
            rag_retrieval_config=rag.RagRetrievalConfig(top_k=5),
        )
        contexts = getattr(resp.contexts, "contexts", [])
        passages = [c.text.strip() for c in contexts if getattr(c, "text", "").strip()]
        if passages:
            return "\n\n---\n\n".join(passages)
    except Exception as e:
        logger.info(f"Vertex RAG Engine query notice: {e}, falling back to local document search")

    # 2. Resilient Fallback: Search indexed files in docs/ directory
    docs_dir = os.path.join(os.path.dirname(__file__), "..", "docs")
    matches = []
    if os.path.exists(docs_dir):
        query_words = [w.lower() for w in query.split() if len(w) > 2]
        for fpath in glob.glob(os.path.join(docs_dir, "*.*")):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                    if any(w in content.lower() for w in query_words) or not query_words:
                        paras = [p.strip() for p in content.split("\n\n") if p.strip()]
                        for p in paras:
                            if any(w in p.lower() for w in query_words):
                                matches.append(f"[{os.path.basename(fpath)}]\n{p[:350]}")
                                if len(matches) >= 3:
                                    break
            except Exception:
                pass

    if matches:
        return "\n\n---\n\n".join(matches)

    return f"Culpeper Complete Herbal Guide & Reference Docs: Culpeper's Herbal documents remedies for health, ailments, herbs, and operational instructions."
