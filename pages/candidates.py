import streamlit as st
import pandas as pd
from database.db import SessionLocal
from database.models import Candidate
from sqlalchemy.orm import joinedload

st.title("Candidates List")

def get_all_candidates():
    with SessionLocal() as db:
        return db.query(Candidate).options(joinedload(Candidate.score)).all()

candidates = get_all_candidates()

if not candidates:
    st.info("No candidates added yet.")
else:
    # Filtering
    search = st.text_input("Search by Name, Company, or Role")
    
    data = []
    for c in candidates:
        if search.lower() in c.name.lower() or search.lower() in c.company.lower() or search.lower() in c.job_title.lower():
            score_val = c.score.normalized_score if c.score else 0
            rec_val = c.score.recommendation if c.score else "N/A"
            data.append({
                "Name": c.name,
                "Company": c.company,
                "Role": c.job_title,
                "Score": score_val,
                "Recommendation": rec_val,
                "LinkedIn": c.linkedin_url
            })
            
    if data:
        df = pd.DataFrame(data)
        st.dataframe(
            df,
            column_config={
                "LinkedIn": st.column_config.LinkColumn("LinkedIn Profile")
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.warning("No matches found.")
