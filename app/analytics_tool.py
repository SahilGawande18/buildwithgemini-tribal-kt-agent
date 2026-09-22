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


def get_knowledge_analytics(project_name: str = "NovaSmart Platform") -> str:
    """Generates an executive knowledge analytics dashboard showing documentation health, top queried microservices, and team gotcha frequency metrics.

    Args:
        project_name: Name of the project (e.g. 'Billing Service', 'Payment Gateway', 'NovaSmart Platform').

    Returns:
        Structured executive analytics report detailing knowledge coverage, top gotchas, and documentation health metrics.
    """
    logger.info(f"Generating knowledge analytics dashboard for project '{project_name}'")

    report = f"""📊 **Enterprise AI Knowledge & Observability Dashboard**
📌 **Target Scope**: `{project_name}` | **Status**: ACTIVE MONITORING

---

### 1. 📈 Knowledge Coverage Metrics
- **ADR Documentation Health Score**: `94/100` (🟢 EXCELLENT)
- **Indexed Confluence Wiki Pages**: `18 Space Pages`
- **Vertex AI RAG Corpus Coverage**: `100% Vector Embedded`
- **Active Maintainer Graph Nodes**: `12 Microservices & Engineers`

---

### 2. 🔥 Top Queried Microservices & Topics
1. **Firestore Alphanumeric Project ID Gotcha**: `142 queries/week`
2. **Payment Gateway Redis Caching Strategy**: `98 queries/week`
3. **Authentication Core JWT Rotation**: `76 queries/week`
4. **Vertex AI Memory Bank State Sync**: `64 queries/week`

---

### 3. 🚨 Identified Documentation Gaps & Recommendations
- ⚠️ **Gap**: Legacy Memcached deprecation migration plan lacks an updated ADR.
- 💡 **Action**: Use `generate_synthetic_confluence_doc` to create a `Memcached to Redis Migration ADR`.
- ✅ **Health Index**: All core payment and billing pipelines have active owner graph nodes.
"""

    return report
