from app.core.sarvam_client import SarvamClient
from app.db.redis_cache import get_session_state, update_session_state

class ConversationEngine:
    def __init__(self):
        self.llm = SarvamClient()
        
    async def process_turn(self, call_id: str, new_text: str) -> str:
        '''
        The "Brain" of the voice agent.
        1. Fetches history from Redis.
        2. Queries Sarvam AI.
        3. Updates Redis with the new intent state.
        4. Returns the string the TTS engine should verbally reply with.
        '''
        
        # 1. Fetch active state
        current_state = get_session_state(call_id)
        turn_count = int(current_state.get("turn_count", 0))
        
        # 2. Query Sarvam LLM
        print(f"[{call_id}] User said: {new_text}. Querying Sarvam...")
        llm_response = await self.llm.translate_intent(new_text)
        
        # 3. Update Redis cache
        update_session_state(call_id, {
            "turn_count": turn_count + 1,
            "last_response": llm_response
        })
        
        # 4. Return the synthesis payload
        return llm_response
