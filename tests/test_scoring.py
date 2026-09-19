# pyrefly: ignore [missing-import]
import pytest
import os
from database.db import Base, engine, SessionLocal
from database.models import Candidate, Skill, UserProfile
from services.scoring import calculate_deterministic_score
from services.data_manager import save_user_profile, add_candidate

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_scoring_logic():
    # Set up user profile
    save_user_profile({
        "name": "Test User",
        "university": "Test University",
        "technical_interests": "Python, React, AWS",
        "target_companies": "Google, Microsoft"
    })
    
    # Add candidate
    data = {
        "name": "Jane Doe",
        "linkedin_url": "https://linkedin.com/in/janedoe",
        "job_title": "Backend Engineer",
        "company": "Microsoft",
        "education": "Test University",
        "mutual_connections": 5
    }
    skills = ["Python", "AWS", "Docker"]
    
    cid = add_candidate(data, skills)
    assert cid is not None
    
    score = calculate_deterministic_score(cid)
    
    assert score is not None
    assert score.role_score == 10 # Backend Engineer
    assert score.skill_score == 6 # Python, AWS
    assert score.company_score == 10 # Microsoft
    assert score.education_score == 10 # Test University
    assert score.connection_score == 3
    
    assert score.total_score == 39
    assert score.recommendation in ["CONNECT", "FOLLOW", "REVIEW", "IGNORE"]
