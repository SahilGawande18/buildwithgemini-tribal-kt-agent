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

import re
import logging
from google.cloud import firestore

logger = logging.getLogger(__name__)

PROJECT_ID = "qwiklabs-gcp-02-3932e9061bcb"


def audit_codebase_compliance(code_snippet: str, project_name: str = "General", language: str = "python") -> str:
    """Scans code snippets or configuration files for security vulnerabilities, hardcoded secrets, ADR compliance, and performance anti-patterns.

    Args:
        code_snippet: Code snippet or configuration text to audit.
        project_name: Name of the project (e.g. 'Billing Service', 'NovaSmart Platform').
        language: Programming language ('python', 'javascript', 'yaml', 'go').

    Returns:
        Structured code audit report with security findings, ADR compliance score, and recommended fixes.
    """
    logger.info(f"Auditing code compliance for project '{project_name}' in {language}")

    findings = []
    score = 100

    # 1. Secret / Credential Scan
    if re.search(r'(?i)(api[_-]?key|secret|password|bearer\s+[a-z0-9\.\-_]+)\s*[:=]\s*["\'][^"\']+["\']', code_snippet):
        findings.append("⚠️ **CRITICAL (Security)**: Hardcoded API key or bearer secret detected in code. Move to Secret Manager.")
        score -= 30

    # 2. Project ID vs Project Number Gotcha Scan
    if "google.auth.default()" in code_snippet or "GOOGLE_CLOUD_PROJECT" in code_snippet:
        findings.append("⚠️ **WARNING (Platform Gotcha)**: Using `google.auth.default()` or `GOOGLE_CLOUD_PROJECT` returns numeric project number on Agent Engine, breaking Firestore clients. Hardcode alphanumeric `PROJECT_ID` as string.")
        score -= 20

    # 3. Synchronous Blocking on Async Loops
    if "time.sleep(" in code_snippet or ".result()" in code_snippet:
        findings.append("⚠️ **WARNING (Performance)**: Synchronous blocking call detected (`time.sleep` / `.result()`). Use `asyncio.sleep` to prevent loop blocking.")
        score -= 15

    # 4. Missing Error Handling / Bare Except
    if re.search(r'except\s*:', code_snippet) or re.search(r'except\s+Exception\s*:\s*pass', code_snippet):
        findings.append("⚠️ **MEDIUM (Reliability)**: Bare or silent `except:` block detected. Log exact exceptions with traceback.")
        score -= 15

    # 5. Database Connection Pooling / ADR Compliance
    if "firestore.Client()" in code_snippet and "project=" not in code_snippet:
        findings.append("⚠️ **MEDIUM (ADR Compliance)**: Firestore client instantiated without explicit `project` parameter.")
        score -= 10

    if not findings:
        findings.append("✅ **PASSED**: No security vulnerabilities, hardcoded secrets, or performance anti-patterns detected!")

    score = max(score, 0)
    status_emoji = "🟢 PASS" if score >= 80 else ("🟡 WARNING" if score >= 50 else "🔴 FAIL")

    report = (
        f"🛡️ **Codebase Audit & ADR Compliance Report**\n"
        f"📌 **Target Project**: `{project_name}` | **Language**: `{language}`\n"
        f"📊 **Compliance Score**: `{score}/100` ({status_emoji})\n\n"
        f"### Audit Findings:\n" + "\n".join([f"- {f}" for f in findings]) + "\n\n"
        f"### Refactoring Recommendation:\n"
        f"```python\n"
        f"# Recommended compliant pattern for {project_name}\n"
        f"import logging\n"
        f"from google.cloud import firestore\n\n"
        f"PROJECT_ID = \"{PROJECT_ID}\"  # Explicit alphanumeric string\n\n"
        f"async def get_db_client():\n"
        f"    return firestore.Client(project=PROJECT_ID)\n"
        f"```"
    )

    return report
