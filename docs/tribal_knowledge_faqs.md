# Tribal Knowledge & FAQ Guide

## Frequently Asked Questions

### Q: Why do we use Redis for token sessions instead of Memcached?
**Answer**: Memcached is strictly in-memory without persistence. Redis gives us AOF persistence so active user sessions survive cache server restarts, plus Redis pub-sub lets us broadcast token revocations instantly across cluster nodes.

### Q: Who do I contact if the deployment pipeline fails on staging?
**Answer**: Contact DevOps On-Call or Dave Miller (@dave_ops). Make sure `aiplatform.googleapis.com` API is enabled and application default credentials (ADC) have been refreshed.

### Q: What is the gotcha with Firestore project IDs vs Project Numbers?
**Answer**: When deploying to Agent Engine / Cloud Run, `GOOGLE_CLOUD_PROJECT` returns the numeric project number. Firestore `Client(project=...)` requires the alphanumeric project ID (`qwiklabs-gcp-02-...`), not the project number.

### Q: Where are emergency database rollback procedures documented?
**Answer**: Check the `docs/confluence_architecture_decisions.md` ADR log or query `query_knowledge_graph` with 'PostgreSQL'.
