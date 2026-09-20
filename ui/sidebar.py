import streamlit as st

def render_sidebar():
    """Renders the application sidebar for settings and API keys."""
    st.sidebar.title("🔗 LinkBot Settings")
    st.sidebar.markdown("---")
    
    st.sidebar.header("API Keys")
    st.sidebar.markdown(
        "LinkBot requires a **Google Gemini API Key** for intelligent profile analysis. "
        "[Get a free key here](https://aistudio.google.com/)."
    )
    
    # Try to load from Streamlit secrets first, fallback to user input
    default_gemini_key = ""
    default_serper_key = ""
    try:
        default_gemini_key = st.secrets.get("GEMINI_API_KEY", "")
        default_serper_key = st.secrets.get("SERPER_API_KEY", "")
    except Exception:
        pass

    gemini_key = st.sidebar.text_input(
        "Gemini API Key", 
        value=default_gemini_key, 
        type="password",
        help="Used to analyze your resume/GitHub."
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "**(Optional)** For better search results, you can provide a Serper.dev API key. "
        "Otherwise, DuckDuckGo (free) is used."
    )
    serper_key = st.sidebar.text_input(
        "Serper API Key (Optional)", 
        value=default_serper_key, 
        type="password"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.header("About LinkBot")
    st.sidebar.info(
        "LinkBot is a free, open-source tool that helps you grow your LinkedIn network "
        "by finding relevant professionals based on your resume and skills."
    )
    st.sidebar.markdown("⚠️ **Note:** Always review profiles before connecting.")
    
    return gemini_key, serper_key
