import streamlit as st
from config.constants import DEFAULT_COMPOSITION, DEFAULT_CONTAMINANTS

def initialize_session_state():
    """Initialize session state variables"""
    if 'composition' not in st.session_state:
        st.session_state.composition = DEFAULT_COMPOSITION.copy()

    if 'contaminants' not in st.session_state:
        st.session_state.contaminants = DEFAULT_CONTAMINANTS.copy()

def reset_session_state():
    """Reset all session state variables to default values"""
    st.session_state.composition = DEFAULT_COMPOSITION.copy()
    st.session_state.contaminants = DEFAULT_CONTAMINANTS.copy()
    
    # Reset any other session state variables if they exist
    if 'co2_avoided' in st.session_state:
        del st.session_state.co2_avoided