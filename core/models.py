from pydantic import BaseModel, Field
from typing import List, Optional

class UserProfile(BaseModel):
    name: str = ""
    headline: str = ""
    skills: List[str] = Field(default_factory=list)
    job_titles: List[str] = Field(default_factory=list)
    industries: List[str] = Field(default_factory=list)
    experience_years: int = 0
    education: List[str] = Field(default_factory=list)
    location: str = ""
    interests: List[str] = Field(default_factory=list)
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None

class LinkedInSuggestion(BaseModel):
    name: str
    title: str
    url: str
    snippet: str
    relevance_score: float = 0.0
    category: str = "Unknown"
    reason: str = ""
    action: str = "Connect"
    connect_message: str = ""
    psychological_profile: str = ""
    outreach_strategy: str = ""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        return value

    def __init__(self, **data):
        super().__init__(**data)
        # Enforce LinkedIn connection note limit
        if len(self.connect_message) > 300:
            self.connect_message = self.connect_message[:297] + "..."
