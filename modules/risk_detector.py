"""
Risk detection and scoring

Copyright (c) 2025 Mattias Nyqvist
Licensed under the MIT License
"""

from typing import List, Dict
import re


def detect_payment_risks(contract_text: str) -> List[Dict]:
    """
    Detect payment-related risks.
    
    Args:
        contract_text: Contract text
        
    Returns:
        List of detected payment risks
    """
    risks = []
    text_lower = contract_text.lower()
    
    # Check for payment terms
    if 'payment' not in text_lower and 'fee' not in text_lower:
        risks.append({
            'level': 'HIGH',
            'category': 'Payment Terms',
            'description': 'No clear payment terms found',
            'impact': 'Unclear payment obligations could lead to disputes'
        })
    
    # Check for late payment penalties
    if 'late payment' not in text_lower and 'overdue' not in text_lower:
        risks.append({
            'level': 'MEDIUM',
            'category': 'Payment Terms',
            'description': 'No late payment terms specified',
            'impact': 'No protection against delayed payments'
        })
    
    # Check for payment schedule
    if 'payment schedule' not in text_lower and 'installment' not in text_lower:
        risks.append({
            'level': 'LOW',
            'category': 'Payment Terms',
            'description': 'No detailed payment schedule',
            'impact': 'May cause confusion about when payments are due'
        })
    
    return risks


def detect_liability_risks(contract_text: str) -> List[Dict]:
    """
    Detect liability-related risks.
    
    Args:
        contract_text: Contract text
        
    Returns:
        List of detected liability risks
    """
    risks = []
    text_lower = contract_text.lower()
    
    # Check for liability cap
    if 'liability' in text_lower:
        if 'unlimited liability' in text_lower or 'no limit' in text_lower:
            risks.append({
                'level': 'CRITICAL',
                'category': 'Liability',
                'description': 'Unlimited liability clause detected',
                'impact': 'Unlimited financial exposure in case of breach'
            })
        elif 'cap' not in text_lower and 'limit' not in text_lower:
            risks.append({
                'level': 'HIGH',
                'category': 'Liability',
                'description': 'No liability cap specified',
                'impact': 'Potentially unlimited financial exposure'
            })
    
    # Check for indemnification
    if 'indemnif' in text_lower:
        if 'indemnify' in text_lower and 'hold harmless' in text_lower:
            risks.append({
                'level': 'MEDIUM',
                'category': 'Liability',
                'description': 'Broad indemnification clause present',
                'impact': 'May be required to cover third-party claims'
            })
    
    return risks


def detect_termination_risks(contract_text: str) -> List[Dict]:
    """
    Detect termination-related risks.
    
    Args:
        contract_text: Contract text
        
    Returns:
        List of detected termination risks
    """
    risks = []
    text_lower = contract_text.lower()
    
    # Check for termination clause
    if 'termination' not in text_lower and 'cancel' not in text_lower:
        risks.append({
            'level': 'HIGH',
            'category': 'Termination',
            'description': 'No termination clause found',
            'impact': 'Unclear how to exit the contract'
        })
    
    # Check for notice period
    if 'notice' not in text_lower and 'termination' in text_lower:
        risks.append({
            'level': 'MEDIUM',
            'category': 'Termination',
            'description': 'No notice period specified',
            'impact': 'Unclear how much advance notice is required'
        })
    
    # Check for termination penalty
    if 'early termination' in text_lower:
        if 'penalty' in text_lower or 'fee' in text_lower:
            risks.append({
                'level': 'MEDIUM',
                'category': 'Termination',
                'description': 'Early termination penalty exists',
                'impact': 'Cost to exit contract before term ends'
            })
    
    return risks


def detect_missing_clauses(contract_text: str) -> List[str]:
    """
    Detect commonly missing important clauses.
    
    Args:
        contract_text: Contract text
        
    Returns:
        List of missing clause types
    """
    text_lower = contract_text.lower()
    missing = []
    
    important_clauses = {
        'Confidentiality': ['confidential', 'non-disclosure', 'proprietary'],
        'Intellectual Property': ['intellectual property', 'ip rights', 'ownership'],
        'Dispute Resolution': ['dispute', 'arbitration', 'mediation'],
        'Force Majeure': ['force majeure', 'act of god'],
        'Governing Law': ['governing law', 'jurisdiction'],
        'Warranties': ['warrant', 'guarantee'],
        'Non-Compete': ['non-compete', 'non-competition'],
        'Assignment': ['assignment', 'transfer of rights']
    }
    
    for clause_type, keywords in important_clauses.items():
        found = False
        for keyword in keywords:
            if keyword in text_lower:
                found = True
                break
        
        if not found:
            missing.append(clause_type)
    
    return missing


