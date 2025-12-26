"""
AI prompts for contract analysis

Copyright (c) 2025 Mattias Nyqvist
Licensed under the MIT License
"""

def get_analysis_prompt(contract_text: str, language: str = 'en') -> str:
    """
    Generate prompt for contract analysis.
    
    Args:
        contract_text: Full contract text
        language: Response language ('en' or 'sv')
        
    Returns:
        Formatted prompt for Claude
    """
    
    lang_instruction = {
        'en': 'Respond in English.',
        'sv': 'Respond in Swedish.'
    }
    
    return f"""You are an expert legal contract analyst. Analyze the following contract and provide a comprehensive risk assessment.

CONTRACT TEXT:
{contract_text}

Please provide your analysis in the following format:

1. EXECUTIVE SUMMARY
   - Brief overview of the contract (2-3 sentences)
   - Contract type and parties involved
   - Overall risk level (CRITICAL/HIGH/MEDIUM/LOW/MINIMAL)

2. KEY TERMS
   - Payment terms and amounts
   - Contract duration and dates
   - Deliverables or obligations
   - Important deadlines

3. RISK ASSESSMENT
   For each identified risk, provide:
   - Risk Level: CRITICAL/HIGH/MEDIUM/LOW/MINIMAL
   - Category: (Payment, Liability, Termination, etc.)
   - Description: What is the risk?
   - Impact: What could go wrong?
   - Do NOT include recommendations here - save them for section 6

4. RED FLAGS
   - Missing critical clauses
   - Unusual or unfavorable terms
   - Potential legal issues
   - Ambiguous language

5. MISSING CLAUSES
   - Important clauses that should be present but are missing
   - Why each missing clause is important

6. RECOMMENDATIONS
   IMPORTANT: This must be a SEPARATE section with standalone recommendations.
   Do NOT embed recommendations within risk descriptions above.
   
   Provide 5-10 clear, actionable recommendations:
   1. [First recommendation - complete sentence]
   2. [Second recommendation - complete sentence]
   3. [Third recommendation - complete sentence]
   ...
   
   Each recommendation should be:
   - A complete, standalone statement
   - Specific and actionable
   - Focused on mitigating identified risks
   - Prioritized by importance

{lang_instruction[language]}

Be specific, practical, and focus on business impact. Use clear, non-legal language where possible."""


def get_clause_extraction_prompt(contract_text: str, clause_type: str) -> str:
    """
    Generate prompt for extracting specific clause type.
    
    Args:
        contract_text: Full contract text
        clause_type: Type of clause to extract
        
    Returns:
        Formatted prompt
    """
    
    return f"""Extract and analyze the {clause_type} clause(s) from this contract.

CONTRACT TEXT:
{contract_text}

For each {clause_type} clause found, provide:
1. Exact text of the clause
2. Location in contract (section/paragraph number if available)
3. Summary in plain language
4. Potential risks or concerns
5. Whether this is favorable, neutral, or unfavorable

If no {clause_type} clause is found, explain why this is concerning and what should be included."""


def get_comparison_prompt(contract1: str, contract2: str, language: str = 'en') -> str:
    """
    Generate prompt for comparing two contracts.
    
    Args:
        contract1: First contract text
        contract2: Second contract text
        language: Response language
        
    Returns:
        Formatted prompt
    """
    
    lang_instruction = {
        'en': 'Respond in English.',
        'sv': 'Respond in Swedish.'
    }
    
    return f"""Compare these two contracts and identify key differences.

CONTRACT 1:
{contract1}

CONTRACT 2:
{contract2}

Provide comparison in this format:

1. KEY DIFFERENCES
   - Payment terms
   - Liability and warranties
   - Termination conditions
   - Other significant differences

2. RISK COMPARISON
   - Which contract has higher overall risk?
   - Specific risks in Contract 1 vs Contract 2
   - Recommendations on which terms are more favorable

3. MISSING IN EACH
   - Clauses present in Contract 1 but missing in Contract 2
   - Clauses present in Contract 2 but missing in Contract 1

4. RECOMMENDATION
   - Which contract is more favorable and why?
   - Key negotiation points if combining elements

{lang_instruction[language]}

Be specific and focus on business impact."""