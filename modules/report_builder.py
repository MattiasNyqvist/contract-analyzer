"""
Generate analysis reports

Copyright (c) 2025 Mattias Nyqvist
Licensed under the MIT License
"""

from datetime import datetime
from typing import Dict
import io


def generate_text_report(analysis: Dict, contract_filename: str) -> str:
    """
    Generate plain text report.
    
    Args:
        analysis: Analysis results dictionary
        contract_filename: Name of analyzed contract
        
    Returns:
        Formatted text report
    """
    report = []
    report.append("=" * 80)
    report.append("CONTRACT ANALYSIS REPORT")
    report.append("=" * 80)
    report.append(f"\nContract: {contract_filename}")
    report.append(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"Overall Risk Level: {analysis.get('overall_risk', 'UNKNOWN')}")
    report.append("\n" + "=" * 80)
    
    # Executive Summary
    if analysis.get('summary'):
        report.append("\nEXECUTIVE SUMMARY")
        report.append("-" * 80)
        report.append(analysis['summary'])
    
    # Key Terms
    if analysis.get('key_terms'):
        report.append("\n\nKEY TERMS")
        report.append("-" * 80)
        for term in analysis['key_terms']:
            report.append(f"• {term}")
    
    # Risks
    if analysis.get('risks'):
        report.append("\n\nRISK ASSESSMENT")
        report.append("-" * 80)
        for i, risk in enumerate(analysis['risks'], 1):
            report.append(f"\nRisk #{i}")
            report.append(f"  Level: {risk.get('level', 'N/A')}")
            report.append(f"  Description: {risk.get('text', risk.get('description', 'N/A'))}")
    
    # Red Flags
    if analysis.get('red_flags'):
        report.append("\n\nRED FLAGS")
        report.append("-" * 80)
        for flag in analysis['red_flags']:
            report.append(f"⚠ {flag}")
    
    # Missing Clauses
    if analysis.get('missing_clauses'):
        report.append("\n\nMISSING CLAUSES")
        report.append("-" * 80)
        for clause in analysis['missing_clauses']:
            report.append(f"• {clause}")
    
    # Recommendations
    if analysis.get('recommendations'):
        report.append("\n\nRECOMMENDATIONS")
        report.append("-" * 80)
        for i, rec in enumerate(analysis['recommendations'], 1):
            report.append(f"{i}. {rec}")
    
    report.append("\n" + "=" * 80)
    report.append("End of Report")
    report.append("=" * 80)
    
    return "\n".join(report)


