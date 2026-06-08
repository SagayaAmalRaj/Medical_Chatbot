"""
Medical Appointment Voice Assistant
Main Streamlit Application with Patient Registration
"""
import streamlit as st
import speech_recognition as sr
import pyttsx3
import openai
import re
from datetime import datetime
import os

# Import configuration
from config import (
    OPENAI_API_KEY, GPT_MODEL, APP_TITLE, SYSTEM_PROMPT,
    VOICE_TIMEOUT, VOICE_PHRASE_TIME_LIMIT, MICROPHONE_ADJUSTMENT_DURATION
)

# Import business logic modules
from doctor_manager import get_doctors, find_doctor_by_name_or_id
from patient_manager import (
    get_patients, get_patient_by_id, find_patient_by_name, 
    create_new_patient, get_all_patient_fields
)
from appointment_manager import (
    book_appointment, view_appointments, cancel_appointment, reschedule_appointment
)
from availability_manager import (
    get_doctor_availability, check_availability_by_specialty,
    initialize_availability_for_all_doctors
)
from ai_tools import FUNCTION_TOOLS
from data_manager import ensure_data_dir

# Set API key
openai.api_key = OPENAI_API_KEY


class MedicalAssistant:
    """Main medical appointment assistant class"""
    
    def __init__(self):
        """Initialize the assistant with voice and session state"""
        # Initialize session state
        if 'messages' not in st.session_state:
            st.session_state.messages = [
                {'role': "system", 'content': SYSTEM_PROMPT}
            ]
        
        if 'session_context' not in st.session_state:
            st.session_state.session_context = {
                'current_patient': None,
                'last_doctor': None,
                'last_doctor_id': None,
                'last_specialty': None,
                'is_new_patient': False
            }
        
        if 'conversation_history' not in st.session_state:
            st.session_state.conversation_history = []
        
        # Initialize voice
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.tts_engine = pyttsx3.init()
            self.setup_microphone()
        except Exception as e:
            st.error(f"Voice initialization failed: {e}")
    
    def setup_microphone(self):
        """Adjust microphone for ambient noise"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(
                    source, duration=MICROPHONE_ADJUSTMENT_DURATION
                )
        except Exception as e:
            st.error(f"Microphone setup failed: {e}")
    
    def listen_for_voice(self):
        """Capture voice input from user"""
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source, timeout=VOICE_TIMEOUT, 
                    phrase_time_limit=VOICE_PHRASE_TIME_LIMIT
                )
            
            user_input = self.recognizer.recognize_google(audio)
            return user_input.lower()
        
        except sr.WaitTimeoutError:
            return "TIMEOUT"
        except sr.UnknownValueError:
            return "UNCLEAR"
        except sr.RequestError as e:
            return f"ERROR: {e}"
    
    def extract_patient_info(self, user_input: str) -> dict:
        """Extract patient identification from user input"""
        # Check for patient ID (e.g., P-1001)
        patient_id_match = re.search(r'P-\d+', user_input.upper())
        if patient_id_match:
            return {'type': 'id', 'value': patient_id_match.group()}
        
        # Check for patient name patterns
        name_patterns = [
            r"I'?m\s+([A-Za-z\s]+?)(?:\s+(?:and|i|want|to|book|appointment|with|for|from|need|looking|seeking|schedule)\b|$)",
            r"my name is\s+([A-Za-z\s]+?)(?:\s+(?:and|i|want|to|book|appointment|with|for|from|need|looking|seeking|schedule)\b|$)",
            r"this is\s+([A-Za-z\s]+?)(?:\s+(?:and|i|want|to|book|appointment|with|for|from|need|looking|seeking|schedule)\b|$)",
            r"I am\s+([A-Za-z\s]+?)(?:\s+(?:and|i|want|to|book|appointment|with|for|from|need|looking|seeking|schedule)\b|$)"
        ]
        
        for pattern in name_patterns:
            name_match = re.search(pattern, user_input, re.IGNORECASE)
            if name_match:
                name = name_match.group(1).strip()
                name = re.sub(r'\b(speaking|calling|here)\b', '', name).strip()
                name_words = name.split()
                if 1 <= len(name_words) <= 4 and all(len(word) >= 2 for word in name_words):
                    return {'type': 'name', 'value': name}
        
        return None
    
    def identify_patient(self, user_input: str) -> str:
        """Identify patient from user input"""
        patient_info = self.extract_patient_info(user_input)
        
        if not patient_info:
            return "I couldn't identify your name. Could you please tell me your name?"
        
        if patient_info['type'] == 'id':
            patient = get_patient_by_id(patient_info['value'])
            if patient:
                st.session_state.session_context['current_patient'] = patient
                st.session_state.session_context['is_new_patient'] = False
                return f"Hello {patient.get('name')}! How can I help you today?"
            else:
                return f"Patient {patient_info['value']} not found."
        
        elif patient_info['type'] == 'name':
            patient = find_patient_by_name(patient_info['value'])
            if patient:
                st.session_state.session_context['current_patient'] = patient
                st.session_state.session_context['is_new_patient'] = False
                return f"Hello {patient.get('name')}! How can I help you today?"
            else:
                return f"I couldn't find a patient named {patient_info['value']}. Would you like to register as a new patient?"
        
        return "Unable to identify you. Please try again."
    
    def process_function_call(self, function_name: str, arguments: dict) -> str:
        """Process function calls from AI"""
        try:
            if function_name == "register_new_patient":
                # Create new patient
                result = create_new_patient(
                    name=arguments.get("name", ""),
                    age=arguments.get("age", 0),
                    phone=arguments.get("phone", ""),
                    email=arguments.get("email", ""),
                    gender=arguments.get("gender", "")
                )
                
                if "error" in result:
                    return f"Registration failed: {result['error']}"
                
                # Set as current patient
                st.session_state.session_context['current_patient'] = result
                st.session_state.session_context['is_new_patient'] = True
                
                patient_id = result.get("patient_id")
                patient_name = result.get("name")
                return (f"Patient {patient_name} registered successfully! "
                       f"Your patient ID is {patient_id}. "
                       f"How can I help you with your appointment?")
            
            elif function_name == "get_doctors":
                return get_doctors(arguments.get("query", ""))
            
            elif function_name == "get_doctor_availability":
                return get_doctor_availability(arguments.get("doctor_name", ""))
            
            elif function_name == "get_patients":
                patients = get_patients()
                result = "Registered patients:\n"
                for patient in patients:
                    result += f"• {patient.get('name')} (ID: {patient.get('patient_id')})\n"
                return result.strip()
            
            elif function_name == "check_availability_by_specialty":
                return check_availability_by_specialty(
                    arguments.get("specialty", ""),
                    arguments.get("date", ""),
                    arguments.get("date_range", 7)
                )
            
            elif function_name == "book_appointment":
                patient = st.session_state.session_context.get('current_patient')
                if not patient:
                    return "Please identify yourself first before booking."
                
                return book_appointment(
                    patient.get("patient_id"),
                    arguments.get("doctor_id", ""),
                    arguments.get("date", ""),
                    arguments.get("time", "")
                )
            
            elif function_name == "view_appointments":
                patient = st.session_state.session_context.get('current_patient')
                if not patient:
                    return "Please identify yourself first."
                
                return view_appointments(patient.get("patient_id"))
            
            elif function_name == "cancel_appointment":
                patient = st.session_state.session_context.get('current_patient')
                if not patient:
                    return "Please identify yourself first."
                
                return cancel_appointment(
                    patient.get("patient_id"),
                    arguments.get("appointment_id", "")
                )
            
            elif function_name == "reschedule_appointment":
                patient = st.session_state.session_context.get('current_patient')
                if not patient:
                    return "Please identify yourself first."
                
                return reschedule_appointment(
                    patient.get("patient_id"),
                    arguments.get("appointment_id", ""),
                    arguments.get("new_date", ""),
                    arguments.get("new_time", "")
                )
            
            return f"Unknown function: {function_name}"
        
        except Exception as e:
            return f"Error processing function: {str(e)}"
    
    def handle_response(self, user_input: str) -> str:
        """Handle user input and generate response"""
        # Check if user is identifying themselves
        if any(keyword in user_input.lower() for keyword in 
               ['my name', "i'm", 'i am', 'this is', 'i am patient']):
            identification_response = self.identify_patient(user_input)
            st.session_state.messages.append(
                {"role": "user", "content": user_input}
            )
            st.session_state.messages.append(
                {"role": "assistant", "content": identification_response}
            )
            return identification_response
        
        # Regular conversation with AI
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )
        
        # Get response from OpenAI with function calling
        try:
            response = openai.ChatCompletion.create(
                model=GPT_MODEL,
                messages=st.session_state.messages,
                tools=FUNCTION_TOOLS,
                tool_choice="auto"
            )
            
            response_message = response["choices"][0]["message"]
            
            # Handle function calls
            while response_message.get("tool_calls"):
                function_call = response_message["tool_calls"][0]
                function_name = function_call["function"]["name"]
                function_args = eval(function_call["function"]["arguments"])
                
                # Process function call
                function_result = self.process_function_call(function_name, function_args)
                
                # Add function result to conversation
                st.session_state.messages.append(response_message)
                st.session_state.messages.append({
                    "role": "tool",
                    "tool_call_id": function_call["id"],
                    "name": function_name,
                    "content": function_result
                })
                
                # Get next response
                response = openai.ChatCompletion.create(
                    model=GPT_MODEL,
                    messages=st.session_state.messages,
                    tools=FUNCTION_TOOLS,
                    tool_choice="auto"
                )
                
                response_message = response["choices"][0]["message"]
            
            # Extract final text response
            if "content" in response_message and response_message["content"]:
                final_response = response_message["content"]
            else:
                final_response = "I couldn't process that request. Please try again."
            
            # Add to conversation history
            st.session_state.messages.append({
                "role": "assistant",
                "content": final_response
            })
            
            return final_response
        
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            st.error(error_msg)
            return error_msg


def main():
    """Main Streamlit app function"""
    # Ensure data directory exists
    ensure_data_dir()
    
    # Initialize availability for all doctors on first run
    if 'availability_initialized' not in st.session_state:
        with st.spinner("Initializing doctor availability..."):
            initialize_availability_for_all_doctors(num_days=7)
        st.session_state.availability_initialized = True
    
    # Initialize assistant
    assistant = MedicalAssistant()
    
    # Page configuration
    st.set_page_config(
        page_title="Medical Chatbot",
        page_icon="🏥",
        layout="wide"
    )
    
    # Main title
    st.title(APP_TITLE)
    st.markdown("---")
    
    # Sidebar with session info and new patient registration
    with st.sidebar:
        st.header("Session Information")
        
        patient = st.session_state.session_context.get('current_patient')
        if patient:
            st.success(f"Patient: {patient.get('name')}")
            st.info(f"ID: {patient.get('patient_id')}")
            st.info(f"Age: {patient.get('age')}")
        else:
            st.warning("No patient identified yet")
        
        st.markdown("---")
        st.header("📝 New Patient Registration")
        
        # Registration form
        with st.form("new_patient_form", clear_on_submit=True):
            reg_name = st.text_input("Full Name", placeholder="Enter your full name")
            reg_age = st.number_input("Age", min_value=0, max_value=150, value=25)
            reg_phone = st.text_input("Phone Number (Optional)", placeholder="+91-XXXXXXXXXX")
            reg_email = st.text_input("Email (Optional)", placeholder="your.email@example.com")
            reg_gender = st.selectbox("Gender (Optional)", 
                                     ["", "Male", "Female", "Other", "Prefer not to say"])
            
            reg_submit = st.form_submit_button("Register New Patient", type="primary")
        
        if reg_submit and reg_name:
            with st.spinner("Registering patient..."):
                result = create_new_patient(
                    name=reg_name,
                    age=int(reg_age),
                    phone=reg_phone,
                    email=reg_email,
                    gender=reg_gender
                )
                
                if "error" not in result:
                    st.session_state.session_context['current_patient'] = result
                    st.session_state.session_context['is_new_patient'] = True
                    st.success(f"✅ Registered! Patient ID: {result.get('patient_id')}")
                    st.rerun()
                else:
                    st.error(f"❌ {result['error']}")
        
        st.markdown("---")
        
        if st.button("🔄 Reset Session", type="secondary"):
            for key in ['messages', 'session_context', 'conversation_history']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    # Conversation history display
    st.header("💬 Conversation")
    
    if st.session_state.conversation_history:
        for user_msg, ai_response, timestamp in st.session_state.conversation_history:
            st.markdown(f"**You** ({timestamp}): {user_msg}")
            st.markdown(f"**Assistant**: {ai_response}")
            st.markdown("---")
    else:
        st.info("💡 Start by identifying yourself or registering as a new patient")
    
    # Input section
    st.header("💭 Send Your Message")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        with st.form("text_input_form", clear_on_submit=True):
            user_input = st.text_input(
                "Type your message:",
                placeholder="e.g., My name is John, I need an appointment",
                key="text_input"
            )
            submit_btn = st.form_submit_button("💌 Send", type="primary")
    
    with col2:
        if st.button("🎤 Voice Input", type="primary"):
            with st.spinner("🎧 Listening..."):
                voice_result = assistant.listen_for_voice()
                
                if voice_result == "TIMEOUT":
                    st.warning("No speech detected. Please try again.")
                elif voice_result == "UNCLEAR":
                    st.warning("Couldn't understand. Please speak clearly.")
                elif voice_result.startswith("ERROR"):
                    st.error(f"Error: {voice_result}")
                else:
                    st.success(f"Heard: {voice_result}")
                    with st.spinner("Processing..."):
                        response = assistant.handle_response(voice_result)
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        st.session_state.conversation_history.append(
                            (voice_result, response, timestamp)
                        )
                        st.rerun()
    
    # Process text submission
    if submit_btn and user_input.strip():
        with st.spinner("Processing..."):
            response = assistant.handle_response(user_input.strip())
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state.conversation_history.append(
                (user_input, response, timestamp)
            )
            st.rerun()
    
    # Quick actions
    st.markdown("---")
    st.header("⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📅 My Appointments", use_container_width=True):
            patient = st.session_state.session_context.get('current_patient')
            if patient:
                response = assistant.handle_response("Show my appointments")
                timestamp = datetime.now().strftime("%H:%M:%S")
                st.session_state.conversation_history.append(
                    ("Show my appointments", response, timestamp)
                )
                st.rerun()
            else:
                st.warning("Please identify yourself first!")
    
    with col2:
        if st.button("🔍 Find Doctors", use_container_width=True):
            response = assistant.handle_response("Show available doctors")
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state.conversation_history.append(
                ("Show available doctors", response, timestamp)
            )
            st.rerun()
    
    with col3:
        if st.button("❓ Help", use_container_width=True):
            help_text = """
            **What I can help with:**
            
            - **Register**: Use the form in the sidebar or say "Register me"
            - **Identify**: Say 'I'm [Your Name]' or use your patient ID
            - **Check availability**: 'Show available doctors' or 'Find [specialty]'
            - **Book appointment**: 'Book with Dr. [Name] on [date] at [time]'
            - **View appointments**: 'Show my appointments'
            - **Cancel appointment**: 'Cancel appointment [ID]'
            - **Reschedule**: 'Reschedule [appointment ID] to [date] at [time]'
            
            Use voice (🎤) or text for all commands!
            """
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state.conversation_history.append(
                ("Help", help_text, timestamp)
            )
            st.rerun()


if __name__ == "__main__":
    main()