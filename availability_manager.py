"""
Availability Management Module
Handles doctor availability and appointment scheduling with auto-generation
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from data_manager import load_data, save_data
from doctor_manager import find_doctor_by_name_or_id, get_doctor_by_id, get_all_doctors


AVAILABILITY_FILE = "availability.json"
APPOINTMENTS_FILE = "appointments.json"

# Doctor working hours
MORNING_START = "09:30"  # 9:30 AM
EVENING_END = "18:30"    # 6:30 PM
SLOT_DURATION_MINUTES = 30


def time_to_minutes(time_str: str) -> int:
    """Convert time string HH:MM to minutes since midnight"""
    try:
        hours, minutes = map(int, time_str.split(":"))
        return hours * 60 + minutes
    except ValueError:
        return 0


def minutes_to_time(minutes: int) -> str:
    """Convert minutes since midnight to HH:MM format"""
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"


def generate_time_slots(start_time: str, end_time: str, slot_duration: int = 30) -> List[str]:
    """
    Generate time slots from start to end time
    
    Args:
        start_time: Start time in HH:MM format
        end_time: End time in HH:MM format
        slot_duration: Duration of each slot in minutes (default: 30)
        
    Returns:
        List of time slots
    """
    slots = []
    start_minutes = time_to_minutes(start_time)
    end_minutes = time_to_minutes(end_time)
    
    current_minutes = start_minutes
    while current_minutes + slot_duration <= end_minutes:
        slots.append(minutes_to_time(current_minutes))
        current_minutes += slot_duration
    
    return slots


def get_booked_slots(doctor_id: str, date: str) -> List[str]:
    """
    Get all booked time slots for a doctor on a specific date
    
    Args:
        doctor_id: Doctor ID
        date: Date in YYYY-MM-DD format
        
    Returns:
        List of booked time slots
    """
    appointments = load_data(APPOINTMENTS_FILE)
    booked_slots = []
    
    for appt in appointments.get("appointments", []):
        if (appt.get("doctor_id") == doctor_id and 
            appt.get("date") == date):
            booked_slots.append(appt.get("time"))
    
    return booked_slots


def generate_availability_for_doctor(doctor_id: str, num_days: int = 7) -> List[Dict]:
    """
    Generate availability for a doctor for next N days
    
    Args:
        doctor_id: Doctor ID
        num_days: Number of days to generate availability for (default: 7)
        
    Returns:
        List of availability dictionaries
    """
    doctor = get_doctor_by_id(doctor_id)
    if not doctor:
        return []
    
    availability_list = []
    today = datetime.now().date()
    
    # Generate slots for each day
    for day_offset in range(num_days):
        current_date = today + timedelta(days=day_offset)
        date_str = current_date.strftime("%Y-%m-%d")
        
        # Skip past days (only for today onwards)
        if current_date < today:
            continue
        
        # Generate all possible time slots
        all_slots = generate_time_slots(MORNING_START, EVENING_END, SLOT_DURATION_MINUTES)
        
        # Get already booked slots
        booked_slots = get_booked_slots(doctor_id, date_str)
        
        # Filter out booked slots
        available_slots = [slot for slot in all_slots if slot not in booked_slots]
        
        # Create availability entry
        if available_slots:  # Only add if there are available slots
            availability_list.append({
                "doctor_id": doctor_id,
                "doctor_name": doctor.get("name", "Unknown"),
                "date": date_str,
                "slots": available_slots
            })
    
    return availability_list


def initialize_availability_for_all_doctors(num_days: int = 7) -> bool:
    """
    Initialize availability for all doctors for next N days
    
    Args:
        num_days: Number of days to generate (default: 7)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        all_doctors = get_all_doctors()
        all_availability = []
        
        for doctor in all_doctors:
            doctor_id = doctor.get("doctor_id")
            availability = generate_availability_for_doctor(doctor_id, num_days)
            all_availability.extend(availability)
        
        # Save availability
        if all_availability:
            data = {"availability": all_availability}
            save_data(AVAILABILITY_FILE, data)
            return True
        
        return False
    
    except Exception as e:
        print(f"Error initializing availability: {e}")
        return False


