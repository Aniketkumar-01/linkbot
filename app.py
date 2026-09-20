import streamlit as st

# Must be the first Streamlit command
st.set_page_config(
    page_title="LinkBot - Free LinkedIn Networking Assistant",
    page_icon="🔗",
    layout="wide"
)

from ui.sidebar import render_sidebar
from ui.components import render_profile_preview
from ui.results_view import render_results
from core.resume_parser import process_resume
from core.github_scraper import scrape_github_profile
from core.profile_analyzer import analyze_profile_with_gemini
from core.search_engine import search_for_connections
from core.result_ranker import rank_and_score_results
from utils.helpers import is_valid_github_url

def main():
    gemini_key, serper_key = render_sidebar()
    
    st.title("🔗 LinkBot")
    st.subheader("Your AI-Powered LinkedIn Growth Assistant")
    
    st.markdown("""
    Upload your resume or provide your GitHub profile. LinkBot will analyze your skills and experience 
    to find the most relevant professionals you should connect with or follow on LinkedIn.
    """)
    
    if not gemini_key:
        st.warning("⚠️ Please enter your Gemini API Key in the sidebar to unlock intelligent analysis.")
        st.stop()

    # Input Method Selection
    def clear_results():
        if 'suggestions' in st.session_state:
            del st.session_state['suggestions']
        if 'user_profile' in st.session_state:
            del st.session_state['user_profile']

    st.markdown("Select one or more sources to build your profile:")
    col1, col2, col3 = st.columns(3)
    with col1:
        use_pdf = st.checkbox("PDF Resume", value=True, on_change=clear_results)
    with col2:
        use_github = st.checkbox("GitHub Profile", on_change=clear_results)
    with col3:
        use_linkedin = st.checkbox("LinkedIn URL", on_change=clear_results)
    
    extracted_text_parts = []
    user_linkedin_url = ""
    
    if use_pdf:
        uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"], on_change=clear_results)
        if uploaded_file is not None:
            with st.spinner("Extracting text from PDF..."):
                extracted_text_parts.append(process_resume(uploaded_file))
                
    if use_github:
        github_url = st.text_input("Enter your GitHub Profile URL", placeholder="https://github.com/username", on_change=clear_results)
        if github_url:
            if is_valid_github_url(github_url):
                with st.spinner("Scraping GitHub profile..."):
                    extracted_text_parts.append(scrape_github_profile(github_url))
            else:
                st.error("Please enter a valid GitHub profile URL.")
                
    if use_linkedin:
        linkedin_url = st.text_input("Enter your LinkedIn Profile URL", placeholder="https://linkedin.com/in/username", on_change=clear_results)
        if linkedin_url:
            user_linkedin_url = linkedin_url
            # We can't scrape LinkedIn directly, but we can tell Gemini the URL so it extracts the slug as the name
            extracted_text_parts.append(f"My LinkedIn URL is: {linkedin_url}")

    extracted_text = "\n\n---\n\n".join(extracted_text_parts) if extracted_text_parts else None

    # Process if we have text
    if extracted_text:
        st.markdown("---")
        if st.button("🚀 Analyze & Find Network", type="primary"):
            
            # Step 1: Analyze Profile
            with st.spinner("🧠 Analyzing your profile with AI..."):
                user_profile = analyze_profile_with_gemini(extracted_text, gemini_key)
                if user_linkedin_url:
                    user_profile.linkedin_url = user_linkedin_url
            
            if user_profile:
                # Store in session state to avoid re-running on tab clicks
                st.session_state['user_profile'] = user_profile
                st.success("Profile analyzed successfully!")
                
            # Step 2 & 3: Search and Rank
            if 'user_profile' in st.session_state:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                def update_progress(fraction, message):
                    progress_bar.progress(fraction)
                    status_text.text(message)
                
                status_text.text("🔍 Searching LinkedIn via web search...")
                raw_suggestions = search_for_connections(
                    st.session_state['user_profile'], 
                    serper_api_key=serper_key,
                    progress_callback=update_progress
                )
                
                progress_bar.progress(1.0)
                status_text.text("📊 Ranking and categorizing results...")
                
                final_results = rank_and_score_results(st.session_state['user_profile'], raw_suggestions, gemini_key)
                st.session_state['suggestions'] = final_results
                
                status_text.empty()
                progress_bar.empty()

    # Display Results if they exist in session state
    if 'user_profile' in st.session_state:
        st.markdown("---")
        render_profile_preview(st.session_state['user_profile'])
        
    if 'suggestions' in st.session_state:
        st.markdown("---")
        render_results(st.session_state['suggestions'])

if __name__ == "__main__":
    main()
