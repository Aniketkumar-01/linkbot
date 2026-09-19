import streamlit as st
from database.db import SessionLocal
from database.models import Candidate, NetworkingStatus
from datetime import datetime
from sqlalchemy.orm import joinedload

st.title("Networking Tracker")
st.markdown("Track your manual outreach progress.")

def get_networking_data():
    with SessionLocal() as db:
        return db.query(NetworkingStatus).options(joinedload(NetworkingStatus.candidate)).all()

def update_status(status_id: int, new_status: str):
    with SessionLocal() as db:
        ns = db.query(NetworkingStatus).filter(NetworkingStatus.id == status_id).first()
        if ns:
            ns.status = new_status
            ns.last_interaction = datetime.utcnow()
            if new_status == "Follow":
                ns.date_followed = datetime.utcnow()
            elif new_status == "Connected":
                ns.date_connected = datetime.utcnow()
            elif new_status == "Messaged":
                ns.date_messaged = datetime.utcnow()
            db.commit()

statuses = get_networking_data()

if not statuses:
    st.info("No candidates in the pipeline.")
else:
    pipeline_stages = ["New", "Reviewed", "Follow", "Connect", "Messaged", "Connected", "Replied", "Archived"]
    
    cols = st.columns(len(pipeline_stages))
    
    for idx, stage in enumerate(pipeline_stages):
        with cols[idx]:
            st.markdown(f"**{stage}**")
            stage_items = [s for s in statuses if s.status == stage]
            for item in stage_items:
                with st.container(border=True):
                    st.markdown(f"**{item.candidate.name}**")
                    
                    next_stage_idx = idx + 1
                    if next_stage_idx < len(pipeline_stages):
                        next_stage = pipeline_stages[next_stage_idx]
                        if st.button(f"→ {next_stage}", key=f"move_{item.id}_{next_stage}"):
                            update_status(item.id, next_stage)
                            st.rerun()
