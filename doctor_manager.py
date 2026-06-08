"""
Doctor Management Module
Handles all doctor-related operations
"""
from typing import List, Dict, Optional
from data_manager import load_data


DOCTORS_FILE = "doctors.json"


def get_doctors(query: str = "") -> str:
    """
    Get list of all doctors, optionally filtered by query
    
    Args:
        query: Optional search query to filter by name or specialty
        
    Returns:
        Formatted string with doctor information
    """
    data = load_data(DOCTORS_FILE)
    doctors = data.get("doctors", [])
    
    if query:
        query = query.lower()
        doctors = [d for d in doctors 
                  if query in d.get("name", "").lower() 
                  or query in d.get("specialty", "").lower()]
    
    if not doctors:
        return "No doctors found."
    
    result = "Available doctors:\n"
    for doctor in doctors:
        result += (f"• {doctor.get('name', 'Unknown')} - "
                  f"{doctor.get('specialty', 'N/A')} "
                  f"(ID: {doctor.get('doctor_id', 'N/A')}) "
                  f"Fee: ₹{doctor.get('consultation_fee', 'N/A')}\n")
    
    return result.strip()


def find_doctor_by_name_or_id(doctor_identifier: str) -> Optional[Dict]:
    """
    Find a doctor by ID or name (fuzzy match)
    
    Args:
        doctor_identifier: Doctor ID or name
        
    Returns:
        Doctor dictionary if found, None otherwise
    """
    data = load_data(DOCTORS_FILE)
    doctors = data.get("doctors", [])
    
    # First try exact ID match
    for doctor in doctors:
        if doctor.get("doctor_id") == doctor_identifier:
            return doctor
    
    # Then try fuzzy name match
    matching_doctors = []
    identifier_lower = doctor_identifier.lower()
    
    for doctor in doctors:
        doctor_name = doctor.get("name", "").lower()
        # Check if identifier matches any part of the name
        if identifier_lower in doctor_name or doctor_name in identifier_lower:
            matching_doctors.append(doctor)
    
    # Return single match, None if multiple or no match
    return matching_doctors[0] if len(matching_doctors) == 1 else None


def get_doctor_by_id(doctor_id: str) -> Optional[Dict]:
    """
    Get doctor information by exact ID
    
    Args:
        doctor_id: The doctor's ID
        
    Returns:
        Doctor dictionary if found, None otherwise
    """
    data = load_data(DOCTORS_FILE)
    doctors = data.get("doctors", [])
    
    for doctor in doctors:
        if doctor.get("doctor_id") == doctor_id:
            return doctor
    
    return None


def get_all_doctors() -> List[Dict]:
    """
    Get all doctors
    
    Returns:
        List of all doctor dictionaries
    """
    data = load_data(DOCTORS_FILE)
    return data.get("doctors", [])


def get_doctors_by_specialty(specialty: str) -> List[Dict]:
    """
    Get all doctors with a specific specialty
    
    Args:
        specialty: Medical specialty to filter by
        
    Returns:
        List of doctor dictionaries
    """
    all_doctors = get_all_doctors()
    specialty_lower = specialty.lower()
    
    return [d for d in all_doctors 
            if specialty_lower in d.get("specialty", "").lower()]