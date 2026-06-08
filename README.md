<<<<<<< HEAD
# Medical Appointment Voice Assistant

A production-ready voice-enabled Streamlit chatbot for managing medical appointments. Built with modular architecture for scalability and maintainability.

## Features

✨ **Core Features:**
- 🗣️ **Voice Input** - Speak naturally to the assistant
- 🔍 **Doctor Search** - Find doctors by specialty or name
- 📅 **Appointment Management** - Book, view, cancel, and reschedule appointments
- 🎤 **Voice Output** - Text-to-speech responses
- 🔐 **Patient Identification** - Secure patient identification
- 💬 **Conversational AI** - OpenAI-powered natural language understanding

## Project Structure

```
medical-chatbot/
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration and settings
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
│
├── data/                      # Data storage (auto-created)
│   ├── doctors.json          # Doctor information
│   ├── patients.json         # Patient information
│   ├── appointments.json     # Appointment records
│   └── availability.json     # Doctor availability slots
│
└── Core Modules:
    ├── data_manager.py       # JSON file operations
    ├── doctor_manager.py     # Doctor-related functions
    ├── patient_manager.py    # Patient-related functions
    ├── appointment_manager.py# Appointment operations
    ├── availability_manager.py# Availability and scheduling
    └── ai_tools.py           # OpenAI function calling tools
```

## Installation

### Prerequisites
- Python 3.8+
- pip
- Microphone (for voice input)

