"""
Contract comparison logic

Copyright (c) 2025 Mattias Nyqvist
Licensed under the MIT License
"""

import anthropic
from typing import Dict, Optional
from config.prompts import get_comparison_prompt


def compare_contracts(
    contract1_text: str,
    contract2_text: str,
    contract1_analysis: Dict,
    contract2_analysis: Dict,
    api_key: str,
    language: str = 'en'
) -> Optional[Dict]:
    """
    Compare two contracts using AI.
    
    Args:
        contract1_text: First contract text
        contract2_text: Second contract text
        contract1_analysis: Analysis of first contract
        contract2_analysis: Analysis of second contract
        api_key: Anthropic API key
        language: Response language
        
    Returns:
        Comparison results dictionary
    """
    if not api_key:
        return create_automated_comparison(contract1_analysis, contract2_analysis)
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        # Generate comparison prompt
        prompt = get_comparison_prompt(contract1_text, contract2_text, language)
        
        # Call Claude API
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            temperature=0.3,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract response
        comparison_text = response.content[0].text
        
        # Combine with automated comparison
        result = create_automated_comparison(contract1_analysis, contract2_analysis)
        result['full_analysis'] = comparison_text
        result['ai_comparison'] = True
        
        # Extract key differences from AI response
        result['key_differences'] = extract_key_differences(comparison_text)
        result['recommendation'] = extract_recommendation(comparison_text)
        
        return result
        
    except Exception as e:
        print(f"AI comparison failed: {e}")
        return create_automated_comparison(contract1_analysis, contract2_analysis)


def create_automated_comparison(
    contract1_analysis: Dict,
    contract2_analysis: Dict
) -> Dict:
    """
    Create automated comparison based on analysis results.
    
    Args:
        contract1_analysis: First contract analysis
        contract2_analysis: Second contract analysis
        
    Returns:
        Comparison dictionary
    """
    # Count risks by level
    def count_risks_by_level(risks):
        counts = {}
        for risk in risks:
            level = risk.get('level', 'MEDIUM')
            counts[level] = counts.get(level, 0) + 1
        return counts
    
    risk1_counts = count_risks_by_level(contract1_analysis.get('risks', []))
    risk2_counts = count_risks_by_level(contract2_analysis.get('risks', []))
    
    # Determine which is better
    risk1_score = calculate_risk_score(contract1_analysis.get('overall_risk', 'MEDIUM'))
    risk2_score = calculate_risk_score(contract2_analysis.get('overall_risk', 'MEDIUM'))
    
    if risk1_score < risk2_score:
        better_contract = 'CONTRACT1'
    elif risk2_score < risk1_score:
        better_contract = 'CONTRACT2'
    else:
        better_contract = 'NEUTRAL'
    
    # Find unique missing clauses
    missing1 = set(contract1_analysis.get('missing_clauses', []))
    missing2 = set(contract2_analysis.get('missing_clauses', []))
    
    unique_to_1 = list(missing2 - missing1)  # Contract 1 has these, 2 doesn't
    unique_to_2 = list(missing1 - missing2)  # Contract 2 has these, 1 doesn't
    
    return {
        'contract1_risk': contract1_analysis.get('overall_risk', 'UNKNOWN'),
        'contract2_risk': contract2_analysis.get('overall_risk', 'UNKNOWN'),
        'contract1_risk_count': len(contract1_analysis.get('risks', [])),
        'contract2_risk_count': len(contract2_analysis.get('risks', [])),
        'contract1_missing_count': len(contract1_analysis.get('missing_clauses', [])),
        'contract2_missing_count': len(contract2_analysis.get('missing_clauses', [])),
        'contract1_risks_by_level': risk1_counts,
        'contract2_risks_by_level': risk2_counts,
        'better_contract': better_contract,
        'unique_to_contract1': unique_to_1,
        'unique_to_contract2': unique_to_2,
        'key_differences': [],
        'recommendation': generate_automated_recommendation(better_contract, risk1_score, risk2_score),
        'ai_comparison': False
    }


def calculate_risk_score(risk_level: str) -> int:
    """Calculate numeric risk score."""
    scores = {
        'CRITICAL': 100,
        'HIGH': 75,
        'MEDIUM': 50,
        'LOW': 25,
        'MINIMAL': 10
    }
    return scores.get(risk_level, 50)


def generate_automated_recommendation(better: str, score1: int, score2: int) -> str:
    """Generate automated recommendation text."""
    diff = abs(score1 - score2)
    
    if better == 'CONTRACT1':
        return f"Contract 1 appears more favorable with lower overall risk. Consider using Contract 1 as the base for negotiations."
    elif better == 'CONTRACT2':
        return f"Contract 2 appears more favorable with lower overall risk. Consider using Contract 2 as the base for negotiations."
    else:
        return "Both contracts have similar risk profiles. Review specific clauses to determine which terms are more favorable for your situation."


def extract_key_differences(comparison_text: str) -> list:
    """Extract key differences from AI comparison."""
    differences = []
    
    # Look for KEY DIFFERENCES section
    if 'KEY DIFFERENCES' in comparison_text.upper():
        lines = comparison_text.split('\n')
        in_section = False
        
        for line in lines:
            if 'KEY DIFFERENCES' in line.upper():
                in_section = True
                continue
            if in_section and line.strip().startswith('-'):
                differences.append(line.strip().lstrip('- '))
            elif in_section and not line.strip():
                break
    
    return differences[:10]  # Limit to 10


def extract_recommendation(comparison_text: str) -> str:
    """Extract recommendation from AI comparison."""
    # Look for RECOMMENDATION section
    if 'RECOMMENDATION' in comparison_text.upper():
        lines = comparison_text.split('\n')
        in_section = False
        rec_text = []
        
        for line in lines:
            if 'RECOMMENDATION' in line.upper():
                in_section = True
                continue
            if in_section:
                if line.strip():
                    rec_text.append(line.strip())
                else:
                    break
        
        return ' '.join(rec_text)
    
    return ""