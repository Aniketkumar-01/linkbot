import streamlit as st
from database.db import init_db
import os

st.set_page_config(
    page_title="LinkedIn Networking Assistant",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
@st.cache_resource
def setup_db():
    init_db()

setup_db()

# Application Sidebar / Navigation
st.sidebar.title("LinkedIn Networking Assistant")
st.sidebar.markdown("Manage your professional network efficiently.")

pages = {
    "Overview": [
        st.Page("pages/dashboard.py", title="Dashboard", icon="📊"),
        st.Page("pages/recommendations.py", title="Recommendations", icon="💡"),
    ],
    "Candidates": [
        st.Page("pages/candidates.py", title="Candidates List", icon="👥"),
        st.Page("pages/add_candidates.py", title="Add Candidates", icon="➕"),
    ],
    "Networking": [
        st.Page("pages/networking.py", title="Networking Tracker", icon="📈"),
        st.Page("pages/messages.py", title="Messages", icon="✉️"),
    ],
    "Configuration": [
        st.Page("pages/settings.py", title="Settings", icon="⚙️"),
        st.Page("pages/data.py", title="Data Management", icon="💾"),
    ]
}

pg = st.navigation(pages)
pg.run()
