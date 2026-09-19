import os
from dotenv import load_dotenv

load_dotenv()

class AIProvider:
    def __init__(self):
        self.api_key = os.environ.get("AI_API_KEY")
        self.provider = os.environ.get("AI_PROVIDER")
        self.is_configured = bool(self.api_key)
        
    def generate_message(self, candidate_info: dict, style: str) -> str:
        if not self.is_configured:
            # Deterministic fallback
            name = candidate_info.get("name", "there").split()[0]
            if style == "Friendly":
                return f"Hi {name}, came across your profile and found your work interesting! Would love to connect and follow your journey."
            elif style == "Concise":
                return f"Hi {name}, I'm expanding my network in this space. Would be great to connect."
            else:
                return f"Hi {name}, I noticed your experience in the industry and would like to add you to my professional network. Looking forward to connecting."
        
        # If configured, we would call the LLM API here.
        # For simplicity and zero cost without an API key, we just return the deterministic string.
        # This can be expanded to use google-genai or openai.
        return f"[AI Generated - {style}] Hi {candidate_info.get('name', 'there')}, ..."
