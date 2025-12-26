"""
Input validation utilities

Copyright (c) 2025 Mattias Nyqvist
Licensed under the MIT License
"""

import os
from typing import Tuple, Optional


def validate_file_upload(file) -> Tuple[bool, Optional[str]]:
    """
    Validate uploaded file.
    
    Args:
        file: Streamlit uploaded file object
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if file is None:
        return False, "No file uploaded"
    
    # Check file extension
    file_ext = file.name.split('.')[-1].lower()
    allowed_extensions = ['pdf', 'docx', 'doc']
    
    if file_ext not in allowed_extensions:
        return False, f"Unsupported file type: .{file_ext}. Please upload PDF or DOCX files."
    
    # Check file size (max 200MB)
    max_size = 200 * 1024 * 1024  # 200MB in bytes
    file_size = file.size if hasattr(file, 'size') else 0
    
    if file_size > max_size:
        return False, f"File too large ({file_size / (1024*1024):.1f}MB). Maximum size is 200MB."
    
    return True, None


def validate_api_key(api_key: str) -> bool:
    """
    Validate Anthropic API key format.
    
    Args:
        api_key: API key string
        
    Returns:
        True if valid format
    """
    if not api_key:
        return False
    
    # Anthropic keys start with 'sk-ant-'
    if not api_key.startswith('sk-ant-'):
        return False
    
    # Should have reasonable length
    if len(api_key) < 20:
        return False
    
    return True


def validate_contract_text(text: str) -> Tuple[bool, Optional[str]]:
    """
    Validate extracted contract text.
    
    Args:
        text: Contract text
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not text or len(text.strip()) == 0:
        return False, "Contract appears to be empty"
    
    # Minimum reasonable length (500 characters)
    if len(text) < 500:
        return False, "Contract text is too short. This might not be a complete contract."
    
    # Maximum reasonable length (500,000 characters ~ 100k words)
    if len(text) > 500000:
        return False, "Contract text is too long. Please upload a shorter document."
    
    return True, None