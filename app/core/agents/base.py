from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """
    Abstract Base Class for all conversational agents in the multi-agent system.
    """
    
    @abstractmethod
    async def process(self, call_id: str, user_transcript: str) -> str:
        """
        Process the user's input and return a synthesized string response.
        Must be implemented by all Industry-Specific Agents and the Router.
        """
        pass
