from database.db import init_db, SessionLocal
from database.models import Candidate, CandidateScore, NetworkingStatus, Skill
from services.data_manager import add_candidate, save_user_profile
from services.scoring import calculate_deterministic_score

def seed():
    init_db()
    
    print("Setting up User Profile...")
    save_user_profile({
        "name": "Demo User",
        "university": "Tech University",
        "technical_interests": "Python, AWS, React",
        "target_companies": "TechCorp, StartupInc"
    })
    
    demo_candidates = [
        {
            "data": {
                "name": "[DEMO DATA] Alice Engineer",
                "linkedin_url": "https://linkedin.com/in/demo-alice",
                "headline": "Backend Engineer at TechCorp",
                "company": "TechCorp",
                "job_title": "Backend Engineer",
                "location": "San Francisco, CA",
                "education": "Tech University",
                "mutual_connections": 12
            },
            "skills": ["Python", "AWS", "PostgreSQL", "Docker"]
        },
        {
            "data": {
                "name": "[DEMO DATA] Bob Manager",
                "linkedin_url": "https://linkedin.com/in/demo-bob",
                "headline": "Engineering Manager",
                "company": "OtherCorp",
                "job_title": "Engineering Manager",
                "location": "New York, NY",
                "education": "State University",
                "mutual_connections": 2
            },
            "skills": ["Leadership", "Agile"]
        },
        {
            "data": {
                "name": "[DEMO DATA] Charlie Recruiter",
                "linkedin_url": "https://linkedin.com/in/demo-charlie",
                "headline": "Technical Recruiter at StartupInc",
                "company": "StartupInc",
                "job_title": "Recruiter",
                "location": "Remote",
                "education": "Business School",
                "mutual_connections": 0
            },
            "skills": ["Sourcing", "Tech Hiring"]
        }
    ]
    
    print("Adding Candidates...")
    for c in demo_candidates:
        cid = add_candidate(c["data"], c["skills"])
        if cid:
            calculate_deterministic_score(cid)
            print(f"Added {c['data']['name']}")
            
    print("Seeding complete.")

if __name__ == "__main__":
    seed()
