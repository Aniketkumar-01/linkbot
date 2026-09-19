from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db import Base

class UserProfile(Base):
    __tablename__ = "user_profile"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="")
    university = Column(String, default="")
    degree = Column(String, default="")
    graduation_year = Column(String, default="")
    location = Column(String, default="")
    current_status = Column(String, default="")
    
    # Store lists as comma separated strings for simplicity in SQLite
    technical_interests = Column(Text, default="")
    target_job_titles = Column(Text, default="")
    target_companies = Column(Text, default="")
    target_industries = Column(Text, default="")
    networking_goals = Column(Text, default="")

class Settings(Base):
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    value = Column(String)

class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    linkedin_url = Column(String, unique=True, index=True)
    headline = Column(String, default="")
    company = Column(String, default="")
    job_title = Column(String, default="")
    location = Column(String, default="")
    education = Column(String, default="")
    experience = Column(Text, default="")
    about = Column(Text, default="")
    recent_posts = Column(Text, default="")
    mutual_connections = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    skills = relationship("Skill", back_populates="candidate", cascade="all, delete-orphan")
    score = relationship("CandidateScore", back_populates="candidate", uselist=False, cascade="all, delete-orphan")
    networking_status = relationship("NetworkingStatus", back_populates="candidate", uselist=False, cascade="all, delete-orphan")

class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    name = Column(String, index=True)
    
    candidate = relationship("Candidate", back_populates="skills")

class CandidateScore(Base):
    __tablename__ = "candidate_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    
    role_score = Column(Integer, default=0)
    skill_score = Column(Integer, default=0)
    company_score = Column(Integer, default=0)
    education_score = Column(Integer, default=0)
    career_score = Column(Integer, default=0)
    content_score = Column(Integer, default=0)
    connection_score = Column(Integer, default=0)
    
    total_score = Column(Integer, default=0)
    normalized_score = Column(Integer, default=0)
    
    recommendation = Column(String, default="REVIEW")
    explanation = Column(Text, default="")
    
    candidate = relationship("Candidate", back_populates="score")

class NetworkingStatus(Base):
    __tablename__ = "networking_status"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    
    status = Column(String, default="New") # New, Reviewed, Follow, Connect, Connected, Messaged, Replied, Archived
    date_added = Column(DateTime, default=datetime.utcnow)
    date_followed = Column(DateTime, nullable=True)
    date_connected = Column(DateTime, nullable=True)
    date_messaged = Column(DateTime, nullable=True)
    last_interaction = Column(DateTime, nullable=True)
    notes = Column(Text, default="")
    
    candidate = relationship("Candidate", back_populates="networking_status")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    style = Column(String) # Professional, Friendly, Concise
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
