# Smart Voice Agent

A highly scalable, multi-agent AI voice receptionist system designed to handle inbound and outbound telephone calls using an LLM (Sarvam AI), FastAPI, WebSocket streaming, and Local DB storage.

## Project Documentation
Before diving into the codebase, please review the complete system architecture and data flows in the `documentation/` folder:
1. `8_High_Level_Design.md`: Core system components and data pipeline.
2. `3_Architecture_Diagram.md`: Visual Mermaid graph of the infrastructure.
3. `9_Low_Level_Design.md`: Microservice specifications and DB schema.
4. `10_API_Postman_Collection.md`: WebSocket and REST Webhook contracts.
5. `11_Integration_Tools.md`: Customizing the CRM tool calls.

---

## Local Development Setup

To run this backend locally, you will need Docker (for the PostgreSQL and Redis containers) and Python 3.9+.

### 1. Configure the Environment
You must configure your `.env` file before booting the system. The `.env` file securely stores your passwords and API tokens and is permanently ignored by Git.

1. Copy the example file to a real `.env` file:
   ```bash
   cp .env.example .env
   ```
2. **Generate a Secure JWT Secret:** The API relies on a cryptographically secure 256-bit symmetric key to mint JSON Web Tokens for the `/call/outbound` webhook. Run this Python command in your terminal to generate a secure random token:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
3. Paste the resulting 64-character hexadecimal string into the `JWT_SECRET_KEY` variable inside your `.env` file. Fill out the rest of the database passwords and your Sarvam API key.

### 2. Start External Services
Boot up the local PostgreSQL database and Redis Cache:
```bash
docker-compose up -d
```

### 3. Start the Python Backend
Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
```

Finally, run the FastAPI core engine:
```bash
uvicorn app.api.routes:router --reload --port 8000
```