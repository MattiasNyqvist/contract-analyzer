"""
Application configuration and constants

Copyright (c) 2025 Mattias Nyqvist
Licensed under the MIT License
"""

# App metadata
APP_TITLE = "Contract Analyzer"
APP_ICON = "📋"
APP_DESCRIPTION = "AI-powered contract analysis for risk detection and clause evaluation"

# File upload settings
MAX_FILE_SIZE_MB = 200
ALLOWED_EXTENSIONS = ['pdf', 'docx', 'doc']

# Risk levels
RISK_LEVELS = {
    'CRITICAL': {'color': '#dc2626', 'label': 'Critical Risk'},
    'HIGH': {'color': '#ea580c', 'label': 'High Risk'},
    'MEDIUM': {'color': '#f59e0b', 'label': 'Medium Risk'},
    'LOW': {'color': '#059669', 'label': 'Low Risk'},
    'MINIMAL': {'color': '#0891b2', 'label': 'Minimal Risk'}
}

# Clause types
CLAUSE_TYPES = [
    'Payment Terms',
    'Liability',
    'Termination',
    'Confidentiality',
    'Intellectual Property',
    'Warranties',
    'Indemnification',
    'Dispute Resolution',
    'Force Majeure',
    'Non-Compete',
    'Governing Law'
]

# Language options
LANGUAGES = {
    'en': 'English',
    'sv': 'Swedish'
}

# Number format options
NUMBER_FORMATS = {
    'swedish': {'separator': ' ', 'decimal': ',', 'label': 'Swedish (10 000,50)'},
    'international': {'separator': ',', 'decimal': '.', 'label': 'International (10,000.50)'}
}