"""
Sidebar UI components

Copyright (c) 2025 Mattias Nyqvist
Licensed under the MIT License
"""

import streamlit as st
from version import __version__, __author__, __license__


def render_mode_selector():
    """Render main mode selector."""
    st.sidebar.subheader("Analysis Mode")
    
    mode = st.sidebar.radio(
        "What would you like to do?",
        options=['single', 'comparison', 'clause'],
        format_func=lambda x: {
            'single': '📄 Analyze One Contract',
            'comparison': '📊 Compare Two Contracts',
            'clause': '🔍 Deep Dive: Specific Clause'
        }[x],
        index=0,
        help="Choose your analysis mode"
    )
    
    return mode


def render_single_contract_options():
    """Render options for single contract analysis."""
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Analysis Detail**")
    
    analysis_detail = st.sidebar.radio(
        "Level of Detail",
        options=['full', 'quick'],
        format_func=lambda x: {
            'full': 'Full Analysis (Comprehensive)',
            'quick': 'Quick Summary (Fast)'
        }[x],
        index=0,
        help="Choose analysis depth",
        label_visibility="collapsed"
    )
    
    st.sidebar.info("💡 Upload one contract to get comprehensive risk analysis")
    
    return analysis_detail


def render_clause_selector():
    """Render clause type selector for deep dive mode."""
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Clause Selection**")
    
    from config.settings import CLAUSE_TYPES
    
    clause_type = st.sidebar.selectbox(
        "Which clause to analyze?",
        options=CLAUSE_TYPES,
        index=0,
        help="Select the specific clause type for deep analysis",
        label_visibility="collapsed"
    )
    
    st.sidebar.info(f"💡 Upload one contract to analyze the {clause_type} clause in detail")
    
    return clause_type


def render_comparison_info():
    """Render info for comparison mode."""
    st.sidebar.markdown("---")
    st.sidebar.info("💡 Upload two contracts to compare terms, risks, and clauses side-by-side")


def render_footer():
    """Render footer in sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.caption(f"**Version:** {__version__}")
    st.sidebar.caption(f"© 2025 {__author__}")
    st.sidebar.caption(f"{__license__} License")


def render_sidebar():
    """Render complete sidebar with mode-based options."""
    
    # Main mode selector
    mode = render_mode_selector()
    
    # Mode-specific options (directly under mode selector)
    analysis_detail = None
    clause_type = None
    
    if mode == 'single':
        analysis_detail = render_single_contract_options()
        
    elif mode == 'comparison':
        render_comparison_info()
        
    elif mode == 'clause':
        clause_type = render_clause_selector()
    
    # Footer (at bottom)
    render_footer()
    
    return {
        'mode': mode,
        'analysis_detail': analysis_detail,
        'clause_type': clause_type
    }


def show_welcome():
    """Show welcome screen when no contract is uploaded."""
    st.info("Upload a contract to begin analysis")
    
    st.markdown("### How It Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📄 Single Analysis")
        st.markdown("""
        - Upload one contract
        - Get full risk assessment
        - AI-powered insights
        - Export detailed report
        """)
    
    with col2:
        st.markdown("#### 📊 Comparison")
        st.markdown("""
        - Upload two contracts
        - Side-by-side comparison
        - Identify differences
        - Which is better?
        """)
    
    with col3:
        st.markdown("#### 🔍 Clause Deep Dive")
        st.markdown("""
        - Upload one contract
        - Choose specific clause
        - Detailed analysis
        - Improvement tips
        """)
    
    st.markdown("---")
    
    st.markdown("### What We Analyze")
    st.markdown("""
    **Risk Assessment:**
    - Payment terms and conditions
    - Liability clauses
    - Termination rights
    - Confidentiality obligations
    - Intellectual property rights
    
    **Red Flags:**
    - Unusual or unfavorable terms
    - Missing critical clauses
    - Ambiguous language
    - Potential legal issues
    
    **Recommendations:**
    - Suggested improvements
    - Negotiation points
    - Risk mitigation strategies
    """)