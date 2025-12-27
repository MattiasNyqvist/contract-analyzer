"""
Clause extraction and analysis

Copyright (c) 2025 Mattias Nyqvist
Licensed under the MIT License
"""

from typing import Dict, List
import re


def find_clause_by_keyword(contract_text: str, clause_type: str) -> str:
    """
    Find clause using keyword matching.
    
    Args:
        contract_text: Full contract text
        clause_type: Type of clause to find
        
    Returns:
        Extracted clause text or empty string
    """
    # Define keywords for each clause type
    keywords = {
        'Payment Terms': ['payment', 'fee', 'compensation', 'invoice'],
        'Liability': ['liability', 'liable', 'damages', 'indemnif'],
        'Termination': ['termination', 'terminate', 'cancel'],
        'Confidentiality': ['confidential', 'proprietary', 'non-disclosure'],
        'Intellectual Property': ['intellectual property', 'ip rights', 'copyright', 'ownership'],
        'Warranties': ['warrant', 'guarantee', 'representation'],
        'Indemnification': ['indemnif', 'hold harmless'],
        'Dispute Resolution': ['dispute', 'arbitration', 'mediation'],
        'Force Majeure': ['force majeure', 'act of god'],
        'Non-Compete': ['non-compete', 'non-competition'],
        'Governing Law': ['governing law', 'jurisdiction']
    }
    
    clause_keywords = keywords.get(clause_type, [])
    
    # Search for sections containing keywords
    paragraphs = contract_text.split('\n\n')
    relevant_paragraphs = []
    
    for para in paragraphs:
        para_lower = para.lower()
        if any(keyword in para_lower for keyword in clause_keywords):
            relevant_paragraphs.append(para)
    
    return '\n\n'.join(relevant_paragraphs[:3]) if relevant_paragraphs else ''


def extract_clause_with_ai(
    contract_text: str,
    clause_type: str,
    api_key: str
) -> Dict:
    """
    Extract clause using AI.
    
    Args:
        contract_text: Full contract text
        clause_type: Type of clause
        api_key: Anthropic API key
        
    Returns:
        Clause extraction results
    """
    from config.prompts import get_clause_extraction_prompt
    import anthropic
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        prompt = get_clause_extraction_prompt(contract_text, clause_type)
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return {
            'clause_type': clause_type,
            'analysis': response.content[0].text
        }
        
    except Exception as e:
        return {
            'clause_type': clause_type,
            'analysis': f'Extraction failed: {str(e)}'
        }


def extract_key_dates(contract_text: str) -> List[str]:
    """
    Extract important dates from contract.
    
    Args:
        contract_text: Contract text
        
    Returns:
        List of identified dates
    """
    # Common date patterns
    date_patterns = [
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # MM/DD/YYYY or DD-MM-YYYY
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
        r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b'
    ]
    
    dates = []
    for pattern in date_patterns:
        dates.extend(re.findall(pattern, contract_text, re.IGNORECASE))
    
    return list(set(dates))[:10]  # Return unique dates, max 10


def extract_parties(contract_text: str) -> List[str]:
    """
    Extract party names from contract.
    
    Args:
        contract_text: Contract text
        
    Returns:
        List of identified parties
    """
    # Look for common patterns
    parties = []
    
    # Pattern: "between X and Y"
    between_pattern = r'between\s+([^,\(]+?)(?:\s+\([^\)]+\))?\s+and\s+([^,\(]+?)(?:\s+\([^\)]+\))?(?:\s|,|\.)'
    matches = re.findall(between_pattern, contract_text, re.IGNORECASE)
    
    for match in matches[:2]:  # Take first 2 matches
        parties.extend([m.strip() for m in match])
    
    return parties[:4]  # Max 4 parties


def extract_amounts(contract_text: str) -> List[str]:
    """
    Extract monetary amounts from contract.
    
    Args:
        contract_text: Contract text
        
    Returns:
        List of identified amounts
    """
    # Patterns for different currencies
    amount_patterns = [
        r'\$\s*[\d,]+(?:\.\d{2})?',  # USD
        r'€\s*[\d,]+(?:\.\d{2})?',   # EUR
        r'£\s*[\d,]+(?:\.\d{2})?',   # GBP
        r'SEK\s*[\d,]+(?:\.\d{2})?', # SEK
        r'[\d,]+(?:\.\d{2})?\s*(?:USD|EUR|GBP|SEK)',
    ]
    
    amounts = []
    for pattern in amount_patterns:
        amounts.extend(re.findall(pattern, contract_text, re.IGNORECASE))
    
    return list(set(amounts))[:10]  # Return unique amounts, max 10


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
        
        lang_text = {
            'en': 'English',
            'sv': 'Swedish'
        }
        
        lang_instruction = {
            'en': 'IMPORTANT: Respond in English.',
            'sv': 'VIKTIGT: Svara på svenska.'
        }
        
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

{lang_instruction[language]}
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
    if 'CLAUSE FOUND: Yes' in analysis_text or 'CLAUSE FOUND: yes' in analysis_text or 'found: yes' in analysis_text.lower():
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
        elif 'RECOMMENDATIONS:' in line.upper() or 'RECOMMENDATION:' in line.upper():
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