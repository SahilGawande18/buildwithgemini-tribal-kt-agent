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

import logging

logger = logging.getLogger(__name__)


def generate_onboarding_quiz(project_name: str = "NovaSmart Platform", difficulty: str = "medium") -> str:
    """Generates an interactive technical onboarding quiz to test an engineer's understanding of a project's architecture, ADRs, and gotchas.

    Args:
        project_name: Name of the project (e.g., 'Billing Service', 'Payment Gateway', 'NovaSmart Platform').
        difficulty: Quiz difficulty level ('easy', 'medium', 'advanced').

    Returns:
        Interactive quiz assessment with architectural questions, multiple-choice options, and answer explanation keys.
    """
    logger.info(f"Generating onboarding quiz for project '{project_name}' ({difficulty})")

    quiz_data = f"""📝 **Interactive Engineer Onboarding Quiz: [{project_name}]**
**Level**: `{difficulty.upper()}` | **Topic**: Architecture, ADRs, & Operational Gotchas

---

### Question 1: Data Consistency & Persistence
In `{project_name}`, why must the Firestore client be initialized with a hardcoded string `project="qwiklabs-gcp-02-3932e9061bcb"` instead of `google.auth.default()`?
- **A)** `google.auth.default()` is deprecated in Python 3.11.
- **B)** On Agent Engine, `google.auth.default()` returns numeric project number instead of project ID, breaking Firestore authentication. ✅
- **C)** Firestore requires project IDs to be written in uppercase.
- **D)** To prevent Cloud Run from scaling down instances.

---

### Question 2: Memory & Session Context
How does `{project_name}` persist engineer role preferences across different browser sessions?
- **A)** By storing unencrypted cookies in local storage only.
- **B)** By writing durable user facts into **Vertex AI Memory Bank** via `PreloadMemoryTool` and callbacks. ✅
- **C)** By storing session state in a temporary Redis cache.
- **D)** By creating a new Git branch for every session.

---

### Question 3: Microservice Communication
What protocol is used by the Cloud Run frontend proxy to communicate with the Agent Engine runtime?
- **A)** Raw WebSocket connections over port 80.
- **B)** Agent-to-Agent (A2A) JSON-RPC protocol over HTTPS. ✅
- **C)** Plain gRPC without authentication headers.
- **D)** Local file system IPC sockets.

---

💡 **Score Key**:
- **3/3 Correct**: 🏆 **Senior Architecture Mastery** — Ready to commit code to production!
- **2/3 Correct**: 🟡 **Onboarding In Progress** — Review team ADRs and gotcha docs.
- **<2 Correct**: 🔴 **KT Required** — Consult `consult_reference_docs` or ask the agent for onboarding guidance.
"""

    return quiz_data
