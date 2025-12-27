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
    import re
    
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
    
    # Split into lines
    lines = response_text.split('\n')
    current_section = None
    current_item = {}
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        if not line:
            continue
        
        # Clean line for section detection
        clean_line = line.replace('#', '').strip()
        clean_line = re.sub(r'^\d+\.?\s*', '', clean_line)
        clean_line_upper = clean_line.upper()
        
        # Detect sections
        if 'EXECUTIVE SUMMARY' in clean_line_upper:
            current_section = 'summary'
            continue
        elif 'KEY TERMS' in clean_line_upper:
            current_section = 'key_terms'
            continue
        elif 'RISK ASSESSMENT' in clean_line_upper:
            current_section = 'risks'
            continue
        elif 'RED FLAGS' in clean_line_upper or 'RED FLAG' in clean_line_upper:
            current_section = 'red_flags'
            continue
        elif 'MISSING CLAUSES' in clean_line_upper or 'MISSING CLAUSE' in clean_line_upper:
            current_section = 'missing_clauses'
            continue
        elif 'RECOMMENDATIONS' in clean_line_upper or 'RECOMMENDATION' in clean_line_upper:
            current_section = 'recommendations'
            continue
        
        # Parse content based on section
        if current_section == 'summary':
            # Skip header lines
            if line.startswith('#'):
                continue
            
            # Clean markdown more carefully
            # First handle bold markers with spaces
            clean_text = line
            # Replace **text** with text (preserve spaces)
            clean_text = re.sub(r'\*\*([^*]+)\*\*', r'\1', clean_text)
            # Replace *text* with text
            clean_text = re.sub(r'\*([^*]+)\*', r'\1', clean_text)
            # Clean up any remaining * or **
            clean_text = clean_text.replace('**', '').replace('*', '')
            # Normalize spaces
            clean_text = ' '.join(clean_text.split())
            
            # Check if this line contains Overall Risk marker
            if 'overall risk' in clean_text.lower():
                # Split: everything before "Overall Risk" is summary (case insensitive)
                parts = re.split(r'overall risk', clean_text, flags=re.IGNORECASE)
                summary_part = parts[0].strip()
                
                if summary_part:
                    result['summary'] += summary_part + ' '
                
                # Extract risk level from the full line
                for risk in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'MINIMAL']:
                    if risk in line.upper():
                        result['overall_risk'] = risk
                        break
            else:
                # Normal line - add everything
                if clean_text:
                    result['summary'] += clean_text + ' '
        
        elif current_section == 'key_terms':
            if line.startswith('-') or line.startswith('•') or line.startswith('**-'):
                clean_line = line.lstrip('-•* ').strip()
                if clean_line:
                    result['key_terms'].append(clean_line)
        
        elif current_section == 'risks':
            # New risk item
            if line.startswith('**Risk') or line.startswith('###') or line.startswith('**Category'):
                if current_item:
                    result['risks'].append(current_item)
                current_item = {'text': line.lstrip('#* ').strip(), 'level': 'MEDIUM'}
            elif 'Risk Level:' in line or '**Risk Level**:' in line:
                for risk in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'MINIMAL']:
                    if risk in line.upper():
                        current_item['level'] = risk
                        break
            elif current_item:
                # Continue current risk
                current_item['text'] += ' ' + line.strip()
        
        elif current_section in ['red_flags', 'missing_clauses']:
            if line.startswith('-') or line.startswith('•') or line.startswith('**-') or (line and line[0].isdigit() and '.' in line[:3]):
                clean_line = line.lstrip('-•*0123456789. )').strip()
                if clean_line:
                    result[current_section].append(clean_line)
        
        elif current_section == 'recommendations':
            if line.startswith('-') or line.startswith('•') or (line and line[0].isdigit() and '.' in line[:3]):
                clean_line = line.lstrip('-•0123456789. ').strip()
                if clean_line and len(clean_line) > 10:
                    result['recommendations'].append(clean_line)
    
    # Add last risk item
    if current_item and current_section == 'risks':
        result['risks'].append(current_item)
    
    # Clean summary
    result['summary'] = result['summary'].strip()
    
    # Fix capitalization - capitalize first letter
    if result['summary']:
        result['summary'] = result['summary'][0].upper() + result['summary'][1:]
    
    # Extract recommendations from risks if needed
    if len(result['recommendations']) < 2:
        for risk in result['risks']:
            risk_text = risk.get('text', '')
            if '**Recommendation**:' in risk_text or 'Recommendation:' in risk_text:
                parts = risk_text.split('ecommendation**:' if '**' in risk_text else 'ecommendation:')
                if len(parts) > 1:
                    rec = parts[1].strip()
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