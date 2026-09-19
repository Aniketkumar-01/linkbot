import streamlit as st
from database.db import SessionLocal
from database.models import Candidate
from services.ai import AIProvider

st.title("Message Generator")

def get_candidates():
    with SessionLocal() as db:
        return db.query(Candidate).all()

candidates = get_candidates()
ai = AIProvider()

if not candidates:
    st.info("No candidates available. Add some first.")
else:
    candidate_names = {c.id: c.name for c in candidates}
    selected_id = st.selectbox("Select Candidate", options=list(candidate_names.keys()), format_func=lambda x: candidate_names[x])
    
    if selected_id:
        c = next(c for c in candidates if c.id == selected_id)
        st.subheader(f"Generate Message for {c.name}")
        
        c_info = {
            "name": c.name,
            "company": c.company,
            "job_title": c.job_title,
        }
        
        style = st.radio("Message Style", ["Professional", "Friendly", "Concise"])
        
        if st.button("Generate"):
            message = ai.generate_message(c_info, style)
            st.text_area("Generated Message", message, height=150)
            st.info("Copy this message and use it manually on LinkedIn. This tool does not send messages automatically.")
