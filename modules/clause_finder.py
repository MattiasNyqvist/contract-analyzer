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