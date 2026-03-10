# Voice Agent API - Postman Collection & Documentation

This document outlines the API endpoints, webhooks, and WebSocket structures used by the Codefeast Smart Voice Agent. It serves as a reference for integrating testing tools like Postman, or for frontend and CRM developers.

---

## 1. WebSockets: Real-Time Audio Streaming

### `WS /api/v1/ws/stream-audio/{call_id}`
**Description:** The primary full-duplex WebSocket connection used by the telephony edge (e.g., Twilio Media Streams, Asterisk) to stream raw audio in and out of the conversational engine during an active call.

* **Connection URL:** `ws://localhost:8000/api/v1/ws/stream-audio/call_12345`
* **Direction:** Bi-directional

#### Incoming Message Format (From Telephony to Agent)
The agent expects binary audio chunks. If sending metadata (like Twilio does), it expects JSON wrappers.
```json
{
  "event": "media",
  "sequenceNumber": "1",
  "media": {
    "track": "inbound",
    "chunk": "1",
    "timestamp": "16542013000",
    "payload": "/+JQAQAAAAEAAQAB..." // Base64 encoded mu-law or PCM audio
  }
}
```

#### Outgoing Message Format (From Agent to Telephony)
After Sarvam AI evaluates the intent, the system replies with the synthesized audio payload.
```json
{
  "event": "media",
  "media": {
    "track": "outbound",
    "payload": "/+JQAQAAAAEAAQAB..." // Base64 encoded synthesized speech audio
  }
}
```

---

## 2. API Authentication

### `POST /api/v1/auth/token`
**Description:** Exchanges valid admin credentials for a JWT Bearer Token. Required for triggering outbound calls and managing the backend system.
* **Headers:** `Content-Type: application/x-www-form-urlencoded`
* **Sample Request Body:**
```text
username=admin&password=secret123
```
* **Sample JSON Response (HTTP 200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
  "token_type": "bearer"
}
```

---

## 3. Telephony API Webhooks

### `POST /api/v1/call/inbound`
**Description:** Triggered by the SIP provider (Twilio/Plivo/Asterisk) when a customer dials the business phone number. The endpoint must return the instructions (e.g., TwiML) telling the provider to connect the audio stream to our WebSocket.

* **Headers:** `Content-Type: application/x-www-form-urlencoded`
* **Sample Request Body (Twilio Standard):**
```text
CallSid=CA1234567890abcdef&From=+19876543210&To=+12345678900&CallStatus=ringing
```

* **Sample Response (HTTP 200 OK):**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect>
        <Stream url="wss://your-domain.com/api/v1/ws/stream-audio/CA1234567890abcdef" />
    </Connect>
</Response>
```

---

### `POST /api/v1/call/outbound`
**Description:** An internal endpoint triggered by the CRM or billing system to launch an outbound call (e.g., for a payment reminder).
* **Headers:** `Content-Type: application/json`, `Authorization: Bearer <YOUR_JWT_TOKEN>`

* **Sample JSON Request:**
```json
{
  "customer_number": "+19876543210",
  "business_id": "bus_9876",
  "intent": "payment_reminder",
  "context": {
    "name": "Jane Doe",
    "amount_due": 150.00,
    "currency": "USD"
  }
}
```

* **Sample JSON Response (HTTP 202 Accepted):**
```json
{
  "status": "success",
  "message": "Outbound call triggered for +19876543210",
  "authorized_user": "admin"
}
```

---

## 4. Integrations & CRM Triggers (Mock Examples)

These are the contracts the `services/integrations.py` folder will use to talk to external systems (or what external systems expose to the Voice Agent).

### `POST /integration/calendar/checkAvailability`
**Description:** The agent checks the salon or clinic database for open slots.
* **Sample JSON Request:**
```json
{
  "business_id": "bus_9876",
  "date": "2026-03-12",
  "service_type": "haircut"
}
```
* **Sample JSON Response:**
```json
{
  "available_slots": ["10:00", "11:30", "14:00"],
  "timezone": "America/New_York"
}
```

### `POST /integration/calendar/createBooking`
**Description:** The agent commits the final booking to the CRM.
* **Sample JSON Request:**
```json
{
  "business_id": "bus_9876",
  "customer_phone": "+19876543210",
  "date": "2026-03-12",
  "time": "14:00",
  "service": "haircut"
}
```
* **Sample JSON Response:**
```json
{
  "status": "confirmed",
  "booking_id": "BK_001928"
}
```
