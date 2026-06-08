# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Setup (1 minute)
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure (1 minute)
```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-...your-key...
```

### Step 3: Prepare Data (1 minute)
The `data/` folder will be created automatically with:
- `doctors.json` - Doctor information
- `patients.json` - Patient records
- `appointments.json` - Booking records
- `availability.json` - Doctor availability slots

### Step 4: Run (1 minute)
```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

### Step 5: Test (1 minute)
1. Click "🎤 Voice Input" or type in the text box
2. Say: "I'm Asha Rao" to identify yourself
3. Say: "Show available doctors"
4. Say: "Book with Dr. Shah tomorrow at 9 AM"

---

## 📁 Project Structure

```
your-project/
├── app.py                  ← Main application (run this!)
├── config.py              ← Settings
├── requirements.txt       ← Dependencies
├── .env                   ← Your API key (keep secret!)
├── .gitignore            ← Files to ignore
├── README.md             ← Full documentation
│
├── data_manager.py       ← File operations
├── doctor_manager.py     ← Doctor functions
├── patient_manager.py    ← Patient functions
├── appointment_manager.py← Appointment functions
├── availability_manager.py← Schedule functions
├── ai_tools.py           ← AI tools
│
└── data/                 ← Auto-created data folder
    ├── doctors.json
    ├── patients.json
    ├── appointments.json
    └── availability.json
```

---

## 🎤 How to Use

### Text Mode
- Type your message in the input box
- Click "Send" button
- Assistant responds immediately

### Voice Mode
- Click "🎤 Voice Input" button
- Speak clearly into your microphone
- Assistant processes and responds

### Quick Actions
- **📅 My Appointments** - View your bookings
- **🔍 Find Doctors** - Search available doctors
- **❓ Help** - Get command suggestions

---

## 📋 Sample Commands

### Identify Yourself
```
"My name is John Doe"
"I'm Sarah Wilson"
"I am P-1001"
```

### Find Doctors
```
"Show available doctors"
"Find dermatologists"
"List cardiologists"
"Check Dr. Shah's availability"
```

### Book Appointment
```
"Book with Dr. Shah tomorrow at 9 AM"
"Schedule with D-02 on 2025-09-25 at 10:00"
"Appointment with Dr. Kumar for ENT"
```

### Manage Appointments
```
"Show my appointments"
"Cancel A-2001"
"Reschedule A-2001 to tomorrow at 2 PM"
"Move my appointment to next week"
```

---

## 🔑 Key Files

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit app - **run this** |
| `config.py` | Settings and API configuration |
| `.env` | Your OpenAI API key (**keep secret!**) |
| `data/` | Folder with JSON data files |
| `requirements.txt` | Python packages to install |

---

## 🐛 Common Issues

### "API key not found"
- Make sure `.env` file exists
- Add `OPENAI_API_KEY=your-key` to `.env`
- Restart the app

### "Microphone not found"
- Check microphone is plugged in
- Try restarting the app
- May need to reinstall `PyAudio`

### "Patient not found"
- Check spelling of patient name
- Use exact name from the system
- Try using patient ID (P-1001 format)

### "No doctors found"
- Make sure `data/doctors.json` exists
- File should contain doctor data
- Check file is valid JSON

---

## 📊 Data Files Format

### doctors.json
```json
{
  "doctors": [
    {
      "doctor_id": "D-01",
      "name": "Dr. Meera Shah",
      "specialty": "Dermatology"
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
      "email": "asha.rao@email.com"
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
      "slots": ["09:30", "10:00", "10:30"]
    }
  ]
}
```

---

## 🚀 Next Steps

1. ✅ Get the app running with your data
2. ✅ Test voice input with sample commands
3. ✅ Customize with your own doctors/patients
4. ✅ Deploy to production when ready
5. ✅ Add authentication for real users

---

## 📚 Full Documentation

See `README.md` for:
- Detailed module documentation
- Configuration options
- Deployment instructions
- Security considerations
- Production checklist

---

**Need help?** Check README.md for troubleshooting!
