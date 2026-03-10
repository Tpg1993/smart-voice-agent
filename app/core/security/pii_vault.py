import re
import uuid
from typing import Tuple, Dict

class PIIVault:
    """
    In-memory temporary vault for storing real PII mapped to a secure token.
    In production, this would be a highly secure Redis instance with a short TTL.
    """
    def __init__(self):
        self._vault: Dict[str, str] = {}

    def store(self, value: str) -> str:
        token = f"[PII_TOKEN_{uuid.uuid4().hex[:8].upper()}]"
        self._vault[token] = value
        return token

    def retrieve(self, token: str) -> str:
        return self._vault.get(token, token)

    def restore_text(self, text: str) -> str:
        """Finds any tokens in the text and replaces them with real vault values."""
        for token, original_value in self._vault.items():
            text = text.replace(token, original_value)
        return text

class PIIScrubber:
    """
    Responsible for identifying and extracting PII from raw text and passing it to the vault.
    """
    def __init__(self, vault: PIIVault):
        self.vault = vault
        
        # Regex patterns for basic PII. Production would use Presidio or AWS Comprehend.
        self.patterns = {
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "credit_card": r"\b(?:\d{4}[ -]?){3}\d{4}\b",
            "phone_number": r"\b\+?1?\s*\(?-*\d{3}\)?\s*-?\d{3}\s*-?\d{4}\b",
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        }

    def redact(self, text: str) -> str:
        """
        Scans text for PII patterns, stores matches in the vault, 
        and replaces the raw text with the secure token.
        """
        redacted_text = text
        for pii_type, pattern in self.patterns.items():
            matches = re.finditer(pattern, redacted_text)
            for match in matches:
                real_value = match.group(0)
                # Store in vault and get token
                token = self.vault.store(real_value)
                # Replace in text
                redacted_text = redacted_text.replace(real_value, token)
                
        return redacted_text
