"""
Find and extract specific clauses

Copyright (c) 2025 Mattias Nyqvist
Licensed under the MIT License
"""

import re
from typing import List, Dict, Optional
import anthropic
from config.prompts import get_clause_extraction_prompt


def find_clause_by_keyword(contract_text: str, clause_type: str) -> Optional[str]:
    """
    Find clause using keyword matching.
    
    Args:
        contract_text: Contract text
        clause_type: Type of clause to find
        
    Returns:
        Clause text or None
    """
    clause_keywords = {
        'Payment Terms': ['payment', 'fee', 'compensation', 'invoice'],
        'Liability': ['liability', 'liable', 'responsible for'],
        'Termination': ['termination', 'terminate', 'cancel'],
        'Confidentiality': ['confidential', 'non-disclosure', 'proprietary'],
        'Intellectual Property': ['intellectual property', 'ip', 'copyright', 'patent'],
        'Warranties': ['warrant', 'guarantee', 'representation'],
        'Indemnification': ['indemnif', 'hold harmless'],
        'Dispute Resolution': ['dispute', 'arbitration', 'mediation'],
        'Force Majeure': ['force majeure', 'act of god'],
        'Governing Law': ['governing law', 'jurisdiction']
    }
    
    keywords = clause_keywords.get(clause_type, [])
    
    # Split into paragraphs
    paragraphs = contract_text.split('\n\n')
    
    # Find paragraphs containing keywords
    matching_paragraphs = []
    for para in paragraphs:
        para_lower = para.lower()
        for keyword in keywords:
            if keyword in para_lower:
                matching_paragraphs.append(para)
                break
    
    if matching_paragraphs:
        return '\n\n'.join(matching_paragraphs)
    
    return None


def extract_clause_with_ai(
    contract_text: str,
    clause_type: str,
    api_key: str
) -> Optional[Dict]:
    """
    Extract and analyze specific clause using AI.
    
    Args:
        contract_text: Contract text
        clause_type: Type of clause to extract
        api_key: Anthropic API key
        
    Returns:
        Clause analysis dictionary or None
    """
    if not api_key:
        return None
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        prompt = get_clause_extraction_prompt(contract_text, clause_type)
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        
        analysis = response.content[0].text
        
        return {
            'clause_type': clause_type,
            'analysis': analysis,
            'found': 'not found' not in analysis.lower()
        }
        
    except Exception as e:
        print(f"Clause extraction failed: {e}")
        return None

def analyze_specific_clause(
    contract_text: str,
    clause_type: str,
    api_key: str,
    language: str = 'en'
) -> Dict:
    """
    Comprehensive analysis of a specific clause type.
    
    Args:
        contract_text: Full contract text
        clause_type: Type of clause to analyze
        api_key: Anthropic API key
        language: Response language
        
    Returns:
        Structured clause analysis
    """
    if not api_key:
        # Fallback to keyword-based extraction
        clause_text = find_clause_by_keyword(contract_text, clause_type)
        
        if clause_text:
            return {
                'found': True,
                'clause_type': clause_type,
                'clause_text': clause_text,
                'location': 'Found via keyword matching',
                'summary': 'AI analysis unavailable - API key required',
                'risk_level': 'UNKNOWN',
                'risks': [],
                'favorability': 'NEUTRAL',
                'recommendations': [],
                'analysis': 'Configure API key for detailed AI analysis'
            }
        else:
            return {
                'found': False,
                'clause_type': clause_type,
                'analysis': f'No {clause_type} clause found. This is a significant gap in the contract.'
            }
    
    # Use AI for comprehensive analysis
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        
        prompt = f"""Analyze the {clause_type} clause in this contract.

CONTRACT:
{contract_text}

Provide a comprehensive analysis in this format:

1. CLAUSE FOUND: Yes/No

2. CLAUSE TEXT: [Extract the exact text of the {clause_type} clause]

3. LOCATION: [Section/paragraph number if identifiable]

4. PLAIN LANGUAGE SUMMARY: [Explain what this clause means in simple terms]

5. RISK ASSESSMENT:
   - Risk Level: CRITICAL/HIGH/MEDIUM/LOW/MINIMAL
   - Specific Risks: [List any concerns]

6. FAVORABILITY: FAVORABLE/NEUTRAL/UNFAVORABLE
   [Explain who this clause favors]

7. RECOMMENDATIONS:
   - [Specific suggestions for improvement]
   - [Negotiation points]
   - [Red flags to address]

Language: {"Swedish" if language == 'sv' else "English"}
Be specific and practical."""
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=3000,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        
        analysis_text = response.content[0].text
        
        # Parse the response
        result = parse_clause_analysis(analysis_text, clause_type)
        result['raw_analysis'] = analysis_text
        
        return result
        
    except Exception as e:
        print(f"Clause analysis failed: {e}")
        return {
            'found': False,
            'clause_type': clause_type,
            'analysis': f'Analysis failed: {str(e)}'
        }


