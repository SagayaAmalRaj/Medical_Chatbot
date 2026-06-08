# Production-Ready Project Structure

This document outlines the refactored medical chatbot project structure for production deployment.

## 📁 Complete Directory Tree

```
medical-chatbot/
│
├── 📄 app.py                          ⭐ MAIN APPLICATION (Run this!)
│   └── Entry point for Streamlit app
│
├── 🔧 Configuration & Core Modules
│   ├── config.py                      Configuration, API keys, settings
│   ├── data_manager.py                JSON file I/O operations
│   ├── ai_tools.py                    OpenAI function tools
│   └── requirements.txt               Python dependencies
│
├── 💼 Business Logic Modules (Separated Functions)
│   ├── doctor_manager.py              Doctor search & retrieval
│   ├── patient_manager.py             Patient identification & lookup
│   ├── appointment_manager.py         Book, cancel, reschedule
│   └── availability_manager.py        Doctor availability & slots
│
├── 📊 Data Storage (Auto-Created)
│   └── data/
│       ├── doctors.json               Doctor information
│       ├── patients.json              Patient records
│       ├── appointments.json          Appointment bookings
│       └── availability.json          Doctor availability slots
│
├── 📚 Documentation
│   ├── README.md                      Full documentation
│   ├── QUICKSTART.md                  5-minute setup guide
│   └── FILE_STRUCTURE.md              This file
│
├── 🔐 Configuration Files
│   ├── .env.example                   Environment variables template
│   ├── .env                           Actual API keys (do NOT commit)
│   └── .gitignore                     Files to ignore in Git
│
└── 📝 Optional/Generated
    ├── __pycache__/                   Python cache (auto-generated)
    └── venv/                          Virtual environment (auto-generated)
```

---

## 📄 File Descriptions

### Main Application
**`app.py`** (28KB)
- Main Streamlit web application
- Handles UI, voice input, session management
- Imports all business logic modules
- Single entry point for the entire app

### Configuration
**`config.py`** (2KB)
- Centralized configuration management
- API key loading from .env
- Application settings (timeouts, defaults)
- System prompt for AI assistant

### Data Management
**`data_manager.py`** (1KB)
- Generic JSON file operations
- load_data() - Read from JSON
- save_data() - Write to JSON
- Handles missing files gracefully

### Business Logic Modules

**`doctor_manager.py`** (2KB)
- get_doctors(query) - List all doctors
- find_doctor_by_name_or_id() - Search doctors
- get_doctor_by_id() - Exact lookup
- get_all_doctors() - Retrieve all

**`patient_manager.py`** (2KB)
- get_patients() - List all patients
- get_patient_by_id() - Find by ID
- find_patient_by_name() - Fuzzy name search
- patient_exists() - Check if registered

**`appointment_manager.py`** (4KB)
- book_appointment() - Create new appointment
- view_appointments() - Show patient bookings
- cancel_appointment() - Remove appointment
- reschedule_appointment() - Modify date/time
- get_appointment() - Retrieve specific appointment

**`availability_manager.py`** (3KB)
- get_doctor_availability() - Check doctor schedule
- check_availability_by_specialty() - Filter by specialty
- is_slot_available() - Verify slot free
- book_slot() - Reserve time slot
- release_slot() - Free up time slot
- get_available_slots() - List open slots

**`ai_tools.py`** (2KB)
- FUNCTION_TOOLS - Array of OpenAI tools
- Defines all available functions for AI calling
- Includes parameters and descriptions

### Data Storage (Auto-Created)

**`data/doctors.json`**
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

**`data/patients.json`**
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

**`data/appointments.json`**
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

**`data/availability.json`**
```json
{
  "availability": [
    {
      "doctor_id": "D-01",
      "date": "2025-09-22",
      "slots": ["09:30", "10:00", "10:30", "11:00"]
    }
  ]
}
```

### Configuration Files

**`.env.example`** - Template for environment variables
```
OPENAI_API_KEY=your_api_key_here
```

**`.env`** - Actual API keys (NEVER commit this!)
```
OPENAI_API_KEY=sk-...your-real-key...
```

**`.gitignore`** - What to exclude from Git
- `.env` (API keys)
- `__pycache__/` (Python cache)
- `venv/` (Virtual environment)
- `*.pyc` (Compiled Python)
- `data/*.json` (Optional - sensitive data)

