import pandas as pd
from services.data_manager import add_candidate
from services.scoring import calculate_deterministic_score
import logging

def import_csv(file) -> dict:
    try:
        df = pd.read_csv(file)
        success = 0
        skipped = 0
        for _, row in df.iterrows():
            data = {
                "name": row.get("name", ""),
                "linkedin_url": row.get("linkedin_url", ""),
                "headline": row.get("headline", ""),
                "company": row.get("company", ""),
                "job_title": row.get("job_title", ""),
                "location": row.get("location", ""),
                "education": row.get("education", ""),
                "experience": str(row.get("experience", "")),
                "about": str(row.get("about", "")),
                "mutual_connections": int(row.get("mutual_connections", 0)) if pd.notna(row.get("mutual_connections")) else 0,
            }
            if not data["linkedin_url"]:
                skipped += 1
                continue
                
            skills = str(row.get("skills", "")).split(",") if pd.notna(row.get("skills")) else []
            candidate_id = add_candidate(data, skills)
            
            if candidate_id:
                calculate_deterministic_score(candidate_id)
                success += 1
            else:
                skipped += 1
                
        return {"success": success, "skipped": skipped}
    except Exception as e:
        logging.error(f"CSV Import Error: {e}")
        return {"error": str(e)}

def export_candidates_to_csv() -> pd.DataFrame:
    from database.models import Candidate
    from database.db import SessionLocal
    with SessionLocal() as db:
        candidates = db.query(Candidate).all()
        data = []
        for c in candidates:
            data.append({
                "id": c.id,
                "name": c.name,
                "linkedin_url": c.linkedin_url,
                "headline": c.headline,
                "company": c.company,
                "job_title": c.job_title,
                "location": c.location
            })
        return pd.DataFrame(data)
