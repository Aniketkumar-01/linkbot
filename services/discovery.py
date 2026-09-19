import json
from services.data_manager import get_user_profile
from services.ai import AIProvider
from duckduckgo_search import DDGS
from database.db import SessionLocal
from database.models import Candidate, Skill

def discover_candidates():
    profile = get_user_profile()
    if not profile or not profile.target_job_titles:
        return {"error": "Please set up your profile and Target Job Titles in Settings first."}
    
    # Formulate query
    roles = [r.strip() for r in profile.target_job_titles.split(",") if r.strip()]
    skills = [s.strip() for s in profile.technical_interests.split(",") if s.strip()] if profile.technical_interests else []
    
    if not roles:
        return {"error": "Please configure Target Job Titles in Settings."}
        
    role_q = " OR ".join([f'"{r}"' for r in roles[:2]])
    skill_q = " OR ".join([f'"{s}"' for s in skills[:2]])
    
    query = f"site:linkedin.com/in/ ({role_q})"
    if skill_q:
        query += f" ({skill_q})"
        
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=15):
                results.append(r)
    except Exception as e:
        return {"error": f"Search engine failed: {str(e)}"}
        
    if not results:
        return {"error": f"No profiles found for query: {query}"}
        
    # Use AI to parse the DDG results into structured candidates
    ai = AIProvider()
    if not ai.is_configured:
        return {"error": "AI API Key is required for Auto-Discovery (configure in .env)."}
        
    prompt = f"""
    I have a list of search engine snippets of LinkedIn profiles.
    Extract the candidate information from these snippets into a JSON array of objects.
    Clean up the names (remove 'LinkedIn', 'Profiles', etc.).
    
    JSON Schema for the output array:
    [
        {{
            "name": "string",
            "job_title": "string",
            "company": "string",
            "location": "string",
            "skills": ["string"],
            "linkedin_url": "string"
        }}
    ]
    
    Snippets:
    {json.dumps(results)}
    """
    
    try:
        from google import genai
        client = genai.Client(api_key=ai.api_key)
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
                'temperature': 0.1
            },
        )
        candidates_data = json.loads(response.text)
    except Exception as e:
        return {"error": f"AI Parsing failed: {str(e)}"}
        
    # Save to DB
    saved_count = 0
    with SessionLocal() as db:
        for c_data in candidates_data:
            url = c_data.get('linkedin_url', '')
            if not url or "linkedin.com/in/" not in url:
                continue
            
            # Check if exists
            existing = db.query(Candidate).filter(Candidate.linkedin_url == url).first()
            if existing:
                continue
                
            new_cand = Candidate(
                name=c_data.get('name', 'Unknown'),
                job_title=c_data.get('job_title', ''),
                company=c_data.get('company', ''),
                location=c_data.get('location', ''),
                linkedin_url=url,
                source="Auto-Discovery"
            )
            
            skills_list = c_data.get('skills', [])
            for s in skills_list:
                new_cand.skills.append(Skill(name=s))
                
            db.add(new_cand)
            saved_count += 1
            
        db.commit()
        
    # Trigger deterministic scoring for new candidates
    from services.scoring import calculate_deterministic_score
    from sqlalchemy.orm import joinedload
    with SessionLocal() as db:
        new_cands = db.query(Candidate).options(joinedload(Candidate.score)).all()
        for c in new_cands:
            if not c.score:
                calculate_deterministic_score(c.id)
            
    return {"success": True, "count": saved_count}
