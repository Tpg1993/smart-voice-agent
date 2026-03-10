import httpx
from typing import Dict, Any
from app.config import settings

class SarvamClient:
    def __init__(self):
        self.api_key = settings.SARVAM_API_KEY
        self.base_url = settings.SARVAM_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
    async def generate_response(self, system_prompt: str, user_transcript: str) -> str:
        '''
        Generic method to call the Sarvam LLM with a specific agent's instruction.
        '''
        if not self.api_key:
            return "NO_API_KEY_CONFIGURED"
            
        async with httpx.AsyncClient() as client:
            try:
                # Example Sarvam Chat Completion payload
                # payload = {
                #     "model": "sarvam-chat",
                #     "messages": [
                #         {"role": "system", "content": system_prompt},
                #         {"role": "user", "content": user_transcript}
                #     ],
                #     "temperature": 0.3
                # }
                # response = await client.post(f"{self.base_url}/v1/chat/completions", json=payload, headers=self.headers)
                # response.raise_for_status()
                # return response.json()['choices'][0]['message']['content']
                
                return f"Mock reply to: {user_transcript}"
            
            except Exception as e:
                print(f"Error calling Sarvam: {e}")
                return "ERROR_FETCHING_INTENT"
