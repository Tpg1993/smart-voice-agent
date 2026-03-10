from app.core.agents.base import BaseAgent
from app.core.sarvam_client import SarvamClient
from app.db.redis_cache import get_session_state, update_session_state
from app.services.integrations import check_calendar_availability, create_booking

class SalonAgent(BaseAgent):
    """
    Specialized Industry Agent for Salons & Spas.
    Knows how to ask for service types, staff, and book appointments.
    """
    def __init__(self):
        self.llm = SarvamClient()
        self.system_prompt = """
        You are a polite, professional AI receptionist for a high-end Salon.
        Your goal is to help the user book a haircut or spa service.
        Be concise and friendly.
        """
        
    async def process(self, call_id: str, user_transcript: str) -> str:
        # 1. Fetch active state (what do we know so far?)
        state = get_session_state(call_id)
        
        # 2. Add custom Salon logic (e.g. checking slots)
        if "time" in user_transcript.lower() or "slot" in user_transcript.lower():
            # Mocking a calendar check
            slots = check_calendar_availability("salon_123", "2026-03-12", "haircut")
            available = ", ".join(slots)
            user_transcript += f" [System Context: Available slots are {available}]"

        # 3. Generate response using the specialized system prompt
        llm_response = await self.llm.generate_response(self.system_prompt, user_transcript)
        
        # 4. Update state context
        update_session_state(call_id, {"last_agent": "SalonAgent", "last_response": llm_response})
        
        return llm_response
