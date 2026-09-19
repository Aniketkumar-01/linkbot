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

    def extract_candidate_data(self, text: str) -> dict:
        if not self.is_configured:
            return {"error": "AI API Key is not configured. Please add AI_API_KEY to your .env file."}
        
        try:
            from google import genai
            import json
            
            client = genai.Client(api_key=self.api_key)
            
            prompt = f"""
            Extract the following candidate information from the provided text (which might be a resume, a LinkedIn profile copy, or just raw text).
            If a field is not found or not explicitly stated, return an empty string (or empty list for skills).
            Try to infer 'company' and 'job_title' from the most recent or current experience.
            
            Return exactly this JSON schema:
            {{
                "name": "string",
                "linkedin_url": "string",
                "headline": "string",
                "company": "string",
                "job_title": "string",
                "location": "string",
                "education": "string",
                "about": "string",
                "experience": "string",
                "skills": ["string"]
            }}
            
            Text:
            {text}
            """
            
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt,
                config={
                    'response_mime_type': 'application/json',
                    'temperature': 0.1
                },
            )
            
            data = json.loads(response.text)
            return data
        except Exception as e:
            return {"error": f"Failed to extract data: {str(e)}"}