def generate_markdown_report(analysis: Dict, contract_filename: str) -> str:
    """
    Generate Markdown report.
    
    Args:
        analysis: Analysis results dictionary
        contract_filename: Name of analyzed contract
        
    Returns:
        Formatted Markdown report
    """
    md = []
    md.append("# Contract Analysis Report\n")
    md.append(f"**Contract:** {contract_filename}  ")
    md.append(f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  ")
    md.append(f"**Overall Risk Level:** {analysis.get('overall_risk', 'UNKNOWN')}  \n")
    
    # Executive Summary
    if analysis.get('summary'):
        md.append("## Executive Summary\n")
        md.append(f"{analysis['summary']}\n")
    
    # Key Terms
    if analysis.get('key_terms'):
        md.append("## Key Terms\n")
        for term in analysis['key_terms']:
            md.append(f"- {term}")
        md.append("")
    
    # Risks
    if analysis.get('risks'):
        md.append("## Risk Assessment\n")
        for i, risk in enumerate(analysis['risks'], 1):
            level = risk.get('level', 'N/A')
            desc = risk.get('text', risk.get('description', 'N/A'))
            md.append(f"### Risk #{i} - {level}\n")
            md.append(f"{desc}\n")
    
    # Red Flags
    if analysis.get('red_flags'):
        md.append("## Red Flags\n")
        for flag in analysis['red_flags']:
            md.append(f"⚠️ {flag}")
        md.append("")
    
    # Missing Clauses
    if analysis.get('missing_clauses'):
        md.append("## Missing Clauses\n")
        for clause in analysis['missing_clauses']:
            md.append(f"- {clause}")
        md.append("")
    
    # Recommendations
    if analysis.get('recommendations'):
        md.append("## Recommendations\n")
        for i, rec in enumerate(analysis['recommendations'], 1):
            md.append(f"{i}. {rec}")
        md.append("")
    
    return "\n".join(md)


def generate_html_report(analysis: Dict, contract_filename: str) -> str:
    """
    Generate HTML report.
    
    Args:
        analysis: Analysis results dictionary
        contract_filename: Name of analyzed contract
        
    Returns:
        Formatted HTML report
    """
    risk_colors = {
        'CRITICAL': '#dc2626',
        'HIGH': '#ea580c',
        'MEDIUM': '#f59e0b',
        'LOW': '#059669',
        'MINIMAL': '#0891b2'
    }
    
    overall_risk = analysis.get('overall_risk', 'MEDIUM')
    risk_color = risk_colors.get(overall_risk, '#6b7280')
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Contract Analysis Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            line-height: 1.6;
        }}
        h1 {{
            color: #1f2937;
            border-bottom: 3px solid {risk_color};
            padding-bottom: 10px;
        }}
        h2 {{
            color: #374151;
            margin-top: 30px;
            border-bottom: 1px solid #e5e7eb;
            padding-bottom: 5px;
        }}
        .metadata {{
            background: #f9fafb;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .risk-badge {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 15px;
            color: white;
            background: {risk_color};
            font-weight: bold;
        }}
        .risk-item {{
            background: #fef3c7;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #f59e0b;
            border-radius: 3px;
        }}
        .risk-critical {{ border-left-color: #dc2626; background: #fee2e2; }}
        .risk-high {{ border-left-color: #ea580c; background: #ffedd5; }}
        .risk-medium {{ border-left-color: #f59e0b; background: #fef3c7; }}
        .risk-low {{ border-left-color: #059669; background: #d1fae5; }}
        ul {{
            list-style-type: none;
            padding-left: 0;
        }}
        li {{
            padding: 5px 0;
            padding-left: 20px;
        }}
        li:before {{
            content: "•";
            color: #3b82f6;
            font-weight: bold;
            display: inline-block;
            width: 1em;
            margin-left: -1em;
        }}
    </style>
</head>
<body>
    <h1>Contract Analysis Report</h1>
    
    <div class="metadata">
        <p><strong>Contract:</strong> {contract_filename}</p>
        <p><strong>Analysis Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        <p><strong>Overall Risk Level:</strong> <span class="risk-badge">{overall_risk}</span></p>
    </div>
"""
    
    # Executive Summary
    if analysis.get('summary'):
        html += f"""
    <h2>Executive Summary</h2>
    <p>{analysis['summary']}</p>
"""
    
    # Key Terms
    if analysis.get('key_terms'):
        html += "<h2>Key Terms</h2><ul>"
        for term in analysis['key_terms']:
            html += f"<li>{term}</li>"
        html += "</ul>"
    
    # Risks
    if analysis.get('risks'):
        html += "<h2>Risk Assessment</h2>"
        for risk in analysis['risks']:
            level = risk.get('level', 'MEDIUM').lower()
            desc = risk.get('text', risk.get('description', 'N/A'))
            html += f'<div class="risk-item risk-{level}">'
            html += f'<strong>{risk.get("level", "N/A")} Risk:</strong> {desc}'
            html += '</div>'
    
    # Red Flags
    if analysis.get('red_flags'):
        html += "<h2>Red Flags</h2><ul>"
        for flag in analysis['red_flags']:
            html += f"<li>⚠️ {flag}</li>"
        html += "</ul>"
    
    # Missing Clauses
    if analysis.get('missing_clauses'):
        html += "<h2>Missing Clauses</h2><ul>"
        for clause in analysis['missing_clauses']:
            html += f"<li>{clause}</li>"
        html += "</ul>"
    
    # Recommendations
    if analysis.get('recommendations'):
        html += "<h2>Recommendations</h2><ol>"
        for rec in analysis['recommendations']:
            html += f"<li>{rec}</li>"
        html += "</ol>"
    
    html += """
</body>
</html>
"""
    
    return html