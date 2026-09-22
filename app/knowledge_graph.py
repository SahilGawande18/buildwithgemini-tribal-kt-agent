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
import sqlite3
import logging

logger = logging.getLogger(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "knowledge_graph.db")

def init_db():
    """Initialize the SQLite Knowledge Graph database schema and seed default data."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        category TEXT NOT NULL,
        owner TEXT,
        description TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT NOT NULL,
        relation TEXT NOT NULL,
        target TEXT NOT NULL,
        notes TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS decisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE NOT NULL,
        decision TEXT NOT NULL,
        rationale TEXT NOT NULL,
        owner TEXT NOT NULL
    );
    """)

    # Seed default entities if empty
    cursor.execute("SELECT COUNT(*) FROM entities")
    if cursor.fetchone()[0] == 0:
        logger.info("Seeding initial Knowledge Graph entities...")
        cursor.executemany("""
        INSERT INTO entities (name, category, owner, description) VALUES (?, ?, ?, ?)
        """, [
            ("Authentication Service", "Microservice", "Bob Johnson (@bob_sec)", "Go-based auth and JWT token management service."),
            ("Payment Service", "Microservice", "Alice Smith (@alice_dev)", "Python/FastAPI payment ledger and transaction service."),
            ("User Profile Service", "Microservice", "Charlie Davis (@charlie_data)", "Firestore-backed user preferences service."),
            ("Redis Cache", "Infrastructure", "Bob Johnson (@bob_sec)", "In-memory cache for token sessions with AOF persistence."),
            ("PostgreSQL", "Database", "Alice Smith (@alice_dev)", "Relational ACID database for financial payment transactions.")
        ])

        cursor.executemany("""
        INSERT INTO relationships (source, relation, target, notes) VALUES (?, ?, ?, ?)
        """, [
            ("Authentication Service", "USES_CACHE", "Redis Cache", "Uses AOF persistence and pub/sub token revocation"),
            ("Payment Service", "USES_DATABASE", "PostgreSQL", "Requires strict ACID compliance and row locking"),
            ("Authentication Service", "MAINTAINED_BY", "Bob Johnson (@bob_sec)", "Contact for security and JWT issues"),
            ("Payment Service", "MAINTAINED_BY", "Alice Smith (@alice_dev)", "Contact for payment webhook retries")
        ])

        cursor.executemany("""
        INSERT INTO decisions (title, decision, rationale, owner) VALUES (?, ?, ?, ?)
        """, [
            ("ADR-001: Session Cache", "Use Redis over Memcached", "Memcached lacks persistence and pub/sub. Redis AOF ensures sessions survive server restarts and allows real-time token revocation.", "Bob Johnson"),
            ("ADR-002: Payment Database", "Use PostgreSQL", "Row-level locking and strict transactions prevent billing race conditions.", "Alice Smith")
        ])

    conn.commit()
    conn.close()

# Auto-initialize DB on module import
init_db()

def query_graph(search_term: str) -> dict:
    """Search knowledge graph entities, relationships, and architecture decisions."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    term = f"%{search_term.strip()}%"

    cursor.execute("SELECT name, category, owner, description FROM entities WHERE name LIKE ? OR description LIKE ? OR owner LIKE ?", (term, term, term))
    entities = [{"name": r[0], "category": r[1], "owner": r[2], "description": r[3]} for r in cursor.fetchall()]

    cursor.execute("SELECT source, relation, target, notes FROM relationships WHERE source LIKE ? OR target LIKE ? OR relation LIKE ? OR notes LIKE ?", (term, term, term, term))
    relationships = [{"source": r[0], "relation": r[1], "target": r[2], "notes": r[3]} for r in cursor.fetchall()]

    cursor.execute("SELECT title, decision, rationale, owner FROM decisions WHERE title LIKE ? OR decision LIKE ? OR rationale LIKE ? OR owner LIKE ?", (term, term, term, term))
    decisions = [{"title": r[0], "decision": r[1], "rationale": r[2], "owner": r[3]} for r in cursor.fetchall()]

    conn.close()
    return {
        "query": search_term,
        "entities": entities,
        "relationships": relationships,
        "architecture_decisions": decisions
    }

def add_entity(name: str, category: str, owner: str, description: str):
    """Add or update an entity in the knowledge graph."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO entities (name, category, owner, description) VALUES (?, ?, ?, ?)
    ON CONFLICT(name) DO UPDATE SET category=excluded.category, owner=excluded.owner, description=excluded.description
    """, (name, category, owner, description))
    conn.commit()
    conn.close()
