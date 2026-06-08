"""
Appointment Management Module
Handles all appointment-related operations
"""
from typing import Optional, Dict, List
from data_manager import load_data, save_data
from doctor_manager import find_doctor_by_name_or_id, get_doctor_by_id
from availability_manager import (
    book_slot, release_slot, is_slot_available, 
    get_available_slots
)


APPOINTMENTS_FILE = "appointments.json"


def book_appointment(patient_id: str, doctor_identifier: str, date: str, time: str) -> str:
    """
    Book an appointment for a patient
    
    Args:
        patient_id: Patient ID
        doctor_identifier: Doctor ID or name
        date: Date in YYYY-MM-DD format
        time: Time in HH:MM format
        
    Returns:
        Message indicating success or failure
    """
    # Find the doctor
    doctor = find_doctor_by_name_or_id(doctor_identifier)
    if not doctor:
        return f"Doctor '{doctor_identifier}' not found."
    
    doctor_id = doctor.get("doctor_id")
    doctor_name = doctor.get("name", "Unknown")
    
    # Check if slot is available
    if not is_slot_available(doctor_id, date, time):
        available = get_available_slots(doctor_id, date)
        available_str = ', '.join(available) if available else "None"
        return f"Time {time} on {date} is not available. Available: {available_str}"
    
    # Check for existing appointment at same time
    appointments_data = load_data(APPOINTMENTS_FILE)
    for appt in appointments_data.get("appointments", []):
        if (appt.get("doctor_id") == doctor_id and 
            appt.get("date") == date and 
            appt.get("time") == time):
            return f"Time {time} on {date} is already booked."
    
    # Generate new appointment ID
    existing_ids = []
    for appt in appointments_data.get("appointments", []):
        try:
            appt_num = int(appt.get("appt_id", "").split("-")[1])
            existing_ids.append(appt_num)
        except (ValueError, IndexError):
            continue
    
    new_id = max(existing_ids) + 1 if existing_ids else 2001
    appt_id = f"A-{new_id}"
    
    # Create appointment
    new_appointment = {
        "appt_id": appt_id,
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "date": date,
        "time": time
    }
    
    # Book the slot and save appointment
    if book_slot(doctor_id, date, time):
        appointments_data["appointments"].append(new_appointment)
        save_data(APPOINTMENTS_FILE, appointments_data)
        
        return (f"Appointment {appt_id} booked successfully with {doctor_name} "
               f"on {date} at {time}.")
    else:
        return f"Failed to book appointment. Please try again."


def view_appointments(patient_id: str) -> str:
    """
    View all appointments for a patient
    
    Args:
        patient_id: Patient ID
        
    Returns:
        Formatted string with appointment details
    """
    appointments_data = load_data(APPOINTMENTS_FILE)
    patient_appointments = [a for a in appointments_data.get("appointments", [])
                           if a.get("patient_id") == patient_id]
    
    if not patient_appointments:
        return "You have no upcoming appointments."
    
    result = "Your appointments:\n"
    for appt in patient_appointments:
        doctor = get_doctor_by_id(appt.get("doctor_id"))
        doctor_name = doctor.get("name", "Unknown") if doctor else "Unknown"
        result += (f"• Appointment {appt.get('appt_id')}: "
                  f"{doctor_name} on {appt.get('date')} at {appt.get('time')}\n")
    
    return result.strip()


def cancel_appointment(patient_id: str, appointment_id: str) -> str:
    """
    Cancel an appointment
    
    Args:
        patient_id: Patient ID
        appointment_id: Appointment ID to cancel
        
    Returns:
        Message indicating success or failure
    """
    appointments_data = load_data(APPOINTMENTS_FILE)
    
    # Find the appointment
    appointment = None
    for appt in appointments_data.get("appointments", []):
        if (appt.get("appt_id") == appointment_id and 
            appt.get("patient_id") == patient_id):
            appointment = appt
            break
    
    if not appointment:
        return f"Appointment {appointment_id} not found."
    
    # Release the slot
    doctor_id = appointment.get("doctor_id")
    date = appointment.get("date")
    time = appointment.get("time")
    
    release_slot(doctor_id, date, time)
    
    # Remove appointment
    appointments_data["appointments"] = [
        a for a in appointments_data.get("appointments", [])
        if a.get("appt_id") != appointment_id
    ]
    save_data(APPOINTMENTS_FILE, appointments_data)
    
    doctor = get_doctor_by_id(doctor_id)
    doctor_name = doctor.get("name", "Unknown") if doctor else "Unknown"
    
    return (f"Appointment {appointment_id} with {doctor_name} "
           f"on {date} at {time} has been cancelled.")


def reschedule_appointment(patient_id: str, appointment_id: str, 
                          new_date: str, new_time: str) -> str:
    """
    Reschedule an appointment to a new date and time
    
    Args:
        patient_id: Patient ID
        appointment_id: Appointment ID to reschedule
        new_date: New date in YYYY-MM-DD format
        new_time: New time in HH:MM format
        
    Returns:
        Message indicating success or failure
    """
    appointments_data = load_data(APPOINTMENTS_FILE)
    
    # Find the appointment
    appointment = None
    for appt in appointments_data.get("appointments", []):
        if (appt.get("appt_id") == appointment_id and 
            appt.get("patient_id") == patient_id):
            appointment = appt
            break
    
    if not appointment:
        return f"Appointment {appointment_id} not found."
    
    doctor_id = appointment.get("doctor_id")
    doctor = get_doctor_by_id(doctor_id)
    doctor_name = doctor.get("name", "Unknown") if doctor else "Unknown"
    
    # Check if new slot is available
    if not is_slot_available(doctor_id, new_date, new_time):
        available = get_available_slots(doctor_id, new_date)
        available_str = ', '.join(available) if available else "None"
        return f"Time {new_time} on {new_date} is not available. Available: {available_str}"
    
    # Check for conflicts
    for appt in appointments_data.get("appointments", []):
        if (appt.get("doctor_id") == doctor_id and 
            appt.get("date") == new_date and 
            appt.get("time") == new_time and 
            appt.get("appt_id") != appointment_id):
            return f"Time {new_time} on {new_date} is already booked."
    
    # Release old slot
    release_slot(doctor_id, appointment.get("date"), appointment.get("time"))
    
    # Book new slot
    book_slot(doctor_id, new_date, new_time)
    
    # Update appointment
    old_date, old_time = appointment.get("date"), appointment.get("time")
    appointment["date"] = new_date
    appointment["time"] = new_time
    save_data(APPOINTMENTS_FILE, appointments_data)
    
    return (f"Appointment {appointment_id} rescheduled from {old_date} at {old_time} "
           f"to {new_date} at {new_time} with {doctor_name}.")


def get_appointment(appointment_id: str, patient_id: str) -> Optional[Dict]:
    """
    Get appointment details
    
    Args:
        appointment_id: Appointment ID
        patient_id: Patient ID (for security)
        
    Returns:
        Appointment dictionary if found, None otherwise
    """
    appointments_data = load_data(APPOINTMENTS_FILE)
    
    for appt in appointments_data.get("appointments", []):
        if (appt.get("appt_id") == appointment_id and 
            appt.get("patient_id") == patient_id):
            return appt
    
    return None
