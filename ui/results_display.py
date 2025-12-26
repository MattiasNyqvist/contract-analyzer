"""
Display analysis results

Copyright (c) 2025 Mattias Nyqvist
Licensed under the MIT License
"""

import streamlit as st
from config.settings import RISK_LEVELS
from utils.formatters import get_risk_color
import plotly.graph_objects as go


def show_overall_risk_badge(risk_level: str):
    """
    Display overall risk level badge.
    
    Args:
        risk_level: Risk level (CRITICAL/HIGH/MEDIUM/LOW/MINIMAL)
    """
    risk_info = RISK_LEVELS.get(risk_level.upper(), RISK_LEVELS['MEDIUM'])
    
    st.markdown(
        f"""
        <div style="
            background-color: {risk_info['color']};
            color: white;
            padding: 15px 30px;
            border-radius: 10px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin: 20px 0;
        ">
            Overall Risk: {risk_info['label'].upper()}
        </div>
        """,
        unsafe_allow_html=True
    )


def show_summary_section(analysis: dict):
    """
    Display executive summary.
    
    Args:
        analysis: Analysis results dictionary
    """
    st.markdown("## Executive Summary")
    
    if analysis.get('summary'):
        st.markdown(analysis['summary'])
    else:
        st.info("No summary available")


def show_key_metrics(analysis: dict):
    """
    Display key metrics.
    
    Args:
        analysis: Analysis results dictionary
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        risk_count = len(analysis.get('risks', []))
        st.metric("Risks Identified", risk_count)
    
    with col2:
        red_flags = len(analysis.get('red_flags', []))
        st.metric("Red Flags", red_flags)
    
    with col3:
        missing = len(analysis.get('missing_clauses', []))
        st.metric("Missing Clauses", missing)
    
    with col4:
        recommendations = len(analysis.get('recommendations', []))
        st.metric("Recommendations", recommendations)


def show_risk_breakdown(analysis: dict):
    """
    Display risk breakdown chart.
    
    Args:
        analysis: Analysis results dictionary
    """
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
    colors = [get_risk_color(level) for level in labels]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        hole=0.4
    )])
    
    fig.update_layout(
        title="Risk Distribution by Level",
        showlegend=True,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def show_risks_section(analysis: dict):
    """
    Display detailed risks.
    
    Args:
        analysis: Analysis results dictionary
    """
    st.markdown("## Risk Assessment")
    
    risks = analysis.get('risks', [])
    
    if not risks:
        st.info("No specific risks identified")
        return
    
    # Group by risk level
    risk_groups = {
        'CRITICAL': [],
        'HIGH': [],
        'MEDIUM': [],
        'LOW': [],
        'MINIMAL': []
    }
    
    for risk in risks:
        level = risk.get('level', 'MEDIUM')
        risk_groups[level].append(risk)
    
    # Display risks by level
    for level in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'MINIMAL']:
        level_risks = risk_groups[level]
        if not level_risks:
            continue
        
        risk_info = RISK_LEVELS[level]
        
        with st.expander(f"{risk_info['label']} ({len(level_risks)})", expanded=(level in ['CRITICAL', 'HIGH'])):
            for i, risk in enumerate(level_risks, 1):
                risk_text = risk.get('text', risk.get('description', 'No description'))
                
                st.markdown(
                    f"""
                    <div style="
                        border-left: 4px solid {risk_info['color']};
                        padding: 10px;
                        margin: 10px 0;
                        background-color: rgba(0,0,0,0.02);
                    ">
                        <strong>Risk #{i}</strong><br>
                        {risk_text}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


def show_red_flags_section(analysis: dict):
    """
    Display red flags.
    
    Args:
        analysis: Analysis results dictionary
    """
    red_flags = analysis.get('red_flags', [])
    
    if not red_flags:
        return
    
    st.markdown("## Red Flags")
    
    for flag in red_flags:
        st.markdown(f"⚠️ {flag}")


def show_missing_clauses_section(analysis: dict):
    """
    Display missing clauses.
    
    Args:
        analysis: Analysis results dictionary
    """
    missing = analysis.get('missing_clauses', [])
    
    if not missing:
        return
    
    st.markdown("## Missing Clauses")
    
    st.warning(f"Found {len(missing)} potentially missing important clause(s)")
    
    for clause in missing:
        st.markdown(f"- {clause}")


def show_recommendations_section(analysis: dict):
    """
    Display recommendations.
    
    Args:
        analysis: Analysis results dictionary
    """
    recommendations = analysis.get('recommendations', [])
    
    if not recommendations:
        return
    
    st.markdown("## Recommendations")
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"{i}. {rec}")


def show_key_terms_section(analysis: dict):
    """
    Display key terms.
    
    Args:
        analysis: Analysis results dictionary
    """
    key_terms = analysis.get('key_terms', [])
    
    if not key_terms:
        return
    
    st.markdown("## Key Terms")
    
    for term in key_terms:
        st.markdown(f"- {term}")


def show_analysis(analysis: dict):
    """
    Display complete analysis results.
    
    Args:
        analysis: Analysis results dictionary
    """
    # Overall risk badge
    show_overall_risk_badge(analysis.get('overall_risk', 'MEDIUM'))
    
    # Key metrics
    show_key_metrics(analysis)
    
    st.markdown("---")
    
    # Executive summary
    show_summary_section(analysis)
    
    st.markdown("---")
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["Risks", "Key Terms", "Missing Items", "Recommendations"])
    
    with tab1:
        show_risk_breakdown(analysis)
        show_risks_section(analysis)
        show_red_flags_section(analysis)
    
    with tab2:
        show_key_terms_section(analysis)
    
    with tab3:
        show_missing_clauses_section(analysis)
    
    with tab4:
        show_recommendations_section(analysis)


def show_comparison_results(comparison: dict):
    """
    Display contract comparison results.
    
    Args:
        comparison: Comparison results dictionary
    """
    st.markdown("## Contract Comparison")
    
    # Display comparison results
    if comparison.get('analysis'):
        st.markdown(comparison['analysis'])
    else:
        st.info("No comparison results available")