def refresh_availability_for_doctor(doctor_id: str, num_days: int = 7) -> bool:
    """
    Refresh availability for a specific doctor
    
    Args:
        doctor_id: Doctor ID
        num_days: Number of days to generate (default: 7)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Load current availability
        data = load_data(AVAILABILITY_FILE)
        current_availability = data.get("availability", [])
        
        # Remove old entries for this doctor
        current_availability = [
            a for a in current_availability 
            if a.get("doctor_id") != doctor_id
        ]
        
        # Generate new availability
        new_availability = generate_availability_for_doctor(doctor_id, num_days)
        current_availability.extend(new_availability)
        
        # Save updated availability
        data["availability"] = current_availability
        save_data(AVAILABILITY_FILE, data)
        
        return True
    
    except Exception as e:
        print(f"Error refreshing availability: {e}")
        return False


def get_doctor_availability(doctor_name: str) -> str:
    """
    Get availability for a specific doctor
    
    Args:
        doctor_name: Doctor name or ID
        
    Returns:
        Formatted string with availability
    """
    doctor = find_doctor_by_name_or_id(doctor_name)
    
    if not doctor:
        return f"Doctor '{doctor_name}' not found."
    
    doctor_id = doctor.get("doctor_id")
    doctor_full_name = doctor.get("name", "Unknown")
    
    data = load_data(AVAILABILITY_FILE)
    availability = [a for a in data.get("availability", []) 
                   if a.get("doctor_id") == doctor_id]
    
    if not availability:
        return f"No availability for {doctor_full_name}."
    
    result = f"Availability for {doctor_full_name} (ID: {doctor_id}):\n"
    today = datetime.now().date()
    
    for avail in availability:
        try:
            date_obj = datetime.strptime(avail.get("date", ""), "%Y-%m-%d").date()
            if date_obj >= today and avail.get("slots"):
                slots = ', '.join(avail.get("slots", []))
                result += f"• {avail.get('date')} ({date_obj.strftime('%A')}): {slots}\n"
        except ValueError:
            continue
    
    return result.strip()


def check_availability_by_specialty(specialty: str, date: str = "", date_range: int = 7) -> str:
    """
    Check available appointments by medical specialty
    
    Args:
        specialty: Medical specialty to search for
        date: Optional specific date in YYYY-MM-DD format
        date_range: Number of days to search from today (default: 7)
        
    Returns:
        Formatted string with availability
    """
    all_doctors = get_all_doctors()
    specialist_doctors = [d for d in all_doctors 
                         if specialty.lower() in d.get("specialty", "").lower()]
    
    if not specialist_doctors:
        return f"No doctors found for specialty '{specialty}'."
    
    doctor_ids = [d.get("doctor_id") for d in specialist_doctors]
    
    data = load_data(AVAILABILITY_FILE)
    availability = [a for a in data.get("availability", []) 
                   if a.get("doctor_id") in doctor_ids]
    
    # Filter by date if specified
    if date:
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d").date()
            availability = [a for a in availability 
                           if datetime.strptime(a.get("date", ""), "%Y-%m-%d").date() == target_date]
        except ValueError:
            return f"Invalid date format: {date}. Please use YYYY-MM-DD."
    else:
        today = datetime.now().date()
        end_date = today + timedelta(days=date_range)
        availability = [a for a in availability 
                       if today <= datetime.strptime(a.get("date", ""), "%Y-%m-%d").date() <= end_date]
    
    if not availability:
        return f"No availability found for {specialty}."
    
    result = f"Available slots for {specialty}:\n"
    for avail in availability:
        if avail.get("slots"):
            doctor = get_doctor_by_id(avail.get("doctor_id"))
            if doctor:
                doctor_name = doctor.get("name", "Unknown")
                doctor_id = doctor.get("doctor_id")
                slots = ', '.join(avail.get("slots", []))
                result += f"• {doctor_name} (ID: {doctor_id}) on {avail.get('date')}: {slots}\n"
    
    return result.strip()


def is_slot_available(doctor_id: str, date: str, time: str) -> bool:
    """
    Check if a specific slot is available
    
    Args:
        doctor_id: Doctor ID
        date: Date in YYYY-MM-DD format
        time: Time in HH:MM format
        
    Returns:
        True if slot is available, False otherwise
    """
    data = load_data(AVAILABILITY_FILE)
    
    for avail in data.get("availability", []):
        if (avail.get("doctor_id") == doctor_id and 
            avail.get("date") == date):
            return time in avail.get("slots", [])
    
    return False


def get_available_slots(doctor_id: str, date: str) -> List[str]:
    """
    Get all available slots for a doctor on a specific date
    
    Args:
        doctor_id: Doctor ID
        date: Date in YYYY-MM-DD format
        
    Returns:
        List of available time slots
    """
    data = load_data(AVAILABILITY_FILE)
    
    for avail in data.get("availability", []):
        if (avail.get("doctor_id") == doctor_id and 
            avail.get("date") == date):
            return avail.get("slots", [])
    
    return []


def book_slot(doctor_id: str, date: str, time: str) -> bool:
    """
    Book a time slot (remove from availability)
    
    Args:
        doctor_id: Doctor ID
        date: Date in YYYY-MM-DD format
        time: Time in HH:MM format
        
    Returns:
        True if slot was booked successfully, False otherwise
    """
    data = load_data(AVAILABILITY_FILE)
    
    for avail in data.get("availability", []):
        if (avail.get("doctor_id") == doctor_id and 
            avail.get("date") == date):
            if time in avail.get("slots", []):
                avail["slots"].remove(time)
                save_data(AVAILABILITY_FILE, data)
                return True
    
    return False


def release_slot(doctor_id: str, date: str, time: str):
    """
    Release a time slot (add back to availability)
    
    Args:
        doctor_id: Doctor ID
        date: Date in YYYY-MM-DD format
        time: Time in HH:MM format
    """
    data = load_data(AVAILABILITY_FILE)
    
    for avail in data.get("availability", []):
        if (avail.get("doctor_id") == doctor_id and 
            avail.get("date") == date):
            if time not in avail.get("slots", []):
                avail["slots"].append(time)
                avail["slots"].sort()
                save_data(AVAILABILITY_FILE, data)
                return