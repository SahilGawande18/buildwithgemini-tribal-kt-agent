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
import json
import datetime
import logging
from google.cloud import firestore
from google.api_core.exceptions import NotFound, GoogleAPICallError

logger = logging.getLogger(__name__)

# HARDCODED PROJECT ID string to prevent Agent Platform project number resolution issues
PROJECT_ID = "qwiklabs-gcp-02-3932e9061bcb"
COLLECTION_NAME = "tribal_knowledge_items"
FALLBACK_FILE = os.path.join(os.path.dirname(__file__), "firestore_fallback.json")

_db_client = None

def get_firestore_client() -> firestore.Client:
    """Return an initialized Firestore client using the hardcoded alphanumeric Project ID."""
    global _db_client
    if _db_client is None:
        logger.info(f"Initializing Firestore client for hardcoded project ID: {PROJECT_ID}")
        _db_client = firestore.Client(project=PROJECT_ID)
    return _db_client


def _load_fallback_data() -> dict:
    if os.path.exists(FALLBACK_FILE):
        try:
            with open(FALLBACK_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _save_fallback_data(data: dict):
    with open(FALLBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def search_firestore_knowledge(query: str = "", category: str = None) -> list[dict]:
    """Search and retrieve tribal knowledge items stored in the Cloud Firestore backend (`tribal_knowledge_items` collection).

    Args:
        query: Optional string to filter title, content, or tags.
        category: Optional category filter (e.g., 'Architecture Decision', 'Component Ownership', 'Operational Gotcha').

    Returns:
        A list of matching tribal knowledge documents from Firestore.
    """
    results = []
    try:
        db = get_firestore_client()
        collection_ref = db.collection(COLLECTION_NAME)

        if category:
            docs = collection_ref.where("category", "==", category).stream()
        else:
            docs = collection_ref.stream()

        query_lower = query.lower().strip()
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            if query_lower:
                matchable_text = f"{data.get('title', '')} {data.get('content', '')} {' '.join(data.get('tags', []))} {data.get('owner', '')}".lower()
                if query_lower in matchable_text:
                    results.append(data)
            else:
                results.append(data)

        logger.info(f"Firestore query succeeded: {len(results)} items found.")
        return results

    except (NotFound, GoogleAPICallError, Exception) as e:
        logger.warning(f"Cloud Firestore database unavailable ({str(e)}). Using local fallback store.")
        fallback = _load_fallback_data()
        query_lower = query.lower().strip()
        for doc_id, data in fallback.items():
            if category and data.get("category") != category:
                continue
            if query_lower:
                matchable_text = f"{data.get('title', '')} {data.get('content', '')} {' '.join(data.get('tags', []))} {data.get('owner', '')}".lower()
                if query_lower in matchable_text:
                    results.append(data)
            else:
                results.append(data)
        return results


def save_firestore_knowledge_item(title: str, category: str, owner: str, content: str, tags: list[str] = None) -> dict:
    """Create or update a tribal knowledge entry in the Cloud Firestore backend (`tribal_knowledge_items` collection).

    Args:
        title: Title of the tribal knowledge entry or ADR (e.g. 'ADR-003: Postgres Read Replicas').
        category: Category of the item ('Architecture Decision', 'Component Ownership', 'Operational Gotcha').
        owner: Name/handle of the maintainer or owner (e.g. 'Alice Smith (@alice_dev)').
        content: Detailed content, rationale, or instructions.
        tags: List of descriptive tags (e.g. ['database', 'postgres', 'scaling']).

    Returns:
        Status dictionary with document ID and payload.
    """
    doc_id = title.lower().replace(" ", "_").replace(":", "").replace("-", "_")[:50]
    payload = {
        "id": doc_id,
        "title": title,
        "category": category,
        "owner": owner,
        "content": content,
        "tags": tags or [],
        "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }

    try:
        db = get_firestore_client()
        doc_ref = db.collection(COLLECTION_NAME).document(doc_id)
        doc_ref.set(payload)
        logger.info(f"Successfully saved item '{title}' to Firestore with ID: {doc_id}")
        
        # Mirror to fallback
        fallback = _load_fallback_data()
        fallback[doc_id] = payload
        _save_fallback_data(fallback)
        return {"status": "success", "doc_id": doc_id, "data": payload}

    except (NotFound, GoogleAPICallError, Exception) as e:
        logger.warning(f"Firestore database unavailable ({str(e)}). Saving to local fallback store.")
        fallback = _load_fallback_data()
        fallback[doc_id] = payload
        _save_fallback_data(fallback)
        return {"status": "success_fallback", "doc_id": doc_id, "data": payload, "note": f"Saved to fallback store: {str(e)}"}
