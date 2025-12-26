"""
Contract Analyzer - Main Application

AI-powered contract analysis for risk detection and clause evaluation

Copyright (c) 2025 Mattias Nyqvist
Licensed under the MIT License
"""

import streamlit as st
import os
from dotenv import load_dotenv

from version import __version__, __author__, __license__
from config.settings import APP_TITLE, APP_ICON, APP_DESCRIPTION
from utils.session_manager import init_session, reset_analysis
from ui.sidebar import render_sidebar, show_welcome
from ui.results_display import show_analysis
from modules.file_handler import save_uploaded_file
from modules.text_extractor import extract_text, clean_text
from modules.contract_analyzer import analyze_contract, get_quick_summary
from modules.risk_detector import run_automated_risk_detection
from modules.report_builder import generate_text_report, generate_html_report
from utils.validators import validate_contract_text, validate_api_key

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
init_session()

# Title and description
st.title(f"{APP_ICON} {APP_TITLE}")
st.markdown(APP_DESCRIPTION)

# Render sidebar and get options
sidebar_options = render_sidebar()

# Main content
if sidebar_options['uploaded_file'] is None:
    # Show welcome screen
    show_welcome()
    st.stop()

# Process uploaded file
uploaded_file = sidebar_options['uploaded_file']
analysis_type = sidebar_options['analysis_type']

# Save file
with st.spinner("Processing contract..."):
    file_path = save_uploaded_file(uploaded_file)
    
    # Extract text
    contract_text, error = extract_text(file_path)
    
    if error:
        st.error(f"Error extracting text: {error}")
        st.stop()
    
    # Clean text
    contract_text = clean_text(contract_text)
    
    # Validate
    is_valid, validation_error = validate_contract_text(contract_text)
    
    if not is_valid:
        st.error(validation_error)
        st.stop()
    
    # Store in session
    st.session_state.contract_text = contract_text
    st.session_state.contract_filename = uploaded_file.name
    st.session_state.contract_uploaded = True

st.success(f"Contract processed: {len(contract_text)} characters extracted")

# Analysis section
st.markdown("---")

# Get API key
api_key = os.environ.get("ANTHROPIC_API_KEY")

if not api_key:
    st.warning("⚠️ API key not configured. Set ANTHROPIC_API_KEY in .env file for AI-powered analysis.")
    st.info("Running automated rule-based analysis only...")
    use_ai = False
else:
    use_ai = True

# Analyze button
if st.button("🔍 Analyze Contract", type="primary", use_container_width=True):
    with st.spinner("Analyzing contract... This may take 30-60 seconds..."):
        
        if analysis_type == 'quick':
            # Quick summary only
            if use_ai:
                summary = get_quick_summary(st.session_state.contract_text, api_key)
                st.session_state.analysis_results = {
                    'summary': summary,
                    'overall_risk': 'UNKNOWN',
                    'risks': [],
                    'red_flags': [],
                    'missing_clauses': [],
                    'recommendations': []
                }
            else:
                st.error("Quick summary requires AI. Please configure API key.")
                st.stop()
        
        elif analysis_type == 'full':
            # Full AI analysis
            if use_ai:
                analysis = analyze_contract(
                    st.session_state.contract_text,
                    api_key,
                    st.session_state.language
                )
                
                if analysis:
                    # Enhance with automated risk detection
                    automated = run_automated_risk_detection(st.session_state.contract_text)
                    
                    # Merge results
                    if automated['risks']:
                        analysis['risks'].extend(automated['risks'])
                    if automated['missing_clauses']:
                        for clause in automated['missing_clauses']:
                            if clause not in analysis.get('missing_clauses', []):
                                analysis.setdefault('missing_clauses', []).append(clause)
                    
                    # Add automated recommendations if AI didn't provide enough
                    if len(analysis.get('recommendations', [])) < 3:
                        auto_recs = automated.get('recommendations', [])
                        for rec in auto_recs:
                            if rec not in analysis.get('recommendations', []):
                                analysis.setdefault('recommendations', []).append(rec)
                    
                    st.session_state.analysis_results = analysis
                else:
                    st.error("AI analysis failed. Please try again.")
                    st.stop()
            else:
                # Automated analysis only
                analysis = run_automated_risk_detection(st.session_state.contract_text)
                st.session_state.analysis_results = {
                    'summary': 'Automated rule-based analysis (AI analysis requires API key)',
                    'overall_risk': analysis['overall_risk'],
                    'risks': analysis['risks'],
                    'red_flags': [],
                    'missing_clauses': analysis['missing_clauses'],
                    'key_terms': [],
                    'recommendations': analysis.get('recommendations', [])
                }
        
        else:  # specific clauses
            st.info("Specific clause analysis coming soon!")
            st.stop()
        
        st.session_state.analysis_complete = True
        st.success("✅ Analysis complete!")

# Display results
if st.session_state.get('analysis_complete') and st.session_state.get('analysis_results'):
    st.markdown("---")
    show_analysis(st.session_state.analysis_results)
    
    # Export section
    st.markdown("---")
    st.subheader("Export Report")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Text report
        text_report = generate_text_report(
            st.session_state.analysis_results,
            st.session_state.contract_filename
        )
        st.download_button(
            label="📄 Download Text Report",
            data=text_report,
            file_name=f"analysis_{st.session_state.contract_filename}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        # HTML report
        html_report = generate_html_report(
            st.session_state.analysis_results,
            st.session_state.contract_filename
        )
        st.download_button(
            label="🌐 Download HTML Report",
            data=html_report,
            file_name=f"analysis_{st.session_state.contract_filename}.html",
            mime="text/html",
            use_container_width=True
        )
    
    with col3:
        st.info("PDF export coming soon")
    
    # New analysis button
    st.markdown("---")
    if st.button("🔄 Analyze New Contract"):
        reset_analysis()
        st.rerun()