from app.core.agents.base import BaseAgent
from app.core.sarvam_client import SarvamClient
from app.core.agents.salon_agent import SalonAgent
from app.core.agents.healthcare_agent import HealthcareAgent
from app.core.agents.education_agent import EducationAgent
from app.core.agents.hotel_agent import HotelAgent
from app.core.agents.real_estate_agent import RealEstateAgent
from app.core.agents.general_service_agent import GeneralServiceAgent
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
        self.education_agent = EducationAgent()
        self.hotel_agent = HotelAgent()
        self.real_estate_agent = RealEstateAgent()
        self.general_agent = GeneralServiceAgent()
        
    async def process(self, call_id: str, user_transcript: str) -> str:
        state = get_session_state(call_id)
        routed_agent = state.get("assigned_agent")
        
        # If we already routed this call to an agent, send the turn straight to them
        if routed_agent == "salon":
            return await self.salon_agent.process(call_id, user_transcript)
        elif routed_agent == "healthcare":
            return await self.healthcare_agent.process(call_id, user_transcript)
        elif routed_agent == "education":
            return await self.education_agent.process(call_id, user_transcript)
        elif routed_agent == "hotel":
            return await self.hotel_agent.process(call_id, user_transcript)
        elif routed_agent == "real_estate":
            return await self.real_estate_agent.process(call_id, user_transcript)
        elif routed_agent == "general":
            return await self.general_agent.process(call_id, user_transcript)
            
        # Otherwise, this is a NEW call. We must classify the Intent.
        # In a real Saas, the 'assigned_agent' would be tied to the incoming Phone Number.
        # For this logic loop, we'll ask the LLM to classify based on transcript.
        
        system_prompt = """
        Classify the intent of the following user phrase into one of these strict categories:
        1. 'salon' (haircut, spa, nails, beauty)
        2. 'healthcare' (doctor, clinic, appointment, sick, medical)
        3. 'education' (school, college, campus tour, admission, degree)
        4. 'hotel' (room, reservation, booking, stay, concierge)
        5. 'real_estate' (property, site visit, rent, buyer, broker)
        6. 'general' (any other service request or unknown)
        
        Reply ONLY with the single category word.
        """
        
        classification = await self.llm.generate_response(system_prompt, user_transcript)
        assigned_agent = classification.strip().lower()
        
        if "healthcare" in assigned_agent:
            update_session_state(call_id, {"assigned_agent": "healthcare"})
            print(f"[{call_id}] Router classified intent as HEALTHCARE")
            return await self.healthcare_agent.process(call_id, user_transcript)
        elif "education" in assigned_agent:
            update_session_state(call_id, {"assigned_agent": "education"})
            print(f"[{call_id}] Router classified intent as EDUCATION")
            return await self.education_agent.process(call_id, user_transcript)
        elif "hotel" in assigned_agent:
            update_session_state(call_id, {"assigned_agent": "hotel"})
            print(f"[{call_id}] Router classified intent as HOTEL")
            return await self.hotel_agent.process(call_id, user_transcript)
        elif "real_estate" in assigned_agent or "real estate" in assigned_agent:
            update_session_state(call_id, {"assigned_agent": "real_estate"})
            print(f"[{call_id}] Router classified intent as REAL ESTATE")
            return await self.real_estate_agent.process(call_id, user_transcript)
        elif "salon" in assigned_agent:
            update_session_state(call_id, {"assigned_agent": "salon"})
            print(f"[{call_id}] Router classified intent as SALON")
            return await self.salon_agent.process(call_id, user_transcript)
        else:
            # Default fallback
            update_session_state(call_id, {"assigned_agent": "general"})
            print(f"[{call_id}] Router classified intent as GENERAL SERVICE")
            return await self.general_agent.process(call_id, user_transcript)
