"""
Clause-by-clause analysis view

Copyright (c) 2025 Mattias Nyqvist
Licensed under the MIT License
"""

import streamlit as st
from typing import Dict, Optional


def show_clause_analysis(clause_result: Dict, clause_type: str):
    """
    Display detailed clause analysis.
    
    Args:
        clause_result: Clause analysis results
        clause_type: Type of clause analyzed
    """
    st.markdown(f"## {clause_type} Clause Analysis")
    
    # Check if clause was found
    if not clause_result.get('found', False):
        st.warning(f"⚠️ No {clause_type} clause found in this contract")
        
        if clause_result.get('analysis'):
            st.markdown("### Why This Matters")
            st.markdown(clause_result['analysis'])
        
        return
    
    # Clause was found - show analysis
    st.success(f"✅ {clause_type} clause identified in contract")
    
    # Create tabs for different aspects
    tab1, tab2, tab3 = st.tabs(["Clause Text", "Analysis", "Recommendations"])
    
    with tab1:
        show_clause_text(clause_result)
    
    with tab2:
        show_clause_analysis_details(clause_result, clause_type)
    
    with tab3:
        show_clause_recommendations(clause_result)


def show_clause_text(clause_result: Dict):
    """Display extracted clause text."""
    st.markdown("### Extracted Clause Text")
    
    clause_text = clause_result.get('clause_text', '')
    location = clause_result.get('location', 'Location not specified')
    
    if clause_text:
        st.info(f"📍 **Location:** {location}")
        st.markdown("---")
        
        # Display clause in a nice box
        st.markdown(
            f"""
            <div style="
                background-color: #f8f9fa;
                border-left: 4px solid #3b82f6;
                padding: 20px;
                border-radius: 5px;
                font-family: monospace;
                white-space: pre-wrap;
            ">
            {clause_text}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.info("Clause text not available in structured format")


def show_clause_analysis_details(clause_result: Dict, clause_type: str):
    """Display detailed analysis of the clause."""
    st.markdown("### Detailed Analysis")
    
    # Plain language summary
    summary = clause_result.get('summary', '')
    if summary:
        st.markdown("#### Plain Language Summary")
        st.markdown(summary)
        st.markdown("---")
    
    # Risk assessment
    risk_level = clause_result.get('risk_level', 'UNKNOWN')
    risks = clause_result.get('risks', [])
    
    if risk_level != 'UNKNOWN':
        st.markdown("#### Risk Assessment")
        
        risk_colors = {
            'CRITICAL': '#dc2626',
            'HIGH': '#ea580c',
            'MEDIUM': '#f59e0b',
            'LOW': '#059669',
            'MINIMAL': '#0891b2'
        }
        
        color = risk_colors.get(risk_level, '#6b7280')
        
        st.markdown(
            f"""
            <div style="
                background-color: {color};
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
                margin: 10px 0;
            ">
                Risk Level: {risk_level}
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if risks:
            st.markdown("**Identified Risks:**")
            for risk in risks:
                st.markdown(f"- {risk}")
        
        st.markdown("---")
    
    # Favorability
    favorability = clause_result.get('favorability', 'NEUTRAL')
    if favorability:
        st.markdown("#### Favorability Assessment")
        
        fav_colors = {
            'FAVORABLE': '#059669',
            'NEUTRAL': '#f59e0b',
            'UNFAVORABLE': '#dc2626'
        }
        
        fav_icons = {
            'FAVORABLE': '✅',
            'NEUTRAL': '⚖️',
            'UNFAVORABLE': '❌'
        }
        
        color = fav_colors.get(favorability.upper(), '#6b7280')
        icon = fav_icons.get(favorability.upper(), '❓')
        
        st.markdown(f"{icon} This clause is **{favorability}** to you")
    
    # Full AI analysis
    analysis = clause_result.get('analysis', '')
    if analysis and len(analysis) > 100:
        st.markdown("---")
        st.markdown("#### Complete Analysis")
        st.markdown(analysis)


def show_clause_recommendations(clause_result: Dict):
    """Display recommendations for the clause."""
    st.markdown("### Recommendations")
    
    recommendations = clause_result.get('recommendations', [])
    
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"{i}. {rec}")
    else:
        # Extract from analysis if available
        analysis = clause_result.get('analysis', '')
        if 'recommend' in analysis.lower():
            st.markdown(analysis)
        else:
            st.info("No specific recommendations available for this clause")


def show_clause_not_found_help(clause_type: str):
    """Show helpful information when clause is not found."""
    st.warning(f"⚠️ {clause_type} clause not found in contract")
    
    st.markdown("### What This Means")
    
    importance = {
        'Payment Terms': 'CRITICAL - Every contract should clearly specify payment obligations',
        'Liability': 'HIGH - Important for understanding financial exposure',
        'Termination': 'HIGH - Defines how either party can exit the agreement',
        'Confidentiality': 'MEDIUM - Important for protecting sensitive information',
        'Intellectual Property': 'HIGH - Critical for ownership of work product',
        'Warranties': 'MEDIUM - Defines quality guarantees and representations',
        'Indemnification': 'HIGH - Determines who covers third-party claims',
        'Dispute Resolution': 'MEDIUM - Specifies how conflicts will be resolved',
        'Force Majeure': 'LOW - Protects against unforeseeable events',
        'Non-Compete': 'MEDIUM - May restrict future business activities',
        'Governing Law': 'MEDIUM - Determines which jurisdiction applies'
    }
    
    imp_level = importance.get(clause_type, 'UNKNOWN')
    st.error(f"**Importance:** {imp_level}")
    
    st.markdown("### What You Should Do")
    st.markdown(f"""
    1. **Add a {clause_type} clause** to this contract before signing
    2. **Consult a lawyer** to draft appropriate language
    3. **Review industry standards** for typical {clause_type} terms
    4. **Negotiate with the other party** to include this protection
    """)