# Backend Engineering Onboarding Guide & Architecture Decisions

## Component Overview & Ownership
- **Payment Service**: 
  - Owner: Alice Smith (@alice_dev)
  - Tech Stack: Python / FastAPI, PostgreSQL
  - Status: Active
  - Tribal Knowledge: Payment webhook retries back off exponentially. Do not manually flush queue during high-traffic sales.

- **Authentication & Identity Service**:
  - Owner: Bob Johnson (@bob_sec)
  - Tech Stack: Go, Redis, JWT
  - Status: Active
  - Tribal Knowledge: Uses Redis instead of Memcached because we require AOF persistence and key-space notifications for session invalidation.

- **User Profile Service**:
  - Owner: Charlie Davis (@charlie_data)
  - Tech Stack: Python, Firestore
  - Status: Active
  - Tribal Knowledge: Customer preference flags are cached locally in memory for 60 seconds.

## Architecture Decision Records (ADRs)

### ADR-001: Session Caching Strategy (Redis vs Memcached)
- **Status**: Approved
- **Decision**: Standardize on Redis for session caching across all microservices.
- **Rationale**: Memcached does not support persistence or pub/sub. Redis allows background snapshotting, AOF persistence, and sub/pub events for instant token revocation.
- **Maintainer**: Bob Johnson

### ADR-002: Primary Database for Payment Transactions (PostgreSQL)
- **Status**: Approved
- **Decision**: Use PostgreSQL with ACID compliance for payment ledger transactions.
- **Rationale**: Strict transactions and row-level locking prevent race conditions in billing events.
- **Maintainer**: Alice Smith