def calculate_overall_risk_score(risks: List[Dict]) -> str:
    """
    Calculate overall risk level based on individual risks.
    
    Args:
        risks: List of risk dictionaries
        
    Returns:
        Overall risk level (CRITICAL/HIGH/MEDIUM/LOW/MINIMAL)
    """
    if not risks:
        return 'MINIMAL'
    
    risk_scores = {
        'CRITICAL': 100,
        'HIGH': 50,
        'MEDIUM': 20,
        'LOW': 5,
        'MINIMAL': 0
    }
    
    # Calculate weighted score
    total_score = sum(risk_scores.get(risk.get('level', 'MEDIUM'), 20) for risk in risks)
    
    # Determine overall level
    if total_score >= 100:
        return 'CRITICAL'
    elif total_score >= 50:
        return 'HIGH'
    elif total_score >= 20:
        return 'MEDIUM'
    elif total_score > 0:
        return 'LOW'
    else:
        return 'MINIMAL'


def generate_automated_recommendations(risks: List[Dict], missing_clauses: List[str]) -> List[str]:
    """
    Generate automated recommendations based on detected risks.
    
    Args:
        risks: List of detected risks
        missing_clauses: List of missing clauses
        
    Returns:
        List of recommendation strings
    """
    recommendations = []
    
    # Recommendations based on risk categories
    risk_categories = set(risk.get('category', '') for risk in risks)
    
    if 'Payment Terms' in risk_categories:
        recommendations.append(
            "Review and clarify payment terms. Specify exact amounts, due dates, and payment methods."
        )
        recommendations.append(
            "Add late payment penalty clause to protect against delayed payments."
        )
    
    if 'Liability' in risk_categories:
        recommendations.append(
            "Negotiate a liability cap to limit financial exposure (e.g., total fees paid in last 12 months)."
        )
        recommendations.append(
            "Review and potentially limit indemnification obligations."
        )
    
    if 'Termination' in risk_categories:
        recommendations.append(
            "Clarify termination rights and notice periods for both parties."
        )
        recommendations.append(
            "Negotiate to reduce or remove early termination penalties."
        )
    
    # Recommendations for missing clauses
    if 'Confidentiality' in missing_clauses:
        recommendations.append(
            "Add confidentiality clause to protect sensitive business information."
        )
    
    if 'Dispute Resolution' in missing_clauses:
        recommendations.append(
            "Include dispute resolution clause specifying arbitration or mediation process."
        )
    
    if 'Force Majeure' in missing_clauses:
        recommendations.append(
            "Add force majeure clause to protect against unforeseen circumstances."
        )
    
    if 'Governing Law' in missing_clauses:
        recommendations.append(
            "Specify governing law and jurisdiction for legal disputes."
        )
    
    if 'Intellectual Property' in missing_clauses:
        recommendations.append(
            "Clarify intellectual property ownership and usage rights."
        )
    
    # General recommendations
    if len(risks) > 10:
        recommendations.append(
            "Consider having this contract reviewed by a legal professional due to high number of identified risks."
        )
    
    return recommendations[:10]  # Limit to top 10 recommendations


def run_automated_risk_detection(contract_text: str) -> Dict:
    """
    Run all automated risk detection checks.
    
    Args:
        contract_text: Contract text
        
    Returns:
        Dictionary with all detected risks
    """
    all_risks = []
    
    # Detect various risk types
    all_risks.extend(detect_payment_risks(contract_text))
    all_risks.extend(detect_liability_risks(contract_text))
    all_risks.extend(detect_termination_risks(contract_text))
    
    # Detect missing clauses
    missing = detect_missing_clauses(contract_text)
    
    # Calculate overall risk
    overall_risk = calculate_overall_risk_score(all_risks)
    
    # Generate recommendations
    recommendations = generate_automated_recommendations(all_risks, missing)
    
    return {
        'risks': all_risks,
        'missing_clauses': missing,
        'overall_risk': overall_risk,
        'risk_count': len(all_risks),
        'recommendations': recommendations
    }