### Documentation

**`README.md`** - Complete documentation
- Feature overview
- Installation instructions
- Module documentation
- Configuration options
- Troubleshooting guide
- Production deployment

**`QUICKSTART.md`** - 5-minute setup guide
- Quick installation steps
- Sample commands
- Common issues
- Data file formats

**`FILE_STRUCTURE.md`** - This document
- Directory tree
- File descriptions
- Dependencies
- Data flow

---

## 🔄 Data Flow

```
User Input
    ↓
[Streamlit UI - app.py]
    ↓
[AI Processing - OpenAI API]
    ↓
[Function Calling]
    ├→ doctor_manager.py ─→ data_manager.py ←┐
    ├→ patient_manager.py ─→ data_manager.py  │
    ├→ appointment_manager.py ─→ availability_manager.py ─→ data_manager.py
    └→ [data/ folder with JSON files]
    ↓
[Response Generation]
    ↓
[Voice/Text Output]
    ↓
User Output
```

---

## 📦 Dependencies

### Core Dependencies
```
streamlit==1.38.0          Web UI framework
openai==0.28.1            OpenAI API client
python-dotenv==1.0.0      Environment variable management
```

### Voice Features
```
SpeechRecognition==3.10.0  Speech-to-text
pyttsx3==2.99             Text-to-speech
PyAudio==0.2.13           Audio input/output
```

---

## 🚀 Quick Module Reference

| Module | Purpose | Key Functions |
|--------|---------|----------------|
| `data_manager.py` | File I/O | load_data(), save_data() |
| `doctor_manager.py` | Doctor operations | get_doctors(), find_doctor_by_name_or_id() |
| `patient_manager.py` | Patient operations | get_patients(), find_patient_by_name() |
| `appointment_manager.py` | Appointment CRUD | book_appointment(), view_appointments() |
| `availability_manager.py` | Scheduling | book_slot(), release_slot(), is_slot_available() |
| `ai_tools.py` | AI integration | FUNCTION_TOOLS array |
| `config.py` | Settings | API keys, timeouts, prompts |
| `app.py` | Web UI | Main Streamlit application |

---

## 💾 Data Isolation

Each JSON file is **independent**:
- ✅ `doctors.json` - Doctor information only
- ✅ `patients.json` - Patient records only
- ✅ `appointments.json` - Booking records only
- ✅ `availability.json` - Schedule slots only

**No data duplication** - Each piece of information stored once.

---

## 🔐 Security Best Practices

1. ✅ `.env` file in `.gitignore` - Never commit API keys
2. ✅ Config module - Centralized key management
3. ✅ Patient isolation - Each patient sees only own data
4. ✅ Modular design - Easy to audit each module
5. ✅ Clean separation - UI doesn't access files directly

---

## 📈 Scalability Notes

This structure supports:
- ✅ **Adding new doctors/patients** - Just update JSON files
- ✅ **New appointment types** - Extend appointment_manager.py
- ✅ **Additional specialties** - Automatic with doctor data
- ✅ **Database migration** - Replace data_manager.py implementation
- ✅ **API endpoints** - Can expose modules via FastAPI/Flask
- ✅ **Multiple users** - Already supports patient isolation

---

## 🛠️ Maintenance

### Adding a New Feature
1. Create new function in appropriate module
2. Update `ai_tools.py` if it needs AI access
3. Test with existing data
4. Update `README.md` with new command

### Debugging
1. Check `config.py` for API key
2. Verify `data/` folder exists with valid JSON
3. Use Streamlit terminal for error messages
4. Check individual module imports

### Deployment
1. Use `config.py` for all settings
2. Load API key from environment
3. Ensure `data/` folder is writable
4. Test all modules before deployment

---

## ✨ Why This Structure?

| Aspect | Benefit |
|--------|---------|
| **Modular** | Each module has single responsibility |
| **Testable** | Can test each module independently |
| **Maintainable** | Easy to find and fix issues |
| **Scalable** | Easy to add features |
| **Production-Ready** | Follows best practices |
| **Clean** | No monolithic files |
| **Documented** | Every module well-commented |

---

**Last Updated:** 2025-09-21
**Status:** Production Ready ✅
