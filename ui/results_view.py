import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from core.models import LinkedInSuggestion
from .components import render_profile_card

def render_results(suggestions: list[LinkedInSuggestion]):
    """Renders the tabbed results view for the discovered profiles."""
    if not suggestions:
        st.warning("No relevant profiles found. Try a different input or wait a moment and try again.")
        return
        
    st.header(f"Found {len(suggestions)} Potential Connections")
    
    # Extract unique categories dynamically
    categories = ["All"] + sorted(list(set(s.category for s in suggestions)))
    
    # Create tabs
    tabs = st.tabs(categories)
    
    # "All" Tab
    with tabs[0]:
        _render_suggestion_list(suggestions)
        
    # Category Tabs
    for i, category in enumerate(categories[1:], start=1):
        with tabs[i]:
            category_suggestions = [s for s in suggestions if s.category == category]
            _render_suggestion_list(category_suggestions)
            
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        _render_bulk_open_button(suggestions[:10])  # Limit to top 10 to avoid pop-up blockers going crazy
    with col2:
        _render_export_button(suggestions)

def _render_suggestion_list(suggestions: list[LinkedInSuggestion]):
    if not suggestions:
        st.info("No profiles in this category.")
        return
        
    for suggestion in suggestions:
        render_profile_card(suggestion)

def _render_export_button(suggestions: list[LinkedInSuggestion]):
    """Renders a button to download results as CSV."""
    df = pd.DataFrame([s.model_dump() for s in suggestions])
    csv = df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 Export Results as CSV",
        data=csv,
        file_name='linkbot_network_suggestions.csv',
        mime='text/csv',
    )

def _render_bulk_open_button(suggestions: list[LinkedInSuggestion]):
    """Renders a button that uses JS to open multiple tabs at once."""
    urls = [s.url for s in suggestions]
    urls_json = pd.io.json.dumps(urls)
    
    # We use a trick: render a Streamlit button that sets a session state flag,
    # and if that flag is true, we render the HTML/JS to pop the tabs.
    if st.button(f"🚀 Open Top {len(suggestions)} Profiles in Browser"):
        js_code = f"""
        <script>
            const urls = {urls_json};
            urls.forEach(url => window.open(url, '_blank'));
        </script>
        """
        components.html(js_code, height=0)