def parse_clause_analysis(analysis_text: str, clause_type: str) -> Dict:
    """Parse AI clause analysis into structured format."""
    
    result = {
        'found': False,
        'clause_type': clause_type,
        'clause_text': '',
        'location': '',
        'summary': '',
        'risk_level': 'UNKNOWN',
        'risks': [],
        'favorability': 'NEUTRAL',
        'recommendations': [],
        'analysis': analysis_text
    }
    
    # Check if clause was found
    if 'CLAUSE FOUND: Yes' in analysis_text or 'found: yes' in analysis_text.lower():
        result['found'] = True
    
    # Extract sections
    lines = analysis_text.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        
        if 'CLAUSE TEXT:' in line.upper():
            current_section = 'clause_text'
            continue
        elif 'LOCATION:' in line.upper():
            current_section = 'location'
            continue
        elif 'PLAIN LANGUAGE' in line.upper() or 'SUMMARY:' in line.upper():
            current_section = 'summary'
            continue
        elif 'RISK LEVEL:' in line.upper():
            # Extract risk level
            for level in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'MINIMAL']:
                if level in line.upper():
                    result['risk_level'] = level
                    break
            continue
        elif 'SPECIFIC RISKS:' in line.upper() or 'RISKS:' in line.upper():
            current_section = 'risks'
            continue
        elif 'FAVORABILITY:' in line.upper():
            for fav in ['FAVORABLE', 'UNFAVORABLE', 'NEUTRAL']:
                if fav in line.upper():
                    result['favorability'] = fav
                    break
            current_section = 'favorability'
            continue
        elif 'RECOMMENDATIONS:' in line.upper():
            current_section = 'recommendations'
            continue
        
        # Add content to current section
        if current_section and line:
            if current_section == 'clause_text':
                result['clause_text'] += line + '\n'
            elif current_section == 'location':
                result['location'] += line + ' '
            elif current_section == 'summary':
                result['summary'] += line + ' '
            elif current_section == 'risks':
                if line.startswith('-') or line.startswith('•'):
                    result['risks'].append(line.lstrip('-• '))
            elif current_section == 'recommendations':
                if line.startswith('-') or line.startswith('•') or line[0].isdigit():
                    result['recommendations'].append(line.lstrip('-•0123456789. '))
    
    # Clean up
    result['clause_text'] = result['clause_text'].strip()
    result['location'] = result['location'].strip()
    result['summary'] = result['summary'].strip()
    
    return result

def extract_key_dates(contract_text: str) -> List[Dict]:
    """
    Extract important dates from contract.
    
    Args:
        contract_text: Contract text
        
    Returns:
        List of date dictionaries
    """
    dates = []
    
    # Common date patterns
    date_patterns = [
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # DD/MM/YYYY or MM-DD-YYYY
        r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',    # YYYY-MM-DD
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b'
    ]
    
    for pattern in date_patterns:
        matches = re.finditer(pattern, contract_text, re.IGNORECASE)
        for match in matches:
            # Get context around date
            start = max(0, match.start() - 100)
            end = min(len(contract_text), match.end() + 100)
            context = contract_text[start:end]
            
            dates.append({
                'date': match.group(),
                'context': context.strip()
            })
    
    return dates


def extract_parties(contract_text: str) -> List[str]:
    """
    Extract party names from contract.
    
    Args:
        contract_text: Contract text
        
    Returns:
        List of party names
    """
    parties = []
    
    # Look for common party indicators
    party_patterns = [
        r'between\s+([A-Z][A-Za-z\s&,\.]+)\s+(?:and|&)',
        r'Party:\s*([A-Z][A-Za-z\s&,\.]+)',
        r'Client:\s*([A-Z][A-Za-z\s&,\.]+)',
        r'Vendor:\s*([A-Z][A-Za-z\s&,\.]+)',
        r'Company:\s*([A-Z][A-Za-z\s&,\.]+)'
    ]
    
    for pattern in party_patterns:
        matches = re.finditer(pattern, contract_text)
        for match in matches:
            party = match.group(1).strip()
            if len(party) > 3 and party not in parties:  # Avoid short matches
                parties.append(party)
    
    return parties[:10]  # Limit to 10 parties


def extract_amounts(contract_text: str) -> List[Dict]:
    """
    Extract monetary amounts from contract.
    
    Args:
        contract_text: Contract text
        
    Returns:
        List of amount dictionaries
    """
    amounts = []
    
    # Currency patterns
    currency_patterns = [
        r'\$\s*[\d,]+(?:\.\d{2})?',  # $1,000.00
        r'[\d,]+(?:\.\d{2})?\s*(?:SEK|USD|EUR|GBP)',  # 1000 SEK
        r'(?:SEK|USD|EUR|GBP)\s*[\d,]+(?:\.\d{2})?',  # SEK 1000
    ]
    
    for pattern in currency_patterns:
        matches = re.finditer(pattern, contract_text, re.IGNORECASE)
        for match in matches:
            # Get context
            start = max(0, match.start() - 80)
            end = min(len(contract_text), match.end() + 80)
            context = contract_text[start:end]
            
            amounts.append({
                'amount': match.group(),
                'context': context.strip()
            })
    
    return amounts[:20]  # Limit to 20 amounts