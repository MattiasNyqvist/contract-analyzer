"""
File upload and handling

Copyright (c) 2025 Mattias Nyqvist
Licensed under the MIT License
"""

import streamlit as st
from typing import Optional
from utils.validators import validate_file_upload


def render_file_uploader() -> Optional[object]:
    """
    Render file upload widget.
    
    Returns:
        Uploaded file object or None
    """
    uploaded_file = st.file_uploader(
        "Upload Contract",
        type=['pdf', 'docx', 'doc'],
        help="Upload a PDF or Word document containing the contract to analyze",
        key="contract_uploader"
    )
    
    if uploaded_file is not None:
        # Validate file
        is_valid, error_message = validate_file_upload(uploaded_file)
        
        if not is_valid:
            st.error(error_message)
            return None
        
        return uploaded_file
    
    return None


def save_uploaded_file(uploaded_file, save_path: str = "uploads") -> str:
    """
    Save uploaded file to disk.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        save_path: Directory to save file
        
    Returns:
        Path to saved file
    """
    import os
    
    # Create directory if it doesn't exist
    os.makedirs(save_path, exist_ok=True)
    
    # Generate file path
    file_path = os.path.join(save_path, uploaded_file.name)
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path