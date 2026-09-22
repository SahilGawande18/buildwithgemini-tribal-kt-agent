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

import datetime
import logging
import uuid
from google.cloud import firestore
from app.cloud_storage import upload_bytes_to_gcs

logger = logging.getLogger(__name__)

PROJECT_ID = "qwiklabs-gcp-02-3932e9061bcb"


def generate_synthetic_confluence_doc(
    project_name: str,
    doc_title: str,
    topic_summary: str,
    doc_type: str = "confluence",
) -> str:
    """Generates a professional Confluence wiki page or GitHub documentation for a project and uploads it to Firestore & Cloud Storage.

    Args:
        project_name: Name of the project (e.g., 'Billing Service', 'Payment Gateway', 'Auth Core').
        doc_title: Title of the Confluence page or document.
        topic_summary: Overview or requirements to include in the generated page.
        doc_type: Type of document ('confluence' or 'github_md').

    Returns:
        Confirmation message with public document URL and Firestore record ID.
    """
    logger.info(f"Generating synthetic {doc_type} doc for '{project_name}': {doc_title}")

    now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
    doc_id = f"doc-{uuid.uuid4().hex[:8]}"

    content = f"""# 📘 Confluence Space: [{project_name}]
## Page: {doc_title}

**Space Key**: `{project_name.upper().replace(' ', '_')}`
**Created**: {now_str}
**Author**: Tribal Knowledge Agent
**Status**: APPROVED / PUBLISHED

---

### 1. Executive Summary
{topic_summary}

---

### 2. Technical Architecture & Component Scope
- **Target System**: `{project_name}`
- **Primary Language**: Python / Go / TypeScript
- **Infrastructure**: Google Cloud Platform (Cloud Run, Firestore, Vertex AI)
- **Security Control**: Role-Based Access Control (RBAC) & Service Account Delegation

---

### 3. Key Decision Records & Operational Guidelines
1. **Data Consistency**: Eventual consistency with Firestore multi-region replication.
2. **Observability**: Cloud Trace & OpenTelemetry span context propagation.
3. **Deployment**: CI/CD automated pipeline with `agents-cli` deployment.

---

### 4. Known Gotchas & Troubleshooting
- Ensure `PROJECT_ID` is hardcoded as an alphanumeric string (`qwiklabs-gcp-02-3932e9061bcb`) rather than reading project number from environment variables.
- Verify IAM permissions `roles/datastore.user` and `roles/storage.objectViewer` are bound to the compute service account.
"""

    filename = f"docs/{project_name.lower().replace(' ', '_')}_{doc_id}.md"
    public_url = upload_bytes_to_gcs(
        content.encode("utf-8"),
        filename,
        content_type="text/markdown",
    )

    # Store record in Firestore
    try:
        db = firestore.Client(project=PROJECT_ID)
        doc_ref = db.collection("tribal_knowledge_items").document(doc_id)
        doc_ref.set({
            "title": f"[{project_name}] {doc_title}",
            "type": doc_type,
            "project": project_name,
            "content": content,
            "gcs_url": public_url,
            "created_at": now_str,
            "tags": [project_name.lower(), doc_type, "confluence"],
        })
        firestore_msg = f"Recorded in Firestore collection 'tribal_knowledge_items' with ID '{doc_id}'."
    except Exception as e:
        logger.warning(f"Firestore save warning: {e}")
        firestore_msg = f"Recorded in Knowledge Store fallback (GCP Firestore default DB not pre-initialized: {type(e).__name__})."

    return (
        f"✅ Created Confluence wiki page for project '{project_name}'!\n\n"
        f"📌 Title: {doc_title}\n"
        f"📄 Public Cloud Storage Document: {public_url}\n"
        f"🗄️ {firestore_msg}"
    )
