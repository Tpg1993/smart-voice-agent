from app.core.agents.base import BaseAgent
from app.core.sarvam_client import SarvamClient
from app.db.redis_cache import get_session_state, update_session_state

class EducationAgent(BaseAgent):
    """
    Specialized Industry Agent for Schools and Colleges.
    Handles student visits, application consultations, and general campus inquiries.
    """
    def __init__(self):
        self.llm = SarvamClient()
        self.system_prompt = """
        You are a welcoming and knowledgeable admissions assistant for an educational institution.
        Your goal is to help prospective students schedule campus visits or answer application queries.
        Be encouraging, polite, and clear about deadlines.
        """
        
    async def process(self, call_id: str, user_transcript: str) -> str:
        state = get_session_state(call_id)
        
        llm_response = await self.llm.generate_response(self.system_prompt, user_transcript)
        
        update_session_state(call_id, {"last_agent": "EducationAgent", "last_response": llm_response})
        
        return llm_response
