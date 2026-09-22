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
from google.cloud import firestore
from google.api_core.exceptions import NotFound, GoogleAPICallError

# HARDCODED PROJECT ID string (DO NOT use google.auth.default() or GOOGLE_CLOUD_PROJECT)
PROJECT_ID = "qwiklabs-gcp-02-3932e9061bcb"
COLLECTION_NAME = "tribal_knowledge_items"
FALLBACK_FILE = os.path.join(os.path.dirname(__file__), "..", "app", "firestore_fallback.json")

SEED_ITEMS = [
    {
        "id": "adr_001_session_caching",
        "title": "ADR-001: Session Caching Strategy (Redis vs Memcached)",
        "category": "Architecture Decision",
        "owner": "Bob Johnson (@bob_sec)",
        "content": "Standardized on Redis over Memcached for user session storage because Memcached lacks persistence and pub/sub. Redis AOF persistence prevents session data loss across container restarts, and Redis pub/sub enables instant global token revocation.",
        "tags": ["redis", "caching", "sessions", "architecture"],
        "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    },
    {
        "id": "adr_002_payment_database",
        "title": "ADR-002: Primary Database for Payment Transactions",
        "category": "Architecture Decision",
        "owner": "Alice Smith (@alice_dev)",
        "content": "Selected PostgreSQL with strict ACID compliance and row-level locking for the Payment ledger service to prevent double-billing and billing race conditions under high concurrency.",
        "tags": ["database", "postgres", "payments", "acid"],
        "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    },
    {
        "id": "gotcha_001_agent_platform_project_id",
        "title": "Operational Gotcha: Agent Platform Project ID vs Project Number",
        "category": "Operational Gotcha",
        "owner": "Dave Miller (@dave_ops)",
        "content": "On Agent Platform / Cloud Run, GOOGLE_CLOUD_PROJECT returns the numeric project number (e.g., 898315975450). Firestore Client(project=...) requires the alphanumeric project ID ('qwiklabs-gcp-02-3932e9061bcb'). Always hardcode or pass the alphanumeric project ID string.",
        "tags": ["agent-platform", "firestore", "gotcha", "gcp"],
        "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    },
    {
        "id": "ownership_001_auth_service",
        "title": "Component Ownership: Authentication & Security Service",
        "category": "Component Ownership",
        "owner": "Bob Johnson (@bob_sec)",
        "content": "Maintained by Bob Johnson. Handles OAuth 2.0, JWT token generation, and role-based access control. On-call escalation channel: #auth-sec-oncall.",
        "tags": ["auth", "security", "ownership", "jwt"],
        "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
]

def seed_database():
    print(f"Connecting to Firestore with hardcoded project ID: '{PROJECT_ID}'...")
    fallback_dict = {}

    try:
        db = firestore.Client(project=PROJECT_ID)
        collection_ref = db.collection(COLLECTION_NAME)

        for item in SEED_ITEMS:
            doc_id = item["id"]
            doc_data = {k: v for k, v in item.items() if k != "id"}
            collection_ref.document(doc_id).set(doc_data)
            print(f"Seeded Firestore document '{doc_id}': {item['title']}")
            fallback_dict[doc_id] = item
        print("\n✅ Cloud Firestore seeding complete!")

    except (NotFound, GoogleAPICallError, Exception) as e:
        print(f"\n⚠️ Firestore API / database notice ({str(e)}). Seeding to fallback store...")
        for item in SEED_ITEMS:
            fallback_dict[item["id"]] = item
            print(f"Seeded fallback document '{item['id']}': {item['title']}")

    # Save to fallback store
    os.makedirs(os.path.dirname(FALLBACK_FILE), exist_ok=True)
    with open(FALLBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(fallback_dict, f, indent=2)
    print(f"✅ Fallback knowledge store saved to {FALLBACK_FILE}")

if __name__ == "__main__":
    seed_database()
