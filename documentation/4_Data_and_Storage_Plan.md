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
