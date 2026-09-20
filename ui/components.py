import streamlit as st
from core.models import UserProfile, LinkedInSuggestion

def render_profile_preview(profile: UserProfile):
    """Renders a visual summary of the extracted user profile."""
    st.subheader("Your Extracted Profile")
    st.info("We'll use this information to find relevant connections.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Name:** {profile.name or 'N/A'}")
        st.markdown(f"**Headline:** {profile.headline or 'N/A'}")
        st.markdown(f"**Location:** {profile.location or 'N/A'}")
        st.markdown(f"**Experience:** {profile.experience_years} years")
        
    with col2:
        if profile.skills:
            st.markdown("**Top Skills:**")
            st.markdown(", ".join(profile.skills[:5]))
        if profile.job_titles:
            st.markdown("**Titles:**")
            st.markdown(", ".join(profile.job_titles[:3]))
        if profile.industries:
            st.markdown("**Industries:**")
            st.markdown(", ".join(profile.industries))

def render_profile_card(suggestion: LinkedInSuggestion):
    """Renders a single LinkedIn suggestion using native Streamlit layout."""
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### {suggestion.name}")
            st.caption(suggestion.title)
            st.write(suggestion.snippet)
            
            if hasattr(suggestion, 'reason') and suggestion.reason:
                st.info(f"💡 **Why connect:** {suggestion.reason}")
                
            st.link_button(f"{suggestion.action} on LinkedIn", suggestion.url, type="primary")
            
        with col2:
            st.markdown(f"**{suggestion.category}**")
            st.metric(label="Relevance", value=f"{suggestion.relevance_score}%")
