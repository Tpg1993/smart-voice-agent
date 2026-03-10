from app.core.agents.base import BaseAgent
from app.core.sarvam_client import SarvamClient
from app.db.redis_cache import get_session_state, update_session_state

class HealthcareAgent(BaseAgent):
    """
    Specialized Industry Agent for Healthcare Clinics.
    Designed securely with HIPAA-compliance guidelines in mind.
    """
    def __init__(self):
        self.llm = SarvamClient()
        self.system_prompt = """
        You are a HIPAA-compliant medical receptionist.
        You can help book doctor appointments, but you must NEVER give medical advice.
        If a user asks about symptoms, ask them to consult the doctor during their visit.
        Be professional, calm, and highly secure.
        """
        
    async def process(self, call_id: str, user_transcript: str) -> str:
        state = get_session_state(call_id)
        
        # Generate strict, secure healthcare replies
        llm_response = await self.llm.generate_response(self.system_prompt, user_transcript)
        
        # Update State
        update_session_state(call_id, {"last_agent": "HealthcareAgent", "last_response": llm_response})
        
        return llm_response
