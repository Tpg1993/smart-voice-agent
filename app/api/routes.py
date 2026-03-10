import base64
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import PlainTextResponse
from app.core.engine import ConversationEngine
from app.services.speech import SpeechService

router = APIRouter()
speech_service = SpeechService()
engine = ConversationEngine()

@router.post("/call/inbound")
async def handle_inbound_call(request: Request):
    """
    Webhook triggered by Telephony provider (Twilio/Asterisk) when a call starts.
    Returns TwiML / XML instructing it to connect the audio stream to our WebSocket.
    """
    form_data = await request.form()
    call_id = form_data.get("CallSid", "CA_TEST_12345")
    
    # In production, replace the host domain dynamically
    ws_url = f"wss://your-domain.ngrok.io/api/v1/ws/stream-audio/{call_id}"
    
    xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect>
        <Stream url="{ws_url}" />
    </Connect>
</Response>"""
    return PlainTextResponse(content=xml_response, media_type="text/xml")


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
