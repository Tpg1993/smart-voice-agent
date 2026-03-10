from app.core.agents.base import BaseAgent
from app.core.sarvam_client import SarvamClient
from app.db.redis_cache import get_session_state, update_session_state

class RealEstateAgent(BaseAgent):
    """
    Specialized Industry Agent for Real Estate.
    Handles site visit scheduling and initial buyer/renter inquiries.
    """
    def __init__(self):
        self.llm = SarvamClient()
        self.system_prompt = """
        You are a professional real estate assistant.
        Your primary goal is to schedule property site visits and collect basic requirements from buyers or renters.
        Ask clarifying questions about their budget or preferred areas if they are unsure. Be professional and persuasive.
        """
        
    async def process(self, call_id: str, user_transcript: str) -> str:
        state = get_session_state(call_id)
        
        llm_response = await self.llm.generate_response(self.system_prompt, user_transcript)
        
        update_session_state(call_id, {"last_agent": "RealEstateAgent", "last_response": llm_response})
        
        return llm_response
