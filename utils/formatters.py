"""
Text and number formatting utilities

Copyright (c) 2025 Mattias Nyqvist
Licensed under the MIT License
"""

import streamlit as st


def format_number(number: float, decimals: int = 0) -> str:
    """
    Format number based on user preference.
    
    Args:
        number: Number to format
        decimals: Number of decimal places
        
    Returns:
        Formatted number string
    """
    if not number or number == 0:
        return "0"
    
    # Get user preference from session state (default: swedish)
    num_format = st.session_state.get('number_format', 'swedish')
    
    if num_format == 'swedish':
        # Swedish: space separator, comma decimal
        if decimals == 0:
            formatted = f"{number:,.0f}".replace(',', ' ')
        else:
            formatted = f"{number:,.{decimals}f}".replace(',', '|').replace('.', ',').replace('|', ' ')
    else:
        # International: comma separator, period decimal
        if decimals == 0:
            formatted = f"{number:,.0f}"
        else:
            formatted = f"{number:,.{decimals}f}"
    
    return formatted


def format_currency(amount: float, currency: str = 'SEK') -> str:
    """
    Format currency amount.
    
    Args:
        amount: Amount to format
        currency: Currency code (SEK, USD, EUR, etc.)
        
    Returns:
        Formatted currency string
    """
    formatted_number = format_number(amount, decimals=2)
    
    currency_symbols = {
        'SEK': 'kr',
        'USD': '$',
        'EUR': '€',
        'GBP': '£'
    }
    
    symbol = currency_symbols.get(currency, currency)
    
    # For SEK, put symbol after number (Swedish style)
    if currency == 'SEK':
        return f"{formatted_number} {symbol}"
    else:
        return f"{symbol}{formatted_number}"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def get_risk_color(risk_level: str) -> str:
    """
    Get color for risk level.
    
    Args:
        risk_level: Risk level (CRITICAL/HIGH/MEDIUM/LOW/MINIMAL)
        
    Returns:
        Hex color code
    """
    from config.settings import RISK_LEVELS
    
    return RISK_LEVELS.get(risk_level.upper(), {}).get('color', '#6b7280')