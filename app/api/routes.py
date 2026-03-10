import base64
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.core.engine import ConversationEngine
from app.services.speech import SpeechService
from app.core.security.auth import Token, create_access_token, get_current_user, get_password_hash, verify_password
from datetime import timedelta

import os

router = APIRouter()
speech_service = SpeechService()
engine = ConversationEngine()

# Mock user database for JWT token demonstration. 
# In production, query your PostgreSQL database.
admin_password = os.getenv("ADMIN_PASSWORD", "secret123")
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": get_password_hash(admin_password),
    }
}

@router.post("/auth/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    if not verify_password(form_data.password, user_dict["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user_dict["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/call/inbound")
async def handle_inbound_call(request: Request):
    """
    Webhook triggered by Telephony provider (Twilio/Asterisk) when a call starts.
    Returns TwiML / XML instructing it to connect the audio stream to our WebSocket.
    """
    form_data = await request.form()
    call_id = form_data.get("CallSid", "CA_TEST_12345")
    
    # Dynamically build the WebSocket URL based on the incoming request Host
    protocol = "wss" if request.headers.get("x-forwarded-proto", request.url.scheme) == "https" else "ws"
    host = request.headers.get("host")
    ws_url = f"{protocol}://{host}/api/v1/ws/stream-audio/{call_id}"
    
    xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect>
        <Stream url="{ws_url}" />
    </Connect>
</Response>"""
    return PlainTextResponse(content=xml_response, media_type="text/xml")

@router.post("/call/outbound")
async def trigger_outbound_call(request: Request, current_user: dict = Depends(get_current_user)):
    """
    Internal endpoint triggered by the CRM to out-dial a user.
    PROTECTED: Requires a valid JWT Bearer token via the Authorization header.
    """
    form_data = await request.form()
    customer_number = form_data.get("customer_number")
    
    # Trigger Telephony Edge API (e.g., Twilio Client) here
    return {
        "status": "success", 
        "message": f"Outbound call triggered for {customer_number}", 
        "authorized_user": current_user.username
    }


@router.websocket("/ws/stream-audio/{call_id}")
async def stream_audio(websocket: WebSocket, call_id: str):
    """
    Handles exactly the bidirectional, real-time chunked audio communication between
    the caller and the localized Core Agent Engine.
    """
    await websocket.accept()
    print(f"Call {call_id} connected to real-time audio stream.")
    
    try:
        while True:
            # 1. Receive raw audio chunk from Twilio/Asterisk
            audio_json = await websocket.receive_json()
            
            # Extract basic payload assuming a Twilio Media Stream payload
            event = audio_json.get("event")
            if event == "media":
                payload_b64 = audio_json["media"]["payload"]
                audio_bytes = base64.b64decode(payload_b64)
                
                # 2. Sent audio bytes to ASR (Speech-to-Text)
                print(f"[{call_id}] Received audio chunk. Transcribing...")
                text_input = await speech_service.transcribe_audio(audio_bytes)
                
                if text_input and text_input != "ERROR_IN_TRANSCRIPTION":
                    # 3. Pass text to Core LLM Engine
                    llm_response = await engine.process_turn(call_id, text_input)
                    
                    # 4. Convert response text back to Speech (TTS)
                    print(f"[{call_id}] Generating reply audio...")
                    response_audio_bytes = await speech_service.synthesize_speech(llm_response)
                    
                    if response_audio_bytes:
                        # 5. Stream synthesized audio bytes back to caller
                        outbound_b64 = base64.b64encode(response_audio_bytes).decode('utf-8')
                        await websocket.send_json({
                            "event": "media",
                            "media": {
                                "track": "outbound",
                                "payload": outbound_b64
                            }
                        })
            elif event == "stop":
                break
                
    except WebSocketDisconnect:
        print(f"Call {call_id} disconnected from stream.")
        # Trigger post-call integrations (summary generation, DB saving)
