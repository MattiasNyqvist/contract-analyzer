"""
Results display components

Copyright (c) 2025 Mattias Nyqvist
Licensed under the MIT License
"""

import streamlit as st
import plotly.graph_objects as go
from config.settings import RISK_LEVELS


def show_overall_risk_badge(risk_level: str):
    """Display overall risk level badge."""
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
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin: 20px 0;
        ">
            Overall Risk: {risk_level} RISK
        </div>
        """,
        unsafe_allow_html=True
    )


def show_summary_section(analysis: dict):
    """Display executive summary."""
    st.markdown("## Executive Summary")
    
    summary = analysis.get('summary', '')
    
    if summary and len(summary) > 10:
        # Use HTML paragraph for consistent formatting
        st.markdown(
            f"""
            <div style="
                font-size: 16px;
                line-height: 1.6;
                color: #1f2937;
                background-color: #f9fafb;
                padding: 20px;
                border-radius: 8px;
                border-left: 4px solid #3b82f6;
            ">
                {summary}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.info("No summary available")


def show_key_metrics(analysis: dict):
    """Display key metrics."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Risks Identified", len(analysis.get('risks', [])))
    
    with col2:
        st.metric("Red Flags", len(analysis.get('red_flags', [])))
    
    with col3:
        st.metric("Missing Clauses", len(analysis.get('missing_clauses', [])))
    
    with col4:
        st.metric("Recommendations", len(analysis.get('recommendations', [])))


def show_risk_breakdown(analysis: dict):
    """Display risk breakdown chart."""
    risks = analysis.get('risks', [])
    
    if not risks:
        return
    
    # Count risks by level
    risk_counts = {}
    for risk in risks:
        level = risk.get('level', 'MEDIUM')
        risk_counts[level] = risk_counts.get(level, 0) + 1
    
    # Create pie chart
    labels = list(risk_counts.keys())
    values = list(risk_counts.values())
    
    colors = {
        'CRITICAL': '#dc2626',
        'HIGH': '#ea580c',
        'MEDIUM': '#f59e0b',
        'LOW': '#059669',
        'MINIMAL': '#0891b2'
    }
    
    chart_colors = [colors.get(label, '#6b7280') for label in labels]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=chart_colors),
        hole=0.3
    )])
    
    fig.update_layout(
        title="Risk Distribution",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def show_risks_section(analysis: dict):
    """Display risks section."""
    st.markdown("### Risk Assessment")
    
    risks = analysis.get('risks', [])
    
    if not risks:
        st.info("No specific risks identified")
        return
    
    # Group risks by level
    risk_groups = {}
    for risk in risks:
        level = risk.get('level', 'MEDIUM')
        if level not in risk_groups:
            risk_groups[level] = []
        risk_groups[level].append(risk)
    
    # Display risks by level
    level_order = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'MINIMAL']
    
    for level in level_order:
        if level in risk_groups:
            level_risks = risk_groups[level]
            
            with st.expander(f"{level} Risk ({len(level_risks)} items)", expanded=(level in ['CRITICAL', 'HIGH'])):
                for risk in level_risks:
                    st.markdown(f"**{risk.get('text', 'Unknown risk')}**")
                    st.markdown("---")


def show_red_flags_section(analysis: dict):
    """Display red flags."""
    st.markdown("### Red Flags")
    
    red_flags = analysis.get('red_flags', [])
    
    if red_flags:
        for flag in red_flags:
            st.warning(f"⚠️ {flag}")
    else:
        st.info("No red flags identified")


def show_missing_clauses_section(analysis: dict):
    """Display missing clauses."""
    st.markdown("### Missing Clauses")
    
    missing = analysis.get('missing_clauses', [])
    
    if missing:
        st.warning(f"Found {len(missing)} potentially missing important clause(s)")
        for clause in missing:
            st.markdown(f"- {clause}")
    else:
        st.success("All important clauses appear to be present")


def show_recommendations_section(analysis: dict):
    """Display recommendations."""
    st.markdown("### Recommendations")
    
    recommendations = analysis.get('recommendations', [])
    
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"{i}. {rec}")
    else:
        st.info("No specific recommendations available")


def show_key_terms_section(analysis: dict):
    """Display key terms."""
    st.markdown("### Key Terms")
    
    key_terms = analysis.get('key_terms', [])
    
    if key_terms:
        for term in key_terms:
            st.markdown(f"- {term}")
    else:
        st.info("No key terms extracted")


def show_analysis(analysis: dict):
    """
    Display complete analysis results.
    
    Args:
        analysis: Analysis results dictionary
    """
    # Overall risk badge
    show_overall_risk_badge(analysis.get('overall_risk', 'UNKNOWN'))
    
    # Key metrics
    show_key_metrics(analysis)
    
    st.markdown("---")
    
    # Summary
    show_summary_section(analysis)
    
    st.markdown("---")
    
    # Risk breakdown chart
    show_risk_breakdown(analysis)
    
    st.markdown("---")
    
    # Tabs for detailed sections
    tab1, tab2, tab3, tab4 = st.tabs(["Risks", "Key Terms", "Missing Items", "Recommendations"])
    
    with tab1:
        show_risks_section(analysis)
        st.markdown("---")
        show_red_flags_section(analysis)
    
    with tab2:
        show_key_terms_section(analysis)
    
    with tab3:
        show_missing_clauses_section(analysis)
    
    with tab4:
        show_recommendations_section(analysis)