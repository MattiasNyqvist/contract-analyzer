"""
Sidebar UI components

Copyright (c) 2025 Mattias Nyqvist
Licensed under the MIT License
"""

import streamlit as st
from version import __version__, __author__, __license__


def render_file_upload_section():
    """Render file upload section in sidebar - NOW REMOVED."""
    # File upload moved to main area
    pass


def render_settings_section():
    """Render settings section in sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.subheader("Settings")
    
    # Language selection
    language = st.sidebar.selectbox(
        "Response Language",
        options=['en', 'sv'],
        format_func=lambda x: '🇬🇧 English' if x == 'en' else '🇸🇪 Swedish',
        index=0,
        help="Select language for AI analysis results"
    )
    
    st.session_state.language = language
    
    # Number format
    number_format = st.sidebar.radio(
        "Number Format",
        options=['swedish', 'international'],
        format_func=lambda x: 'Swedish (10 000,50)' if x == 'swedish' else 'International (10,000.50)',
        index=0,
        help="Choose number formatting style"
    )
    
    st.session_state.number_format = number_format


def render_analysis_options():
    """Render analysis options in sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.subheader("Analysis Options")
    
    # Analysis type
    analysis_type = st.sidebar.radio(
        "Analysis Type",
        options=['full', 'quick', 'specific'],
        format_func=lambda x: {
            'full': 'Full Analysis',
            'quick': 'Quick Summary',
            'specific': 'Specific Clause'
        }[x],
        index=0
    )
    
    # If specific clause selected, show clause type dropdown
    clause_type = None
    if analysis_type == 'specific':
        from config.settings import CLAUSE_TYPES
        
        clause_type = st.sidebar.selectbox(
            "Select Clause Type",
            options=CLAUSE_TYPES,
            index=0,
            help="Choose which type of clause to analyze in detail"
        )
    
    return analysis_type, clause_type


def render_comparison_mode():
    """Render comparison mode toggle."""
    st.sidebar.markdown("---")
    st.sidebar.subheader("Comparison Mode")
    
    comparison_enabled = st.sidebar.checkbox(
        "Compare Two Contracts",
        value=st.session_state.get('comparison_mode', False),
        help="Enable to compare two contracts side-by-side"
    )
    
    st.session_state.comparison_mode = comparison_enabled
    
    return comparison_enabled


def render_footer():
    """Render footer in sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Version:** {__version__}")
    st.sidebar.caption(f"© 2025 {__author__}")
    st.sidebar.caption(f"{__license__} License")


def render_sidebar():
    """Render complete sidebar."""
    # Settings
    render_settings_section()
    
    # Analysis options
    analysis_type, clause_type = render_analysis_options()
    
    # Comparison mode
    comparison_mode = render_comparison_mode()
    
    # Footer
    render_footer()
    
    return {
        'uploaded_file': None,  # Not used anymore - uploads in main area
        'analysis_type': analysis_type,
        'clause_type': clause_type,
        'comparison_mode': comparison_mode
    }


def show_welcome():
    """Show welcome screen when no contract is uploaded."""
    st.info("Upload a contract to begin analysis")
    
    st.markdown("### How It Works")
    st.markdown("""
    1. **Upload** - Upload your contract (PDF or DOCX)
    2. **Analyze** - AI analyzes risks, clauses, and terms
    3. **Review** - Get comprehensive risk assessment
    4. **Export** - Download detailed report
    """)
    
    st.markdown("### Supported Contracts")
    st.markdown("""
    - Employment agreements
    - Vendor contracts
    - Non-disclosure agreements (NDAs)
    - Service agreements
    - Partnership agreements
    - Lease agreements
    - And more...
    """)
    
    st.markdown("### What We Check")
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