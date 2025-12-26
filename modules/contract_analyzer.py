"""
AI-powered contract analysis

Copyright (c) 2025 Mattias Nyqvist
Licensed under the MIT License
"""

import anthropic
from typing import Optional, Dict
from config.prompts import get_analysis_prompt


def analyze_contract(
    contract_text: str,
    api_key: str,
    language: str = 'en'
) -> Optional[Dict]:
    """
    Analyze contract using Claude AI.
    
    Args:
        contract_text: Full contract text
        api_key: Anthropic API key
        language: Response language ('en' or 'sv')
        
    Returns:
        Analysis results dictionary or None if failed
    """
    if not api_key:
        return None
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        # Generate prompt
        prompt = get_analysis_prompt(contract_text, language)
        
        # Call Claude API
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            temperature=0.3,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract response text
        analysis_text = response.content[0].text
        
        # Parse response into structured format
        result = parse_analysis_response(analysis_text)
        result['raw_response'] = analysis_text
        
        return result
        
    except Exception as e:
        print(f"Contract analysis failed: {e}")
        return None


def parse_analysis_response(response_text: str) -> Dict:
    """
    Parse AI response into structured format.
    
    Args:
        response_text: Raw AI response
        
    Returns:
        Structured analysis dictionary
    """
    # Initialize result structure
    result = {
        'summary': '',
        'overall_risk': 'MEDIUM',
        'key_terms': [],
        'risks': [],
        'red_flags': [],
        'missing_clauses': [],
        'recommendations': []
    }
    
    # Split into sections
    sections = response_text.split('\n')
    current_section = None
    current_item = {}
    
    for line in sections:
        line = line.strip()
        
        if not line:
            continue
        
        # Detect sections
        if 'EXECUTIVE SUMMARY' in line.upper():
            current_section = 'summary'
            continue
        elif 'KEY TERMS' in line.upper():
            current_section = 'key_terms'
            continue
        elif 'RISK ASSESSMENT' in line.upper():
            current_section = 'risks'
            continue
        elif 'RED FLAGS' in line.upper():
            current_section = 'red_flags'
            continue
        elif 'MISSING CLAUSES' in line.upper():
            current_section = 'missing_clauses'
            continue
        elif 'RECOMMENDATIONS' in line.upper() or 'RECOMMENDATION' in line.upper():
            current_section = 'recommendations'
            continue
        
        # Parse content based on section
        if current_section == 'summary':
            if 'Overall risk level:' in line or 'risk level:' in line.lower():
                # Extract risk level
                for risk in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'MINIMAL']:
                    if risk in line.upper():
                        result['overall_risk'] = risk
                        break
            else:
                result['summary'] += line + ' '
        
        elif current_section == 'risks':
            if line.startswith('-') or line.startswith('•') or line.startswith('###'):
                # New risk item
                if current_item:
                    result['risks'].append(current_item)
                current_item = {'text': line.lstrip('-•#').strip()}
            elif 'Risk Level:' in line or '**Risk Level**:' in line:
                for risk in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'MINIMAL']:
                    if risk in line.upper():
                        current_item['level'] = risk
                        break
        
        elif current_section in ['red_flags', 'missing_clauses', 'key_terms']:
            if line.startswith('-') or line.startswith('•') or line[0].isdigit():
                clean_line = line.lstrip('-•0123456789. ').strip()
                if clean_line:
                    result[current_section].append(clean_line)
        
        elif current_section == 'recommendations':
            if line.startswith('-') or line.startswith('•') or line[0].isdigit():
                clean_line = line.lstrip('-•0123456789. ').strip()
                if clean_line and len(clean_line) > 10:  # Filter out very short items
                    result['recommendations'].append(clean_line)
    
    # Add last risk item if exists
    if current_item and current_section == 'risks':
        result['risks'].append(current_item)
    
    # Clean summary
    result['summary'] = result['summary'].strip()
    
    # Extract recommendations from risks if no separate recommendations section found
    if len(result['recommendations']) < 2:
        for risk in result['risks']:
            risk_text = risk.get('text', '')
            # Look for embedded recommendations
            if '**Recommendation**:' in risk_text:
                parts = risk_text.split('**Recommendation**:')
                if len(parts) > 1:
                    rec = parts[1].strip()
                    # Remove any trailing incomplete parts
                    if rec and len(rec) > 20:
                        result['recommendations'].append(rec)
            elif 'recommendation**:' in risk_text.lower():
                # Case insensitive search
                import re
                match = re.search(r'\*\*recommendation\*\*:\s*(.+)', risk_text, re.IGNORECASE)
                if match:
                    rec = match.group(1).strip()
                    if rec and len(rec) > 20:
                        result['recommendations'].append(rec)
    
    return result


def get_quick_summary(contract_text: str, api_key: str) -> Optional[str]:
    """
    Get quick 2-3 sentence summary of contract.
    
    Args:
        contract_text: Full contract text
        api_key: Anthropic API key
        
    Returns:
        Brief summary or None
    """
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        prompt = f"""Provide a brief 2-3 sentence summary of this contract:

{contract_text[:3000]}

Include: contract type, parties involved, and main purpose."""
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=200,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
        
    except Exception as e:
        return None