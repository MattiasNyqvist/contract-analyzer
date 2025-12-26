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
from ui.comparison_view import show_comparison_results
from ui.clause_view import show_clause_analysis
from modules.file_handler import save_uploaded_file
from modules.text_extractor import extract_text, clean_text
from modules.contract_analyzer import analyze_contract, get_quick_summary
from modules.risk_detector import run_automated_risk_detection
from modules.contract_comparator import compare_contracts
from modules.clause_finder import analyze_specific_clause
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

# Check if comparison mode is enabled
comparison_mode = sidebar_options['comparison_mode']
analysis_type = sidebar_options['analysis_type']
clause_type = sidebar_options['clause_type']

# Main content - File Upload
st.markdown("---")

if comparison_mode:
    st.subheader("📊 Upload Contracts for Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 Contract 1")
        uploaded_file1 = st.file_uploader(
            "First Contract",
            type=['pdf', 'docx', 'doc'],
            help="Upload first contract",
            key="contract1_uploader"
        )
    
    with col2:
        st.markdown("### 📄 Contract 2")
        uploaded_file2 = st.file_uploader(
            "Second Contract",
            type=['pdf', 'docx', 'doc'],
            help="Upload second contract to compare",
            key="contract2_uploader"
        )
    
    # Check if both uploaded
    if uploaded_file1 is None or uploaded_file2 is None:
        st.info("👆 Please upload both contracts to enable comparison")
        show_welcome()
        st.stop()
    
    # Store in session
    st.session_state.contract1_file = uploaded_file1
    st.session_state.contract2_file = uploaded_file2

else:
    # Single contract mode
    st.subheader("📄 Upload Contract")
    
    uploaded_file = st.file_uploader(
        "Contract Document",
        type=['pdf', 'docx', 'doc'],
        help="Upload PDF or DOCX contract",
        key="single_contract_uploader"
    )
    
    if uploaded_file is None:
        show_welcome()
        st.stop()
    
    st.session_state.contract1_file = uploaded_file

# Process uploaded file(s)
st.markdown("---")

with st.spinner("Processing contract(s)..."):
    # Process first contract
    file_path1 = save_uploaded_file(st.session_state.contract1_file)
    contract1_text, error1 = extract_text(file_path1)
    
    if error1:
        st.error(f"Error extracting Contract 1: {error1}")
        st.stop()
    
    contract1_text = clean_text(contract1_text)
    is_valid1, validation_error1 = validate_contract_text(contract1_text)
    
    if not is_valid1:
        st.error(f"Contract 1: {validation_error1}")
        st.stop()
    
    st.session_state.contract_text = contract1_text
    st.session_state.contract_filename = st.session_state.contract1_file.name
    st.session_state.contract_uploaded = True
    
    # Show success messages
    if comparison_mode:
        col1_msg, col2_msg = st.columns(2)
        col1_msg.success(f"✅ Contract 1: {len(contract1_text)} characters extracted")
    else:
        st.success(f"✅ Contract processed: {len(contract1_text)} characters extracted")
    
    # Process second contract if comparison mode
    if comparison_mode:
        file_path2 = save_uploaded_file(st.session_state.contract2_file)
        contract2_text, error2 = extract_text(file_path2)
        
        if error2:
            st.error(f"Error extracting Contract 2: {error2}")
            st.stop()
        
        contract2_text = clean_text(contract2_text)
        is_valid2, validation_error2 = validate_contract_text(contract2_text)
        
        if not is_valid2:
            st.error(f"Contract 2: {validation_error2}")
            st.stop()
        
        st.session_state.contract2_text = contract2_text
        st.session_state.contract2_filename = st.session_state.contract2_file.name
        
        col2_msg.success(f"✅ Contract 2: {len(contract2_text)} characters extracted")

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
if comparison_mode:
    analyze_label = "🔍 Compare Contracts"
elif analysis_type == 'specific':
    analyze_label = f"🔍 Analyze {clause_type} Clause"
else:
    analyze_label = "🔍 Analyze Contract"

