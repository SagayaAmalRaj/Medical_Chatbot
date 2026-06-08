"""
AI Tools Configuration Module
Defines all function calling tools for OpenAI API
"""

FUNCTION_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "register_new_patient",
            "description": "Register a new patient in the system and get a patient ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Patient's full name"
                    },
                    "age": {
                        "type": "integer",
                        "description": "Patient's age in years"
                    },
                    "phone": {
                        "type": "string",
                        "description": "Patient's phone number (optional)"
                    },
                    "email": {
                        "type": "string",
                        "description": "Patient's email address (optional)"
                    },
                    "gender": {
                        "type": "string",
                        "description": "Patient's gender: Male, Female, Other, or Prefer not to say (optional)"
                    }
                },
                "required": ["name", "age"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_doctors",
            "description": "Get a list of available doctors, optionally filtered by name or specialty",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Optional search query to filter doctors by name or specialty"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_doctor_availability",
            "description": "Get availability for a specific doctor by name or ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "doctor_name": {
                        "type": "string",
                        "description": "The name or ID of the doctor to check availability for"
                    }
                },
                "required": ["doctor_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_patients",
            "description": "Get list of all patients (for identification purposes)",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_availability_by_specialty",
            "description": "Check available appointments by medical specialty and optional date range",
            "parameters": {
                "type": "object",
                "properties": {
                    "specialty": {
                        "type": "string",
                        "description": "Medical specialty (e.g., 'Dermatology', 'Cardiology', 'General Medicine', 'ENT')"
                    },
                    "date": {
                        "type": "string",
                        "description": "Optional specific date in YYYY-MM-DD format"
                    },
                    "date_range": {
                        "type": "integer",
                        "description": "Number of days to check from today (default: 7)"
                    }
                },
                "required": ["specialty"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "book_appointment",
            "description": "Book an appointment for the patient. Use doctor ID (like 'D-04') or doctor name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "doctor_id": {
                        "type": "string",
                        "description": "Doctor ID (e.g., 'D-04') or doctor name (e.g., 'Kumar', 'Dr. Kumar')"
                    },
                    "date": {
                        "type": "string",
                        "description": "Appointment date in YYYY-MM-DD format"
                    },
                    "time": {
                        "type": "string",
                        "description": "Appointment time in HH:MM format (e.g., '09:00')"
                    }
                },
                "required": ["doctor_id", "date", "time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "view_appointments",
            "description": "View all appointments for the current patient",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_appointment",
            "description": "Cancel an existing appointment by appointment ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "appointment_id": {
                        "type": "string",
                        "description": "Appointment ID to cancel (e.g., 'A-2001')"
                    }
                },
                "required": ["appointment_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "reschedule_appointment",
            "description": "Reschedule an existing appointment to a new date and time",
            "parameters": {
                "type": "object",
                "properties": {
                    "appointment_id": {
                        "type": "string",
                        "description": "Appointment ID to reschedule (e.g., 'A-2001')"
                    },
                    "new_date": {
                        "type": "string",
                        "description": "New appointment date in YYYY-MM-DD format"
                    },
                    "new_time": {
                        "type": "string",
                        "description": "New appointment time in HH:MM format (e.g., '10:00')"
                    }
                },
                "required": ["appointment_id", "new_date", "new_time"]
            }
        }
    }
]