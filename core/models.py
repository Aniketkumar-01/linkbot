from typing import List, Optional
from pydantic import BaseModel, Field

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
    category: str = "Unknown"
    action: str = "Connect"

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        return value

class ActionAssignment(BaseModel):
    url: str
    action: str

class ActionsResponse(BaseModel):
    assignments: List[ActionAssignment]
