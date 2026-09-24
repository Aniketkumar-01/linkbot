from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

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
    connect_message: Optional[str] = None

    @field_validator("connect_message")
    @classmethod
    def truncate_connect_message(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v) > 300:
            return v[:297] + "..."
        return v

class ActionAssignment(BaseModel):
    url: str
    action: str

class ActionsResponse(BaseModel):
    assignments: List[ActionAssignment]
