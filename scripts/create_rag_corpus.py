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
import vertexai
from vertexai.preview import rag
from vertexai.preview.rag.utils import resources as rr

PROJECT_ID = "qwiklabs-gcp-02-3932e9061bcb"
LOCATION = "us-central1"
GCS_PATH = "gs://qwiklabs-gcp-02-3932e9061bcb-tribal-media/rag/reference_medical_guide.txt"

PARSING_PROMPT = (
    "Extract the individual useful facts, herbs, remedies, and instructions described in this text. "
    "Omit metadata, license text, boilerplate, and page headers. "
    "Output clean, self-contained prose."
)

def build_corpus():
    print(f"Initializing Vertex AI RAG Engine for project: {PROJECT_ID}, location: {LOCATION}...")
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    # 1. Switch region to serverless mode
    cfg = f"projects/{PROJECT_ID}/locations/{LOCATION}/ragEngineConfig"
    try:
        rag.update_rag_engine_config(rag_engine_config=rag.RagEngineConfig(
            name=cfg,
            rag_managed_db_config=rag.RagManagedDbConfig(mode=rr.Serverless()),
        ))
        print("Updated ragEngineConfig to Serverless mode.")
    except Exception as e:
        print(f"Notice during update_rag_engine_config: {e}")

    # 2. Create corpus
    print("Creating RAG corpus...")
    corpus = rag.create_corpus(
        display_name="tribal-kt-reference-corpus",
        embedding_model_config=rag.EmbeddingModelConfig(
            publisher_model="publishers/google/models/text-embedding-005"
        ),
    )
    print(f"\n✅ Created RAG Corpus Name: {corpus.name}")

    # Save corpus name to config file
    corpus_file = os.path.join(os.path.dirname(__file__), "..", "app", "rag_corpus_name.txt")
    with open(corpus_file, "w", encoding="utf-8") as f:
        f.write(corpus.name)
    print(f"Saved corpus name to {corpus_file}")

    # 3. Import + parse + chunk + embed
    print(f"Importing files from {GCS_PATH}...")
    try:
        resp = rag.import_files(
            corpus_name=corpus.name,
            paths=[GCS_PATH],
            transformation_config=rag.TransformationConfig(
                chunking_config=rag.ChunkingConfig(chunk_size=512, chunk_overlap=100)
            ),
            llm_parser=rag.LlmParserConfig(
                model_name="gemini-flash-latest",
                custom_parsing_prompt=PARSING_PROMPT
            ),
        )
        print(f"✅ Successfully imported {getattr(resp, 'imported_rag_files_count', 1)} files into RAG corpus!")
    except Exception as e:
        print(f"Notice during import_files: {e}")

if __name__ == "__main__":
    build_corpus()