### Setup Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd medical-chatbot
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
```

5. **Add your OpenAI API key to `.env`**
```
OPENAI_API_KEY=sk-...your-key-here...
```

6. **Run the application**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Usage

### Starting the App
```bash
streamlit run app.py
```

### Voice Interaction
1. Click **"🎤 Voice Input"** button
2. Speak clearly into your microphone
3. Wait for the assistant to process your request

### Text Interaction
1. Type your message in the text input field
2. Click **"💌 Send"** button
3. View the assistant's response

### Common Commands

**Identify Yourself:**
- "My name is John Doe"
- "I'm Sarah Wilson"
- "I am P-1001"

**Check Availability:**
- "Show available doctors"
- "Find dermatologists"
- "Check availability for cardiology"

**Book Appointments:**
- "Book appointment with Dr. Shah"
- "Schedule with D-02 tomorrow at 9 AM"

**Manage Appointments:**
- "Show my appointments"
- "Cancel appointment A-2001"
- "Reschedule A-2001 to tomorrow at 10 AM"

## Module Documentation

### data_manager.py
Handles all JSON file operations and data persistence.

**Key Functions:**
- `load_data(filename)` - Load JSON files
- `save_data(filename, data)` - Save data to JSON
- `ensure_data_dir()` - Create data directory

### doctor_manager.py
Manages doctor information and searches.

**Key Functions:**
- `get_doctors(query)` - Get all doctors or filter by name/specialty
- `find_doctor_by_name_or_id(identifier)` - Find specific doctor
- `get_all_doctors()` - Retrieve all doctors

### patient_manager.py
Handles patient identification and information.

**Key Functions:**
- `get_patients()` - Get all patients
- `get_patient_by_id(patient_id)` - Find patient by ID
- `find_patient_by_name(name)` - Find patient by name (fuzzy match)
- `patient_exists(patient_id)` - Check if patient exists

### appointment_manager.py
Manages appointment lifecycle operations.

**Key Functions:**
- `book_appointment(patient_id, doctor_id, date, time)` - Create appointment
- `view_appointments(patient_id)` - Get patient's appointments
- `cancel_appointment(patient_id, appointment_id)` - Cancel appointment
- `reschedule_appointment(patient_id, appointment_id, new_date, new_time)` - Modify appointment

### availability_manager.py
Handles doctor availability and scheduling.

**Key Functions:**
- `get_doctor_availability(doctor_name)` - Check doctor's slots
- `check_availability_by_specialty(specialty, date, date_range)` - Search by specialty
- `is_slot_available(doctor_id, date, time)` - Verify slot availability
- `book_slot(doctor_id, date, time)` - Reserve a slot
- `release_slot(doctor_id, date, time)` - Free up a slot

### config.py
Centralized configuration management.

**Configuration Options:**
- `OPENAI_API_KEY` - API key (from .env)
- `GPT_MODEL` - LLM model selection
- `SYSTEM_PROMPT` - AI assistant instructions
- `VOICE_TIMEOUT` - Voice input timeout
- Voice and session settings

### ai_tools.py
Defines OpenAI function calling tools.

**Available Functions:**
- `get_doctors` - Search doctors
- `get_doctor_availability` - Check doctor's schedule
- `check_availability_by_specialty` - Find doctors by specialty
- `book_appointment` - Create appointments
- `view_appointments` - Show patient appointments
- `cancel_appointment` - Remove appointments
- `reschedule_appointment` - Modify appointments

## Data Files

### doctors.json
```json
{
  "doctors": [
    {
      "doctor_id": "D-01",
      "name": "Dr. Meera Shah",
      "specialty": "Dermatology",
      "qualification": "MD, DDVL",
      "experience": "12 years",
      "consultation_fee": 800,
      "hospital": "Apollo Hospital"
    }
  ]
}
```

### patients.json
```json
{
  "patients": [
    {
      "patient_id": "P-1001",
      "name": "Asha Rao",
      "phone": "+91-9876543210",
      "email": "asha.rao@email.com",
      "age": 34,
      "gender": "Female"
    }
  ]
}
```

### appointments.json
```json
{
  "appointments": [
    {
      "appt_id": "A-2001",
      "patient_id": "P-1001",
      "doctor_id": "D-01",
      "date": "2025-09-22",
      "time": "09:30"
    }
  ]
}
```

### availability.json
```json
{
  "availability": [
    {
      "doctor_id": "D-01",
      "date": "2025-09-22",
      "slots": ["09:30", "10:00", "10:30", "11:00", "14:00"]
    }
  ]
}
```

## Configuration

### Environment Variables (.env)
```
OPENAI_API_KEY=your_api_key_here
```

### Application Settings (config.py)
Modify these in `config.py` to customize:
- `VOICE_TIMEOUT` - Listening duration (seconds)
- `VOICE_PHRASE_TIME_LIMIT` - Max phrase length (seconds)
- `DEFAULT_DATE_RANGE` - Availability search window (days)

## Troubleshooting

### Voice Input Not Working
- Check microphone is properly connected
- Ensure `PyAudio` is installed correctly
- Try adjusting `MICROPHONE_ADJUSTMENT_DURATION` in config

### OpenAI API Errors
- Verify API key is valid
- Check account has available credits
- Ensure internet connection is active

### Patient Not Found
- Check exact spelling of patient name
- Use patient ID format (P-XXXX) if known
- Refer to registered patients list

## Production Deployment

### Docker Support (Optional)
Create a `Dockerfile`:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

### Running in Production
```bash
streamlit run app.py --logger.level=error --client.showErrorDetails=false
```

## Security Considerations

⚠️ **Important:**
1. **Never commit `.env` file** - Use `.env.example` as template
2. **Protect API keys** - Store in environment variables only
3. **Patient data** - Ensure HIPAA compliance in production
4. **Access control** - Implement authentication for real usage
5. **Data encryption** - Use TLS for data transmission

## Contributing

1. Create a new branch for features
2. Write clean, documented code
3. Test thoroughly before committing
4. Follow the module structure
5. Update documentation as needed

## Deployment Checklist

- [ ] API key configured in `.env`
- [ ] All dependencies installed
- [ ] Data files properly formatted
- [ ] Voice input tested
- [ ] Quick actions verified
- [ ] Conversation flows tested
- [ ] `.gitignore` properly configured
- [ ] `.env` file added to `.gitignore`
- [ ] README reviewed and updated

## Support & Issues

For issues or questions:
1. Check the troubleshooting section
2. Review module documentation
3. Check logs in Streamlit terminal
4. Verify data files are properly formatted

## License

[Add your license here]

## Author

[Your Name/Organization]

---

**Last Updated:** 2025-09-21
**Version:** 2.0 (Production-Ready)
=======
# Medical_Chatbot
AI-powered Medical Appointment Booking Assistant built with Streamlit, OpenAI GPT, voice interaction, patient registration, doctor availability management, and appointment scheduling.
>>>>>>> 47d315d32e60572359eec56ee4b4b0702ee3b295
