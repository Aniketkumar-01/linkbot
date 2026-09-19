from services.data_manager import get_user_profile
from database.models import Candidate, CandidateScore
from utils.constants import ROLES_WEIGHTS
from utils.helpers import normalize_score
from database.db import SessionLocal

def calculate_deterministic_score(candidate_id: int):
    with SessionLocal() as db:
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if not candidate:
            return None
            
        profile = get_user_profile()
        score = CandidateScore(candidate_id=candidate.id)
        
        # Role score
        role = candidate.job_title or ""
        role_score = 0
        for key, val in ROLES_WEIGHTS.items():
            if key.lower() in role.lower():
                role_score = max(role_score, val)
        if not role_score and role: # Unknown role
            role_score = -5
        score.role_score = role_score
        
        # Skills score
        skill_score = 0
        if profile and profile.technical_interests:
            user_skills = [s.strip().lower() for s in profile.technical_interests.split(",")]
            cand_skills = [s.name.lower() for s in candidate.skills]
            for s in cand_skills:
                if s in user_skills:
                    skill_score += 3
        score.skill_score = min(skill_score, 30) # Cap at 30
        
        # Company score
        company_score = 0
        if profile and profile.target_companies and candidate.company:
            target_companies = [c.strip().lower() for c in profile.target_companies.split(",")]
            if candidate.company.lower() in target_companies:
                company_score = 10
        score.company_score = company_score
        
        # Education
        education_score = 0
        if profile and profile.university and candidate.education:
            if profile.university.lower() in candidate.education.lower():
                education_score = 10
        score.education_score = education_score
        
        # Connection score
        score.connection_score = 3 if candidate.mutual_connections and candidate.mutual_connections > 0 else 0
        
        score.total_score = score.role_score + score.skill_score + score.company_score + score.education_score + score.connection_score
        score.normalized_score = normalize_score(score.total_score, min_score=-10, max_score=80)
        
        # Basic recommendation
        if score.normalized_score > 70:
            score.recommendation = "CONNECT"
            score.explanation = "High relevance across multiple factors. Strong alignment with your goals."
        elif score.normalized_score > 40:
            score.recommendation = "FOLLOW"
            score.explanation = "Good relevance. Worth following for content and industry updates."
        elif score.normalized_score < 20:
            score.recommendation = "IGNORE"
            score.explanation = "Low relevance. Does not match your target profile."
        else:
            score.recommendation = "REVIEW"
            score.explanation = "Moderate relevance. Requires manual review."
            
        # Delete old score if exists
        db.query(CandidateScore).filter(CandidateScore.candidate_id == candidate.id).delete()
        db.add(score)
        db.commit()
        return score