if st.button(analyze_label, type="primary", use_container_width=True):
    with st.spinner("Analyzing contract(s)... This may take 30-60 seconds..."):
        
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
            # Analyze first contract
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
            
            # If comparison mode, analyze second contract
            if comparison_mode and st.session_state.get('contract2_text'):
                st.info("Analyzing second contract...")
                
                if use_ai:
                    analysis2 = analyze_contract(
                        st.session_state.contract2_text,
                        api_key,
                        st.session_state.language
                    )
                    
                    if analysis2:
                        automated2 = run_automated_risk_detection(st.session_state.contract2_text)
                        
                        if automated2['risks']:
                            analysis2['risks'].extend(automated2['risks'])
                        if automated2['missing_clauses']:
                            for clause in automated2['missing_clauses']:
                                if clause not in analysis2.get('missing_clauses', []):
                                    analysis2.setdefault('missing_clauses', []).append(clause)
                        
                        if len(analysis2.get('recommendations', [])) < 3:
                            auto_recs2 = automated2.get('recommendations', [])
                            for rec in auto_recs2:
                                if rec not in analysis2.get('recommendations', []):
                                    analysis2.setdefault('recommendations', []).append(rec)
                        
                        st.session_state.analysis2_results = analysis2
                    else:
                        st.error("Second contract analysis failed.")
                        st.stop()
                else:
                    automated2 = run_automated_risk_detection(st.session_state.contract2_text)
                    st.session_state.analysis2_results = {
                        'summary': 'Automated rule-based analysis',
                        'overall_risk': automated2['overall_risk'],
                        'risks': automated2['risks'],
                        'red_flags': [],
                        'missing_clauses': automated2['missing_clauses'],
                        'key_terms': [],
                        'recommendations': automated2.get('recommendations', [])
                    }
                
                # Compare contracts
                st.info("Comparing contracts...")
                
                comparison = compare_contracts(
                    st.session_state.contract_text,
                    st.session_state.contract2_text,
                    st.session_state.analysis_results,
                    st.session_state.analysis2_results,
                    api_key,
                    st.session_state.language
                )
                
                st.session_state.comparison_results = comparison
        
        else:  # specific clause analysis
            if not clause_type:
                st.error("Please select a clause type to analyze")
                st.stop()
            
            # Analyze specific clause
            clause_result = analyze_specific_clause(
                st.session_state.contract_text,
                clause_type,
                api_key if use_ai else None,
                st.session_state.language
            )
            
            st.session_state.clause_results = clause_result
        
        st.session_state.analysis_complete = True
        st.success("✅ Analysis complete!")

# Display results
if st.session_state.get('analysis_complete'):
    st.markdown("---")
    
    # Check what type of analysis was done
    if analysis_type == 'specific' and st.session_state.get('clause_results'):
        # Show clause analysis
        show_clause_analysis(
            st.session_state.clause_results,
            clause_type
        )
        
    elif st.session_state.get('analysis_results'):
        # If comparison mode, show comparison results
        if comparison_mode and st.session_state.get('comparison_results'):
            show_comparison_results(
                st.session_state.comparison_results,
                st.session_state.contract_filename,
                st.session_state.contract2_filename
            )
            
            # Show individual analyses in TABS
            st.markdown("---")
            st.subheader("Detailed Individual Analyses")
            
            tab1, tab2 = st.tabs([
                f"📄 {st.session_state.contract_filename}",
                f"📄 {st.session_state.contract2_filename}"
            ])
            
            with tab1:
                show_analysis(st.session_state.analysis_results)
            
            with tab2:
                if st.session_state.get('analysis2_results'):
                    show_analysis(st.session_state.analysis2_results)
        
        else:
            # Single contract analysis
            show_analysis(st.session_state.analysis_results)
    
    # Export section (only for full analysis, not clause-specific)
    if analysis_type != 'specific':
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
            if comparison_mode and st.session_state.get('comparison_results'):
                st.info("Comparison report coming soon")
            else:
                st.info("PDF export coming soon")
    
    # New analysis button
    st.markdown("---")
    if st.button("🔄 Analyze New Contract"):
        reset_analysis()
        st.rerun()