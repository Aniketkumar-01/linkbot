from database.models import Candidate, Skill, CandidateScore, NetworkingStatus, UserProfile
from database.db import SessionLocal

def get_user_profile():
    with SessionLocal() as db:
        return db.query(UserProfile).first()

def save_user_profile(data: dict):
    with SessionLocal() as db:
        profile = db.query(UserProfile).first()
        if not profile:
            profile = UserProfile(**data)
            db.add(profile)
        else:
            for key, value in data.items():
                setattr(profile, key, value)
        db.commit()

def add_candidate(data: dict, skills: list = None):
    with SessionLocal() as db:
        # Check if exists
        existing = db.query(Candidate).filter(Candidate.linkedin_url == data.get('linkedin_url')).first()
        if existing:
            return None # Or update
            
        candidate = Candidate(**data)
        db.add(candidate)
        db.flush() # Get ID
        
        # Add networking status
        status = NetworkingStatus(candidate_id=candidate.id)
        db.add(status)
        
        # Add skills
        if skills:
            for skill_name in skills:
                skill = Skill(candidate_id=candidate.id, name=skill_name.strip())
                db.add(skill)
                
        db.commit()
        return candidate.id

def get_candidates():
    with SessionLocal() as db:
        return db.query(Candidate).all()

def get_candidate_by_id(candidate_id: int):
    with SessionLocal() as db:
        return db.query(Candidate).filter(Candidate.id == candidate_id).first()
        
def get_candidate_score(candidate_id: int):
    with SessionLocal() as db:
        return db.query(CandidateScore).filter(CandidateScore.candidate_id == candidate_id).first()
