import streamlit as st
from database.db import SessionLocal
from database.models import Candidate, CandidateScore
from services.ai import AIProvider

st.title("Recommendations")

def get_scored_candidates():
    with SessionLocal() as db:
        return db.query(Candidate).join(CandidateScore).all()

candidates = get_scored_candidates()

if not candidates:
    st.info("No candidates have been scored yet.")
else:
    filter_rec = st.selectbox("Filter by Recommendation", ["ALL", "CONNECT", "FOLLOW", "REVIEW", "IGNORE"])
    
    for c in candidates:
        if filter_rec != "ALL" and c.score.recommendation != filter_rec:
            continue
            
        with st.container():
            st.markdown(f"### {c.name}")
            st.markdown(f"**{c.job_title} @ {c.company}**")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"**Relevance Score:** {c.score.normalized_score}/100")
                skills_str = " • ".join([s.name for s in c.skills])
                if skills_str:
                    st.markdown(f"**Skills:** {skills_str}")
                st.markdown(f"**Explanation:** {c.score.explanation}")
                
            with col2:
                rec_color = "green" if c.score.recommendation == "CONNECT" else "blue" if c.score.recommendation == "FOLLOW" else "grey"
                st.markdown(f"**Recommendation:** :{rec_color}[{c.score.recommendation}]")
                st.link_button("Open LinkedIn Profile", c.linkedin_url)
                
            with st.expander("View Score Breakdown"):
                st.text(f"Role relevance       +{c.score.role_score}")
                st.text(f"Skill overlap        +{c.score.skill_score}")
                st.text(f"Company relevance    +{c.score.company_score}")
                st.text(f"Education            +{c.score.education_score}")
                st.text(f"Connection logic     +{c.score.connection_score}")
                st.text("---------------------------------")
                st.text(f"TOTAL (Raw)          {c.score.total_score}")
                
            st.divider()
