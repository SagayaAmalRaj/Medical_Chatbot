"""
Data Manager Module
Handles all JSON file operations and data persistence
"""
import json
import os
from typing import Dict, List, Any

DATA_DIR = "data"


def ensure_data_dir():
    """Create data directory if it doesn't exist"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_data(filename: str) -> Dict:
    """
    Load JSON data from file
    
    Args:
        filename: Name of the JSON file in the data directory
        
    Returns:
        Dictionary containing the loaded data
    """
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return default empty structures
        if "doctors" in filename:
            return {"doctors": []}
        elif "patients" in filename:
            return {"patients": []}
        elif "appointments" in filename:
            return {"appointments": []}
        elif "availability" in filename:
            return {"availability": []}
        return {}


def save_data(filename: str, data: Dict):
    """
    Save data to JSON file
    
    Args:
        filename: Name of the JSON file to save in data directory
        data: Dictionary to save
    """
    ensure_data_dir()
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def file_exists(filename: str) -> bool:
    """
    Check if a data file exists
    
    Args:
        filename: Name of the JSON file
        
    Returns:
        True if file exists, False otherwise
    """
    filepath = os.path.join(DATA_DIR, filename)
    return os.path.exists(filepath)