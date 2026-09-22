# Tribal Knowledge AI Agent Platform 🚀

> An enterprise agentic AI platform built with **Google ADK**, **Gemini 2.5 Flash**, **Vertex AI RAG Engine**, **Vertex AI Memory Bank**, and **Google Cloud Agent Engine**.

🌐 **Live Web Application**: [https://tribal-kt-frontend-898315975450.us-central1.run.app](https://tribal-kt-frontend-898315975450.us-central1.run.app)  
📦 **Public GitHub Repository**: [https://github.com/SahilGawande18/buildwithgemini-tribal-kt-agent](https://github.com/SahilGawande18/buildwithgemini-tribal-kt-agent)

---

## 📖 Key Documentation
- 📘 [PROJECT_OVERVIEW.md](file:///config/Desktop/Session1/tribal-kt-agent/PROJECT_OVERVIEW.md) — Comprehensive Architecture & Feature Specification
- 🚀 [DEPLOYMENT_GUIDE.md](file:///config/Desktop/Session1/tribal-kt-agent/DEPLOYMENT_GUIDE.md) — Custom GCP Project Deployment & Setup Guide

---

## ✨ Features at a Glance

1. **💬 Agent Q&A Studio (ChatGPT Mode)**: Conversational chat interface with left sidebar session management (Rename ✏️ & Delete 🗑️).
2. **📁 Create & Ingest Project Workspace**: Dedicated tab to create new projects, link GitHub Repository URLs, and upload local documents (PDFs/Markdown).
3. **🛠️ Advanced Agent Tools Workspace**: Run Code Security Compliance Audits, Onboarding Quizzes, Knowledge Analytics, and Architecture Diagram Rendering.
4. **📘 Confluence & Technical Doc Studio**: Draft wiki space pages, preview syntax, download `.md` files locally, or push directly to Cloud Storage & Firestore.

---

## 🛠️ Quick Start

```bash
git clone https://github.com/SahilGawande18/buildwithgemini-tribal-kt-agent.git
cd buildwithgemini-tribal-kt-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn frontend.main:app --port 8080
```
