### 4) Data & Storage Plan

**General Assumptions:**
* **Average Call Duration:** 3 minutes
* **Audio Format & Size:** Compressed Opus or MP3 (approx. 1 MB per minute). Total = ~3 MB per call.
* **Transcript Size:** ~10 KB of text per call.
* **Summary/Metadata:** Small JSON objects.

| Data Type | Assumption (Format & Duration) | Estimated Size per Call | Retention Policy | Storage Location / Database Type |
| :--- | :--- | :--- | :--- | :--- |
| **Audio Recording** | Compressed MP3/Opus (3 mins) | ~3 MB | 1-7 years (depending on industry compliance, e.g., Healthcare vs Retail) | Cloud Blob Storage (e.g., AWS S3, Azure Blob) with lifecycle policies. |
| **Full Transcript** | Text/JSON format | ~10 KB | 3-5 years | Relational DB (PostgreSQL) or Document DB (MongoDB). |
| **Summary Notes** | Extracted Key-Value points (JSON) | ~2 KB | 3-5 years | Relational DB (PostgreSQL) - indexed for fast searching. |
| **Booking/Action Metadata** | Timestamps, IDs, Status codes | ~1 KB | 3-5 years (or perpetual if anonymized) | Relational DB (PostgreSQL). |
| **Agent Logs** | System execution logs, latency metrics | ~5 KB | 30-90 days | Log Management Service (e.g., Elasticsearch, AWS CloudWatch). |

### 4.1 Auditing & Compliance Measures
1. **PII Redaction (Data Scrubber):** A post-call background worker is responsible for running a regex/NER scrubber over the transcript JSON. It replaces sensitive information (like Credit Card numbers, SSNs, and PHI) with `[REDACTED]` *before* it is saved to long-term Postgres storage. Currently, this worker runs asynchronously using Celery.
2. **Security at Rest:** All Database data (Audio Blob Volume and PostgreSQL Metadata) is encrypted at rest using AES-256. Access is restricted via strict Role-Based Access Control (RBAC) to ensure employees cannot arbitrarily listen to raw audio recordings without proper auditing trails.
