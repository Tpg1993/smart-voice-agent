from app.core.agents.base import BaseAgent
from app.core.sarvam_client import SarvamClient
from app.db.redis_cache import get_session_state, update_session_state

class HotelAgent(BaseAgent):
    """
    Specialized Industry Agent for Hotels and Hospitality.
    Handles room reservations, check-in/out dates, and guest inquiries.
    """
    def __init__(self):
        self.llm = SarvamClient()
        self.system_prompt = """
        You are a polite, accommodating concierge and reservation agent for a premium hotel.
        Your goal is to help guests book rooms, check availability for specific dates, and answer amenities questions.
        Provide a hospitable and warm interaction.
        """
        
    async def process(self, call_id: str, user_transcript: str) -> str:
        state = get_session_state(call_id)
        
        llm_response = await self.llm.generate_response(self.system_prompt, user_transcript)
        
        update_session_state(call_id, {"last_agent": "HotelAgent", "last_response": llm_response})
        
        return llm_response
