import streamlit as st
import streamlit.components.v1 as components
import json
import pandas as pd
from core.models import LinkedInSuggestion

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
        _render_data_table(suggestions, "all")
        
    # Category Tabs
    for i, category in enumerate(categories[1:], start=1):
        with tabs[i]:
            category_suggestions = [s for s in suggestions if s.category == category]
            _render_data_table(category_suggestions, f"cat_{i}")
            
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        _render_bulk_open_button(suggestions[:10])  # Limit to top 10 to avoid pop-up blockers
    with col2:
        _render_export_button(suggestions)

def _render_data_table(suggestions: list[LinkedInSuggestion], key_prefix: str):
    """Renders the suggestions as an interactive Streamlit dataframe."""
    if not suggestions:
        st.info("No profiles in this category.")
        return
        
    # Prepare dataframe
    data = []
    for s in suggestions:
        data.append({
            "Name": s.name,
            "Relevance": s.relevance_score,
            "Category": s.category,
            "Job Title": s.title,
            "Action": s.action,
            "URL": s.url,
            "_raw_idx": suggestions.index(s) # Hidden reference to original object
        })
        
    df = pd.DataFrame(data)
    
    # Render interactive dataframe
    st.markdown("Select a row to view connection details and message.")
    event = st.dataframe(
        df[["Name", "Relevance", "Category", "Job Title", "Action", "URL"]],
        width='stretch',
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        key=f"df_{key_prefix}",
        column_config={
            "Relevance": st.column_config.NumberColumn(
                "Relevance (%)",
                help="Relevance score (0-100) based on how well their skills, title, and industry match your profile. Hover to sort high-to-low.",
                format="%d%%",
            ),
            "URL": st.column_config.LinkColumn(
                "LinkedIn Profile",
                display_text="Open Profile"
            ),
            "Category": st.column_config.TextColumn(
                "Category",
                help="How this person relates to your background (e.g. Same Role, Industry Peer)."
            )
        }
    )
    
    # Handle selection
    if event and event.selection and event.selection.rows:
        selected_row_idx = event.selection.rows[0]
        original_sugg = suggestions[selected_row_idx]
        
        st.markdown("### Selected Connection")
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{original_sugg.name}** - {original_sugg.title}")
                st.write(original_sugg.snippet)
                if original_sugg.reason:
                    st.info(f"💡 **Why connect:** {original_sugg.reason}")
            with col2:
                st.link_button(f"{original_sugg.action} on LinkedIn", original_sugg.url, type="primary")
            
            # Display auto-generated connect message if available
            if original_sugg.connect_message:
                if getattr(original_sugg, 'psychological_profile', None):
                    with st.expander("🧠 Deep Psychographic Insights", expanded=True):
                        st.markdown(f"**Psychological Profile:** {original_sugg.psychological_profile}")
                        st.markdown(f"**Outreach Strategy:** {original_sugg.outreach_strategy}")
                
                st.markdown("#### 💬 Auto-Generated Connect Message")
                st.code(original_sugg.connect_message, language="text")
                st.caption("Click the copy icon in the top right of the box above, then click the Open Profile button to paste it on LinkedIn!")
            elif original_sugg.relevance_score > 0: # It's a valid result but no message generated (maybe not in top 25)
                st.markdown("#### 💬 Connect Message")
                st.warning("No message generated. (Only the top 25 results get AI-generated messages to save time).")


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
    urls_json = json.dumps(urls)
    
    if st.button(f"🚀 Open Top {len(suggestions)} Profiles in Browser"):
        js_code = f"""
        <script>
            const urls = {urls_json};
            urls.forEach(url => window.open(url, '_blank'));
        </script>
        """
        components.html(js_code, height=0)
