"""
Contract comparison view

Copyright (c) 2025 Mattias Nyqvist
Licensed under the MIT License
"""

import streamlit as st
from typing import Dict, Optional
import plotly.graph_objects as go
from config.settings import RISK_LEVELS


def render_comparison_upload() -> Optional[object]:
    """
    Render second contract upload for comparison.
    
    Returns:
        Uploaded file object or None
    """
    st.sidebar.markdown("### Second Contract")
    
    uploaded_file = st.sidebar.file_uploader(
        "Upload Contract to Compare",
        type=['pdf', 'docx', 'doc'],
        help="Upload a second contract to compare with the first",
        key="contract2_uploader"
    )
    
    if uploaded_file is not None:
        st.sidebar.success(f"Loaded: {uploaded_file.name}")
        return uploaded_file
    
    return None


def show_comparison_summary(comparison: Dict):
    """
    Display comparison summary metrics.
    
    Args:
        comparison: Comparison results dictionary
    """
    st.markdown("## Contract Comparison Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 Contract 1")
        st.metric("Overall Risk", comparison.get('contract1_risk', 'UNKNOWN'))
        st.metric("Risks Identified", comparison.get('contract1_risk_count', 0))
        st.metric("Missing Clauses", comparison.get('contract1_missing_count', 0))
    
    with col2:
        st.markdown("### 📄 Contract 2")
        st.metric("Overall Risk", comparison.get('contract2_risk', 'UNKNOWN'))
        st.metric("Risks Identified", comparison.get('contract2_risk_count', 0))
        st.metric("Missing Clauses", comparison.get('contract2_missing_count', 0))


def show_risk_comparison_chart(comparison: Dict):
    """
    Display risk comparison chart.
    
    Args:
        comparison: Comparison results dictionary
    """
    # Get risk counts by level for both contracts
    risk1_counts = comparison.get('contract1_risks_by_level', {})
    risk2_counts = comparison.get('contract2_risks_by_level', {})
    
    risk_levels = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'MINIMAL']
    
    contract1_values = [risk1_counts.get(level, 0) for level in risk_levels]
    contract2_values = [risk2_counts.get(level, 0) for level in risk_levels]
    
    fig = go.Figure(data=[
        go.Bar(name='Contract 1', x=risk_levels, y=contract1_values, marker_color='#3b82f6'),
        go.Bar(name='Contract 2', x=risk_levels, y=contract2_values, marker_color='#10b981')
    ])
    
    fig.update_layout(
        title='Risk Distribution Comparison',
        xaxis_title='Risk Level',
        yaxis_title='Number of Risks',
        barmode='group',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def show_key_differences(comparison: Dict):
    """
    Display key differences between contracts.
    
    Args:
        comparison: Comparison results dictionary
    """
    st.markdown("### 🔍 Key Differences")
    
    differences = comparison.get('key_differences', [])
    
    if differences:
        for diff in differences:
            st.markdown(f"- {diff}")
    else:
        st.info("No major differences identified")


def show_unique_clauses(comparison: Dict):
    """
    Display clauses unique to each contract.
    
    Args:
        comparison: Comparison results dictionary
    """
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 Only in Contract 1")
        unique1 = comparison.get('unique_to_contract1', [])
        if unique1:
            for item in unique1:
                st.markdown(f"- {item}")
        else:
            st.info("No unique clauses")
    
    with col2:
        st.markdown("### 📄 Only in Contract 2")
        unique2 = comparison.get('unique_to_contract2', [])
        if unique2:
            for item in unique2:
                st.markdown(f"- {item}")
        else:
            st.info("No unique clauses")


def show_comparison_recommendation(comparison: Dict):
    """
    Display which contract is more favorable.
    
    Args:
        comparison: Comparison results dictionary
    """
    st.markdown("### 💡 Recommendation")
    
    recommendation = comparison.get('recommendation', '')
    better_contract = comparison.get('better_contract', 'NEUTRAL')
    
    if better_contract == 'CONTRACT1':
        st.success("✅ Contract 1 appears more favorable")
    elif better_contract == 'CONTRACT2':
        st.success("✅ Contract 2 appears more favorable")
    else:
        st.info("⚖️ Contracts are relatively similar in risk")
    
    if recommendation:
        st.markdown(recommendation)


def show_comparison_results(comparison: Dict, filename1: str = "Contract 1", filename2: str = "Contract 2"):
    """
    Display complete comparison results.
    
    Args:
        comparison: Comparison results dictionary
        filename1: Name of first contract file
        filename2: Name of second contract file
    """
    # Summary metrics
    st.markdown("## Contract Comparison Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### 📄 {filename1}")
        st.metric("Overall Risk", comparison.get('contract1_risk', 'UNKNOWN'))
        st.metric("Risks Identified", comparison.get('contract1_risk_count', 0))
        st.metric("Missing Clauses", comparison.get('contract1_missing_count', 0))
    
    with col2:
        st.markdown(f"### 📄 {filename2}")
        st.metric("Overall Risk", comparison.get('contract2_risk', 'UNKNOWN'))
        st.metric("Risks Identified", comparison.get('contract2_risk_count', 0))
        st.metric("Missing Clauses", comparison.get('contract2_missing_count', 0))
    
    st.markdown("---")
    
    # Risk comparison chart
    show_risk_comparison_chart(comparison)
    
    st.markdown("---")
    
    # Tabs for different aspects
    tab1, tab2, tab3 = st.tabs(["Key Differences", "Unique Clauses", "Recommendation"])
    
    with tab1:
        show_key_differences(comparison)
        
        # Full AI analysis
        if comparison.get('full_analysis'):
            with st.expander("📄 Full Comparison Analysis"):
                st.markdown(comparison['full_analysis'])
    
    with tab2:
        # Update headers with filenames
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### 📄 Only in {filename1}")
            unique_to_1 = comparison.get('unique_to_contract2', [])  # These are missing from contract1
            if unique_to_1:
                for item in unique_to_1:
                    st.markdown(f"- {item}")
            else:
                st.info("No unique clauses")
        
        with col2:
            st.markdown(f"### 📄 Only in {filename2}")
            unique_to_2 = comparison.get('unique_to_contract1', [])  # These are missing from contract2
            if unique_to_2:
                for item in unique_to_2:
                    st.markdown(f"- {item}")
            else:
                st.info("No unique clauses")
    
    with tab3:
        show_comparison_recommendation(comparison)