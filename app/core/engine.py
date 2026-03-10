from app.core.agents.router import RouterAgent
from app.core.security.pii_vault import PIIVault, PIIScrubber
from app.db.redis_cache import get_session_state, update_session_state

class ConversationEngine:
    def __init__(self):
        self.router = RouterAgent()
        # In production this vault would be shared state (Redis).
        # We attach it here per-engine instance for local processing.
        self.pii_vault = PIIVault()
        self.scrubber = PIIScrubber(self.pii_vault)
        
    async def process_turn(self, call_id: str, new_text: str) -> str:
        '''
        The entrypoint. It parses the global state, hands the text off
        to the Router Agent, and returns the TTS-bound synthesis payload.
        '''
        
        # 1. Fetch active state
        current_state = get_session_state(call_id)
        turn_count = int(current_state.get("turn_count", 0))
        
        # 2. REDACT PII before LLM sees it
        safe_transcript = self.scrubber.redact(new_text)
        if safe_transcript != new_text:
            print(f"[{call_id}] Security: PII Redacted from transcript.")
        
        # 3. Pass *safe* context to the Multi-Agent Router
        print(f"[{call_id}] User said: {safe_transcript}. Routing...")
        agent_response = await self.router.process(call_id, safe_transcript)
        
        # 4. RESTORE PII into the final actionable response
        final_response = self.pii_vault.restore_text(agent_response)
        
        # 5. Update global turn state
        update_session_state(call_id, {
            "turn_count": turn_count + 1
        })
        
        return final_response
