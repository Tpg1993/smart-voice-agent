from app.core.agents.base import BaseAgent
from app.core.sarvam_client import SarvamClient
from app.db.redis_cache import get_session_state, update_session_state

class GeneralServiceAgent(BaseAgent):
    """
    Fallback Industry Agent for Other Service-Based Businesses.
    Handles general appointment scheduling and customer support inquiries.
    """
    def __init__(self):
        self.llm = SarvamClient()
        self.system_prompt = """
        You are a helpful customer service representative and receptionist for a service-based business.
        Your goal is to assist the caller with general inquiries, support, or scheduling an appointment.
        Be polite, helpful, and efficient.
        """
        
    async def process(self, call_id: str, user_transcript: str) -> str:
        state = get_session_state(call_id)
        
        llm_response = await self.llm.generate_response(self.system_prompt, user_transcript)
        
        update_session_state(call_id, {"last_agent": "GeneralServiceAgent", "last_response": llm_response})
        
        return llm_response
