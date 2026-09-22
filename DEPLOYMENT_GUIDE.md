# Custom Google Cloud Setup & Deployment Guide (`DEPLOYMENT_GUIDE.md`)

This guide provides step-by-step instructions for deploying the **Tribal Knowledge & KT Agent** into any personal, enterprise, or custom **Google Cloud Platform (GCP) Project**.

---

## 📋 Prerequisites & Tools Required

1. **Google Cloud SDK (`gcloud`)**: Installed and authenticated with your personal/company Google account (`gcloud auth login`).
2. **Python 3.11+ & `uv`**: Installed on your local workstation.
3. **`agents-cli`**: Installed (`pip install google-agents-cli`).
4. **GitHub CLI (`gh`)**: For managing code repositories (`gh auth login`).

---

## 🚀 Step 1: Configure Your Google Cloud Project

1. Set your custom Google Cloud Project ID:
   ```bash
   gcloud config set project YOUR_CUSTOM_PROJECT_ID
   ```

2. Enable required Google Cloud APIs:
   ```bash
   gcloud services enable \
     aiplatform.googleapis.com \
     firestore.googleapis.com \
     storage.googleapis.com \
     run.googleapis.com \
     cloudbuild.googleapis.com
   ```

3. Create a Cloud Storage Bucket for public assets & uploaded files:
   ```bash
   gsutil mb -l us-central1 gs://YOUR_CUSTOM_PROJECT_ID-tribal-media
   gsutil iam ch allUsers:objectViewer gs://YOUR_CUSTOM_PROJECT_ID-tribal-media
   ```

4. Initialize Firestore Database (Native Mode):
   ```bash
   gcloud alpha firestore databases create --region=us-central1
   ```

---

## 🛠️ Step 2: Update Hardcoded Project IDs in Codebase

Search and replace the project ID string `qwiklabs-gcp-02-3932e9061bcb` with your `YOUR_CUSTOM_PROJECT_ID` across these key files:

| File Path | Variable / Parameter to Update |
| :--- | :--- |
| `app/firestore_service.py` | `PROJECT_ID = "YOUR_CUSTOM_PROJECT_ID"` |
| `app/cloud_storage.py` | `BUCKET_NAME = "YOUR_CUSTOM_PROJECT_ID-tribal-media"` |
| `app/doc_generator_tool.py` | `PROJECT_ID = "YOUR_CUSTOM_PROJECT_ID"` |
| `app/image_gen_tool.py` | `PROJECT_ID = "YOUR_CUSTOM_PROJECT_ID"` |
| `frontend/main.py` | `BUCKET_NAME = "YOUR_CUSTOM_PROJECT_ID-tribal-media"` |
| `agents-cli-manifest.yaml` | `project_id: YOUR_CUSTOM_PROJECT_ID` |

---

## 🚢 Step 3: Deploy Agent Engine & Cloud Run Frontend

### 1. Deploy the Agent Runtime:
```bash
agents-cli deploy --project YOUR_CUSTOM_PROJECT_ID --region us-central1 --no-confirm-project
```
*Note the output `Agent Runtime ID` (e.g., `projects/<PROJECT_NUMBER>/locations/us-central1/reasoningEngines/<ENGINE_ID>`).*

### 2. Deploy the Cloud Run Frontend:
```bash
gcloud run deploy tribal-kt-frontend \
  --source frontend \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="AGENT_ENGINE_RESOURCE_NAME=projects/<PROJECT_NUMBER>/locations/us-central1/reasoningEngines/<ENGINE_ID>,AGENT_DIRECTORY=app" \
  --project=YOUR_CUSTOM_PROJECT_ID \
  --quiet
```

---

## 🐙 Step 4: Push Updates to GitHub

Whenever you make changes to your project, commit and push them to your personal GitHub repository:

```bash
git add .
git commit -m "Updated project configuration for custom GCP deployment"
git push origin main
```

Your code will automatically sync to your public repository:
👉 `https://github.com/SahilGawande18/buildwithgemini-tribal-kt-agent`
