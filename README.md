# Tribal Knowledge & KT Agent (`tribal-kt-agent`)

A production-ready **AI Knowledge Transfer & Architecture Agent** built with Google's **Agent Development Kit (ADK)** and deployed on **Google Cloud Agent Platform** and **Cloud Run**.

Designed for software engineering teams, Head of AI Platform, DevOps, and onboarding engineers to eliminate tribal knowledge silos, query Architecture Decision Records (ADRs), search Firestore & RAG reference documentation, inspect component maintainers, and generate architecture diagrams.

---

## 🌟 Key Features & Capabilities

- 🧠 **Cross-Session Memory Bank**: Powered by **Vertex AI Memory Bank** (`VertexAiMemoryBankService`), preserving engineer role preferences, team context, and historical interactions across sessions.
- 🗄️ **Firestore Backend**: Real-time document storage (`tribal_knowledge_items`) for ADRs, component ownership records, and operational gotchas with hardcoded alphanumeric GCP project ID resolution.
- 🗂️ **Cloud Storage Integration**: Public GCS bucket (`qwiklabs-gcp-02-3932e9061bcb-tribal-media`) hosting architecture diagrams and generated visuals with public HTTPS URLs.
- 📚 **RAG Engine Grounding**: Serverless **Vertex AI RAG Engine** indexing technical manuals and reference documentation for semantic retrieval without grounding tool conflicts.
- 🎨 **Generative Architecture Visuals**: Image generation via Gemini/Imagen producing component architecture diagrams, saving local artifacts, and uploading public PNG graphics.
- 🌐 **Live External APIs**: Integrated GitHub REST API (`get_github_repo_details`) and Open-Meteo Weather API (`get_team_location_weather_and_time`) for repository stats and team location queries.
- 💻 **Code Execution Sandbox**: Python code executor enabled on the underlying Gemini model for calculations and code analysis.
- 🖼️ **A2UI Rich Surface Cards**: Structured A2UI (v0.8) cards, tables, and image rendering via `a2ui_utils.py` and `A2uiSchemaManager`.
- 🚀 **Custom Frontend & Proxy**: FastAPI proxy service communicating over A2A protocol deployed to **Cloud Run**, serving a responsive Chat UI.

---

## 🏗️ Architecture Overview

```
                          ┌─────────────────────────────┐
                          │   Browser (Custom UI)       │
                          └──────────────┬──────────────┘
                                         │ HTTPS
                                         ▼
                          ┌─────────────────────────────┐
                          │  Cloud Run Frontend Proxy   │
                          └──────────────┬──────────────┘
                                         │ A2A Protocol
                                         ▼
                          ┌─────────────────────────────┐
                          │  Agent Runtime (Agent Engine│
                          └──────────────┬──────────────┘
                                         │
        ┌───────────────────┬────────────┴───────┬───────────────────┐
        ▼                   ▼                    ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌─────────────────┐   ┌───────────────┐
│ Memory Bank   │   │ Cloud Storage │   │ Firestore DB    │   │ RAG Engine    │
└───────────────┘   └───────────────┘   └─────────────────┘   └───────────────┘
```

---

## 🛠️ Local Setup & Running Instructions

### 1. Prerequisites
Ensure you have Python 3.11+, `uv`, and `gcloud` authenticated:
```bash
gcloud config set project qwiklabs-gcp-02-3932e9061bcb
```

### 2. Install Dependencies
```bash
uv sync
```

### 3. Run Agent Locally with ADK Dev UI
```bash
uv run adk web --port 8080 --allow_origins "*" --reload_agents
```

### 4. Run Custom Frontend Proxy Locally
```bash
cd frontend
pip install -r requirements.txt
export AGENT_ENGINE_RESOURCE_NAME="projects/898315975450/locations/us-central1/reasoningEngines/8017484308358889472"
export AGENT_DIRECTORY="app"
python main.py
```
Open `http://localhost:8080` in your browser.

---

## 🚢 Deployment

### Deploy Agent to Agent Runtime
```bash
agents-cli deploy --project qwiklabs-gcp-02-3932e9061bcb --region us-central1 --no-confirm-project
```

### Deploy Frontend to Cloud Run
```bash
gcloud run deploy tribal-kt-frontend \
  --source frontend \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="AGENT_ENGINE_RESOURCE_NAME=projects/898315975450/locations/us-central1/reasoningEngines/8017484308358889472,AGENT_DIRECTORY=app" \
  --project=qwiklabs-gcp-02-3932e9061bcb \
  --quiet
```

---

## 🧪 Sample Prompts to Try

1. **Architecture & ADR Query**:
   > *"What is the architectural decision for session caching and payment transactions?"*
2. **Firestore Gotcha Lookup**:
   > *"Search Firestore for operational gotchas regarding Agent Platform project ID."*
3. **Diagram Generation**:
   > *"Generate an architecture diagram for the Authentication Service with Redis and PostgreSQL."*
4. **Live GitHub Repository Query**:
   > *"Fetch repository details for google/adk."*
5. **RAG Reference Document Grounding**:
   > *"Consult reference docs to find remedies or instructions."*
