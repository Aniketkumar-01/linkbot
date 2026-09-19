import streamlit as st
from database.db import init_db
import os

st.set_page_config(
    page_title="LinkedIn Networking Assistant",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database tables if they don't exist
init_db()

# Application Sidebar / Navigation
st.sidebar.title("LinkedIn Networking Assistant")
st.sidebar.markdown("Manage your professional network efficiently.")

pages = {
    "Overview": [
        st.Page("pages/dashboard.py", title="Dashboard", icon="📊"),
    ],
    "Candidates": [
        st.Page("pages/candidates.py", title="Candidates List", icon="👥"),
        st.Page("pages/add_candidates.py", title="Discover Candidates", icon="🚀"),
    ],
    "Networking": [
        st.Page("pages/networking.py", title="Networking Tracker", icon="📈"),
    ],
    "Configuration": [
        st.Page("pages/settings.py", title="Settings", icon="⚙️"),
    ]
}

pg = st.navigation(pages)
pg.run()
