import streamlit as st
import pandas as pd
from database.db import SessionLocal
from database.models import Candidate, CandidateScore, NetworkingStatus

st.title("Dashboard")

def load_data():
    with SessionLocal() as db:
        candidates = db.query(Candidate).count()
        scores = db.query(CandidateScore).all()
        statuses = db.query(NetworkingStatus).all()
        return candidates, scores, statuses

candidates_count, scores, statuses = load_data()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Candidates", candidates_count)

high_relevance = sum(1 for s in scores if s.normalized_score > 70)
col2.metric("High Relevance (>70)", high_relevance)

connects = sum(1 for s in scores if s.recommendation == "CONNECT")
follows = sum(1 for s in scores if s.recommendation == "FOLLOW")
col3.metric("Recommended Connects", connects)
col4.metric("Recommended Follows", follows)

st.divider()

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Score Distribution")
    if scores:
        df_scores = pd.DataFrame([s.normalized_score for s in scores], columns=["Score"])
        st.bar_chart(df_scores, height=300)
    else:
        st.info("No candidates scored yet.")

with col_chart2:
    st.subheader("Networking Pipeline")
    if statuses:
        status_counts = {}
        for s in statuses:
            status_counts[s.status] = status_counts.get(s.status, 0) + 1
        df_status = pd.DataFrame(list(status_counts.items()), columns=["Status", "Count"]).set_index("Status")
        st.bar_chart(df_status, height=300)
    else:
        st.info("No pipeline data yet.")
