### 5) Cost & Scaling Analysis

**Underlying Primary Assumptions:**
* **Telephony Cost:** ~$0.015 per minute.
* **Speech Conversion:** ~$0.020 per minute combined.
* **Processing Cost:** ~$0.005 per minute equivalent.
* **Total Processing Cost:** ~$0.04 per minute -> ~$0.12 per average 3-minute call.
* **Storage Cost:** ~$0.023 per GB/month for standard Blob storage.
* *Note: Infrastructure/Fixed costs scale in tiers based on database throughput and support requirements.*

| Cost Component | Small Client (2,000 calls/mo) | Medium Client (20,000 calls/mo) | Large Client (200,000 calls/mo) |
| :--- | :--- | :--- | :--- |
| **Call Minutes Cost (Telephony)** | $90 | $900 | $9,000 |
| **Speech Conversion** | $120 | $1,200 | $12,000 |
| **Processing Cost** | $30 | $300 | $3,000 |
| **Storage Cost** | ~$0.15 (6 GB baseline) | ~$1.50 (60 GB baseline) | ~$15.00 (600 GB baseline) |
| **Support/Monitoring/Infra Cost** | $150 (Basic Cloud Infra) | $500 (Dedicated DBs, Alerts) | $2,000 (HA Setup, Premium Support) |
| **Total Estimated Monthly Cost** | **~$390** | **~$2,901** | **~$26,015** |

*(Cost per call averages to approximately $0.19 for small clients, scaling down to ~$0.13 for large Enterprise clients due to infra amortization).*
