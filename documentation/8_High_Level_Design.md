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
3. **Routing & Triage:** The Multi-Agent Router evaluates the first utterance using Sarvam AI's Chat Completion API. It classifies the caller's intent and routes the context object to the appropriate Industry-Specific Agent (e.g., Hotel, Education, Salon).
4. **Fulfillment:** The specialized agent processes the query (using a highly targeted system prompt), referencing the local Integration Layer to check availability via the clinic's CRM or PostgreSQL database.
5. **Response:** The Core Engine generates a response string, passes it to Sarvam AI's Indic-TTS synthesizer to generate an audio buffer, and streams it back to the caller through the Telephony Edge.
6. **Action Execution:** The Integration Layer securely commits the booking locally, sends SMS confirmations, and archives the transcript/audio to the Postgres Data Layer.

## 4. Key Component Responsibilities
* **API Gateway (FastAPI):** Entry point for frontend management portals and telephony WebHooks. Routes traffic to appropriate internal Python logic objects.
* **State Management Store (Redis - Local Docker):** Maintains the short-lived session context (e.g., conversation history, user selections, temporary state) for active calls. This is crucial for sub-second latency handling.
* **Event & Storage Bus:** Handles asynchronous cross-module communication specifically for post-call processing (saving the final JSON payload and Call data to the local PostgreSQL instance).

## 5. Security & Scalability
* **Scalability:** All core services are containerized (Docker/Kubernetes) and stateless (where state is pushed to Redis), allowing horizontal pod auto-scaling based on simultaneous call volume and CPU utilization.
* **Security:** Audio streams are encrypted via SRTP. Database data at rest is encrypted via AES-256. API requests enforce JWT validation. PII redaction runs as an asynchronous pre-processor before any transcript is moved to historical storage.
