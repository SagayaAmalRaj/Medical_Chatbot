"""
Patient Management Module
Handles all patient-related operations including new patient registration
"""
from typing import List, Dict, Optional
from data_manager import load_data, save_data


PATIENTS_FILE = "patients.json"


def get_patients() -> List[Dict]:
    """
    Get all patients
    
    Returns:
        List of all patient dictionaries
    """
    data = load_data(PATIENTS_FILE)
    return data.get("patients", [])


def get_patient_by_id(patient_id: str) -> Optional[Dict]:
    """
    Get patient information by ID
    
    Args:
        patient_id: The patient's ID
        
    Returns:
        Patient dictionary if found, None otherwise
    """
    patients = get_patients()
    for patient in patients:
        if patient.get("patient_id") == patient_id:
            return patient
    return None


def find_patient_by_name(name: str) -> Optional[Dict]:
    """
    Find patient by name (fuzzy match)
    
    Args:
        name: Patient name (or partial name)
        
    Returns:
        Patient dictionary if single match found, None otherwise
    """
    patients = get_patients()
    input_name = name.lower().strip()
    input_words = set(input_name.split())
    
    best_matches = []
    
    for patient in patients:
        patient_name = patient.get("name", "").lower().strip()
        patient_words = set(patient_name.split())
        
        # Exact match
        if patient_name == input_name:
            return patient
        
        # Fuzzy match by common words
        common_words = input_words.intersection(patient_words)
        if common_words:
            score = len(common_words) / max(len(input_words), len(patient_words))
            best_matches.append((score, patient))
    
    # Return best match if score is high enough
    if best_matches:
        best_matches.sort(key=lambda x: x[0], reverse=True)
        if best_matches[0][0] >= 0.5:  # At least 50% match
            return best_matches[0][1]
    
    return None


def patient_exists(patient_id: str) -> bool:
    """
    Check if a patient exists
    
    Args:
        patient_id: The patient's ID
        
    Returns:
        True if patient exists, False otherwise
    """
    return get_patient_by_id(patient_id) is not None


def generate_patient_id() -> str:
    """
    Generate next available patient ID
    
    Returns:
        Next patient ID in format P-XXXX
    """
    patients = get_patients()
    
    if not patients:
        return "P-0001"
    
    # Extract numbers from patient IDs
    existing_ids = []
    for patient in patients:
        try:
            patient_id = patient.get("patient_id", "")
            if patient_id.startswith("P-"):
                num = int(patient_id.split("-")[1])
                existing_ids.append(num)
        except (ValueError, IndexError):
            continue
    
    # Get next ID
    next_num = max(existing_ids) + 1 if existing_ids else 1
    return f"P-{next_num:04d}"


def create_new_patient(name: str, age: int, phone: str = "", 
                       email: str = "", gender: str = "") -> Dict:
    """
    Create a new patient record
    
    Args:
        name: Patient full name
        age: Patient age
        phone: Patient phone number (optional)
        email: Patient email (optional)
        gender: Patient gender (optional)
        
    Returns:
        Dictionary with the created patient or error info
    """
    # Validate inputs
    if not name or not isinstance(name, str) or len(name.strip()) == 0:
        return {"error": "Patient name is required"}
    
    if not isinstance(age, int) or age < 0 or age > 150:
        return {"error": "Age must be a valid number between 0 and 150"}
    
    # Generate new patient ID
    patient_id = generate_patient_id()
    
    # Create patient object
    new_patient = {
        "patient_id": patient_id,
        "name": name.strip(),
        "age": age,
        "phone": phone.strip() if phone else "",
        "email": email.strip() if email else "",
        "gender": gender.strip() if gender else ""
    }
    
    # Load existing patients
    data = load_data(PATIENTS_FILE)
    patients = data.get("patients", [])
    
    # Add new patient
    patients.append(new_patient)
    data["patients"] = patients
    
    # Save updated data
    save_data(PATIENTS_FILE, data)
    
    return new_patient


def get_all_patient_fields() -> Dict:
    """
    Get all fields available for patient registration
    
    Returns:
        Dictionary with field names and their properties
    """
    return {
        "name": {
            "label": "Full Name",
            "type": "text",
            "required": True,
            "help": "Patient's full name"
        },
        "age": {
            "label": "Age",
            "type": "number",
            "required": True,
            "help": "Patient's age in years"
        },
        "phone": {
            "label": "Phone Number",
            "type": "text",
            "required": False,
            "help": "Contact phone number (optional)"
        },
        "email": {
            "label": "Email",
            "type": "email",
            "required": False,
            "help": "Email address (optional)"
        },
        "gender": {
            "label": "Gender",
            "type": "select",
            "options": ["Male", "Female", "Other", "Prefer not to say"],
            "required": False,
            "help": "Gender (optional)"
        }
    }