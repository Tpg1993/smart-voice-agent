from app.core.agents.base import BaseAgent
from app.core.sarvam_client import SarvamClient
from app.core.agents.salon_agent import SalonAgent
from app.core.agents.healthcare_agent import HealthcareAgent
from app.db.redis_cache import get_session_state, update_session_state

class RouterAgent(BaseAgent):
    """
    The Triage/Router module. It takes the very first intent from the caller,
    classifies which Industry they need, and routes the context to that Sub-Agent.
    """
    def __init__(self):
        self.llm = SarvamClient()
        self.salon_agent = SalonAgent()
        self.healthcare_agent = HealthcareAgent()
        
    async def process(self, call_id: str, user_transcript: str) -> str:
        state = get_session_state(call_id)
        routed_agent = state.get("assigned_agent")
        
        # If we already routed this call to an agent, send the turn straight to them
        if routed_agent == "salon":
            return await self.salon_agent.process(call_id, user_transcript)
        elif routed_agent == "healthcare":
            return await self.healthcare_agent.process(call_id, user_transcript)
            
        # Otherwise, this is a NEW call. We must classify the Intent.
        # In a real Saas, the 'assigned_agent' would be tied to the incoming Phone Number.
        # For this logic loop, we'll ask the LLM to classify based on transcript.
        
        system_prompt = """
        Classify the intent of the following user phrase into one of these strict categories:
        1. 'salon' (haircut, spa, nails, beauty)
        2. 'healthcare' (doctor, clinic, appointment, sick, medical)
        
        Reply ONLY with the single category word.
        """
        
        classification = await self.llm.generate_response(system_prompt, user_transcript)
        assigned_agent = classification.strip().lower()
        
        if "healthcare" in assigned_agent:
            # Route and attach state
            update_session_state(call_id, {"assigned_agent": "healthcare"})
            print(f"[{call_id}] Router classified intent as HEALTHCARE")
            return await self.healthcare_agent.process(call_id, user_transcript)
        else:
            # Default fallback to Salon
            update_session_state(call_id, {"assigned_agent": "salon"})
            print(f"[{call_id}] Router classified intent as SALON")
            return await self.salon_agent.process(call_id, user_transcript)
