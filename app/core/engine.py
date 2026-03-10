from app.core.agents.router import RouterAgent
from app.db.redis_cache import get_session_state, update_session_state

class ConversationEngine:
    def __init__(self):
        self.router = RouterAgent()
        
    async def process_turn(self, call_id: str, new_text: str) -> str:
        '''
        The entrypoint. It parses the global state, hands the text off
        to the Router Agent, and returns the TTS-bound synthesis payload.
        '''
        
        # 1. Fetch active state
        current_state = get_session_state(call_id)
        turn_count = int(current_state.get("turn_count", 0))
        
        # 2. Pass context to the Multi-Agent Router
        print(f"[{call_id}] User said: {new_text}. Routing...")
        agent_response = await self.router.process(call_id, new_text)
        
        # 3. Update global turn state
        update_session_state(call_id, {
            "turn_count": turn_count + 1
        })
        
        return agent_response
