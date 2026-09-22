# 🚀 Tribal Knowledge AI Platform — Comprehensive Project Documentation

Welcome to the **Tribal Knowledge AI Platform**, an enterprise-grade AI-powered agentic system built with **Google ADK (Agent Development Kit)**, **Gemini 2.5 Flash**, **Vertex AI RAG Engine**, **Vertex AI Memory Bank**, and **Google Cloud Agent Engine**.

---

## 🏛️ Project Architecture & Overview

The platform addresses a critical engineering problem in modern tech teams: **Siloed Tribal Knowledge & Fragmented Onboarding**. 

By unifying repository code, architecture decision records (ADRs), Confluence space pages, operational gotchas, and PDF documentations into a single multi-model intelligence engine, engineers can instantly query, audit, and onboard into complex microservice estates.

```
                          ┌───────────────────────────────────────┐
                          │   Tribal Knowledge AI Web Frontend    │
                          │   (Cloud Run - FastAPI + A2UI Cards)  │
                          └───────────────────┬───────────────────┘
                                              │ A2A JSON-RPC Protocol
                                              ▼
                          ┌───────────────────────────────────────┐
                          │     Google Agent Engine Runtime       │
                          │  (Gemini 2.5 Flash + ADK Framework)   │
                          └───────────────────┬───────────────────┘
                                              │
         ┌───────────────────┬────────────────┼───────────────────┬───────────────────┐
         ▼                   ▼                ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌───────────┐   ┌───────────────────┐ ┌─────────────────┐
│  Graph Database │ │  Vector DB      │ │ Firestore │   │ Cloud Storage     │ │ Vertex AI Memory│
│  (Dependencies) │ │  (RAG Engine)   │ │  (ADRs)   │   │  (Public Media)   │ │  (Cross-Session)│
└─────────────────┘ └─────────────────┘ └───────────┘   └───────────────────┘ └─────────────────┘
```

---

## ✨ Core Platform Capabilities & Features

### 1. 💬 Agent Q&A Studio (Clean ChatGPT Experience)
- **Conversational ChatGPT Interface**: Uncluttered chat window for natural dialogue, architecture discussions, and next-step sprint planning.
- **Left Sidebar Session Management**: Collapsible chat history with **New Chat**, **Rename ✏️**, and **Delete 🗑️** options stored persistently in `localStorage`.
- **A2UI Rich Card Rendering**: Natively renders display cards, rows, columns, and embedded images alongside plain text responses.

### 2. 📁 Create & Ingest Project Workspace
- **Dedicated Project Creation**: Initialize brand-new project scopes (`Payment Gateway`, `Billing Service`, `NovaSmart Platform`, etc.).
- **Local File & Spec Ingestion**: Upload PDFs, Markdown manuals, TXT specifications, and JSON schemas directly into project scope.
- **GitHub Repository Parsing**: Link external GitHub Repository URLs (`https://github.com/org/repo`) for on-demand code tree parsing and commit history analysis.
- **AI Model Selection**: Select preferred reasoning models (`Gemini 2.5 Flash`, `Gemini 1.5 Pro`, `Gemini Flash Latest`) per project.

### 3. 🛠️ Advanced Agent Tools Workspace
- **🛡️ Codebase Compliance & Security Scanner (`audit_codebase_compliance`)**:
  - Audits code snippets for security vulnerabilities, hardcoded secret gotchas, unhandled exceptions, and team ADR compliance.
  - Calculates a compliance score (`0-100/100`) and provides refactored code recommendations.
- **🎲 Interactive Technical Onboarding Quiz Generator (`generate_onboarding_quiz`)**:
  - Generates real-time randomized technical quizzes testing microservice architecture, DB choices, ADRs, and operational gotchas.
  - Configurable question counts (e.g. 3, 4, 5 questions) with customized scoring keys.
- **📊 Enterprise Knowledge Analytics Dashboard (`get_knowledge_analytics`)**:
  - Evaluates documentation health scores (`0-100`), indexed wiki pages, and top queried team gotchas.
- **📐 System Architecture Visual Renderer (`generate_architecture_diagram`)**:
  - Generates enterprise dark-mode system architecture diagrams rendered directly in A2UI cards.

### 4. 📘 Confluence & Document Studio
- **Dedicated Wiki Generator (`generate_synthetic_confluence_doc`)**: Drafts detailed Confluence space pages or GitHub technical specs.
- **📥 Local Download**: Save generated documentation directly to your computer as `.md` files.
- **☁️ Cloud Push Configuration Modal**: Interactively configure Google Cloud Project ID, Cloud Storage bucket, and Confluence space key parameters for direct cloud storage and Firestore publishing.

---

## 🗄️ Knowledge Storage Architecture

| Engine | Storage Role | Function / Tool |
| :--- | :--- | :--- |
| **Graph Database** | Microservice dependencies & maintainer nodes | `query_knowledge_graph` |
| **Vertex AI RAG Engine** | Serverless vector embeddings for PDFs & docs | `consult_reference_docs` |
| **Cloud Firestore** | Structured ADR records & operational gotchas | `search_firestore_knowledge` |
| **Google Cloud Storage** | Architecture diagrams & Confluence `.md` files | `upload_bytes_to_gcs` |
| **Vertex AI Memory Bank** | Durable cross-session engineer preferences | `PreloadMemoryTool` |

---

## 🌐 Live System Deployment Details

- **GCP Project ID**: `qwiklabs-gcp-02-3932e9061bcb`
- **Region**: `us-central1`
- **Live Web Application**: [https://tribal-kt-frontend-898315975450.us-central1.run.app](https://tribal-kt-frontend-898315975450.us-central1.run.app)
- **Agent Engine Runtime ID**: `projects/898315975450/locations/us-central1/reasoningEngines/8017484308358889472`
- **Public GitHub Repository**: [https://github.com/SahilGawande18/buildwithgemini-tribal-kt-agent](https://github.com/SahilGawande18/buildwithgemini-tribal-kt-agent)

---

## 🚀 How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/SahilGawande18/buildwithgemini-tribal-kt-agent.git
cd buildwithgemini-tribal-kt-agent

# 2. Set up virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Configure Google Cloud credentials
gcloud auth login
gcloud config set project qwiklabs-gcp-02-3932e9061bcb

# 4. Start the frontend web server
python -m uvicorn frontend.main:app --reload --port 8080
```

Open [http://localhost:8080](http://localhost:8080) in your browser!

---

## 📄 License
Licensed under the Apache License, Version 2.0.
