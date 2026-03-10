# High Level Design (HLD) - Codefeast Smart Voice Agent System

## 1. Introduction
The Codefeast Smart Voice Agent is an automated AI-driven communication system designed to handle inbound and outbound telephone calls for service-based businesses. The system acts as a digital receptionist capable of conversing in over 30 languages, understanding natural language intents, and automating scheduling and notifications.

## 2. System Architecture Overview
The system follows an event-driven, multi-modular architecture broken into five primary distinct layers:
1. **Telephony & Edge Layer:** Handles PSTN/SIP signaling and connection management.
2. **Speech Processing Layer:** Manages high-throughput streaming audio translation, including VAD (Voice Activity Detection), STT (Speech-to-Text), and TTS (Text-to-Speech).
3. **Core Logic Engine (Multi-Agent System):** Manages the conversational context, routing, and intent fulfillment across multiple specialized processing units.
4. **Integration Layer:** Provides a unified gateway for external actions (CRM, API syncs, webhook firing, message delivery).
5. **Data & Storage Layer:** Manages states, logs, historical records, and persistent binary audio object storage.

## 3. High-Level Data Flow
1. **Inbound Trigger:** A caller dials the business number. The Telephony Edge (e.g., Twilio or local Asterisk PBX) captures the WebRTC audio stream and routes it to the FastAPI application via secured WebSockets.
2. **Translation:** The audio bytes are sent to Sarvam AI's Indic-ASR to transcribe into text chunks. 
3. **PII Tokenization (Security):** Before sending any data to the LLM, the `PIIScrubber` scans the text chunks for Credit Cards, SSNs, and Emails. It stores the real value in an encrypted local `PIIVault` and replaces the text with a secure string token (e.g., `[PII_TOKEN_XYZ]`).
4. **Input Guardrails (NeMo):** The text utterance is intercepted by NVIDIA NeMo `LLMRails`. It is checked against Colang flow rules to detect prompt injections, insults, or jailbreak attempts. Safe inputs are passed forward.
5. **Routing & Triage:** The Multi-Agent Router evaluates the sanitized utterance using Sarvam AI's Chat Completion API. It classifies the caller's intent and routes the context object to the appropriate Industry-Specific Agent (e.g., Hotel, Education, Salon).
6. **Output Guardrails (NeMo):** The Industry Agent formulates a response string. It is intercepted again by NeMo to ensure the AI did not hallucinate, respond with toxic language, or discuss competitor brands.
7. **Fulfillment & Restoration:** If the safe agent response contains a token, the Engine automatically pulls the real value back from the `PIIVault` and injects it into the final string so the local Integration Layer can securely process CRM actions (like payments).
8. **Response:** The Core Engine passes the restored response string to Sarvam AI's Indic-TTS synthesizer to generate an audio buffer, and streams it back to the caller through the Telephony Edge.
9. **Action Execution:** The Integration Layer securely commits the booking locally, sends SMS confirmations, and archives the cleanly scrubbed transcript/audio to the Postgres Data Layer.

## 4. Key Component Responsibilities
* **API Gateway (FastAPI):** Entry point for frontend management portals and telephony WebHooks. Routes traffic to appropriate internal Python logic objects.
* **State Management Store (Redis - Local Docker):** Maintains the short-lived session context (e.g., conversation history, user selections, temporary state) for active calls. This is crucial for sub-second latency handling.
* **Event & Storage Bus:** Handles asynchronous cross-module communication specifically for post-call processing (saving the final JSON payload and Call data to the local PostgreSQL instance).

## 5. Security & Scalability
* **Scalability:** All core services are containerized (Docker/Kubernetes) and stateless (where state is pushed to Redis), allowing horizontal pod auto-scaling based on simultaneous call volume and CPU utilization.
* **Security:** Audio streams are encrypted via SRTP. Database data at rest is encrypted via AES-256. API requests enforce JWT validation. PII redaction runs as an asynchronous pre-processor before any transcript is moved to historical storage.
