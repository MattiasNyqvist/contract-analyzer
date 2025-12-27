"""
Session state management

Copyright (c) 2025 Mattias Nyqvist
Licensed under the MIT License
"""

import streamlit as st


def init_session():
    """Initialize all session state variables."""
    
    # File and contract data
    if 'contract_uploaded' not in st.session_state:
        st.session_state.contract_uploaded = False
    
    if 'contract_text' not in st.session_state:
        st.session_state.contract_text = None
    
    if 'contract_filename' not in st.session_state:
        st.session_state.contract_filename = None
    
    if 'contract1_file' not in st.session_state:
        st.session_state.contract1_file = None
    
    # Analysis results
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    
    # Clause analysis
    if 'clause_results' not in st.session_state:
        st.session_state.clause_results = None
    
    # Comparison mode
    if 'comparison_mode' not in st.session_state:
        st.session_state.comparison_mode = False
    
    if 'contract2_file' not in st.session_state:
        st.session_state.contract2_file = None
    
    if 'contract2_text' not in st.session_state:
        st.session_state.contract2_text = None
    
    if 'contract2_filename' not in st.session_state:
        st.session_state.contract2_filename = None
    
    if 'analysis2_results' not in st.session_state:
        st.session_state.analysis2_results = None
    
    if 'comparison_results' not in st.session_state:
        st.session_state.comparison_results = None
    
    # User preferences - ALWAYS ENGLISH
    st.session_state.language = 'en'
    st.session_state.number_format = 'international'


def reset_analysis():
    """Reset analysis-related session state."""
    st.session_state.contract_uploaded = False
    st.session_state.contract_text = None
    st.session_state.contract_filename = None
    st.session_state.analysis_results = None
    st.session_state.analysis_complete = False
    st.session_state.clause_results = None
    
    # Reset comparison
    st.session_state.contract1_file = None
    st.session_state.contract2_file = None
    st.session_state.contract2_text = None
    st.session_state.contract2_filename = None
    st.session_state.analysis2_results = None
    st.session_state.comparison_results = None
    st.session_state.comparison_mode = False


def reset_comparison():
    """Reset comparison-related session state."""
    st.session_state.comparison_mode = False
    st.session_state.contract2_file = None
    st.session_state.contract2_text = None
    st.session_state.contract2_filename = None
    st.session_state.analysis2_results = None
    st.session_state.comparison_results = None