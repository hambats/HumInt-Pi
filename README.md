HUMINT‑Pi is a Raspberry Pi–based system that continuously listens through a connected microphone, detects human speech, transcribes it, and classifies the transcript in real time.
It is a fork of BirdNET‑Pi, replacing the bird‑call detection model with a speech recognition and classification pipeline.

Features
Runs entirely offline on a Raspberry Pi (no cloud dependency).

Detects human speech while filtering out non‑speech noise.

Local transcription using Whisper.cpp or Vosk.

Classifies transcripts for:

Language detection

Keyword spotting

Topic categorization

Sentiment/tone (optional)

Web dashboard with searchable detection logs.

REST API for external integrations.

Hardware Requirements
Raspberry Pi 4 or newer (2GB RAM minimum, 4GB+ recommended)

USB microphone or USB audio interface with mic input

32GB+ microSD or SSD storage

Network connection (Ethernet or Wi‑Fi)

Software Stack
Python 3.11+

Whisper.cpp or Vosk (local STT)

Flask for dashboard/API

SQLite for detection storage

Optional: spaCy, langdetect, VADER for classification

Installation
bash
Copy code
# 1. Clone the repository
git clone https://github.com/yourusername/HUMINT-Pi.git
cd HUMINT-Pi

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure microphone and options
nano config.ini

# 4. Start the listener
python listener.py

# 5. Initialise the database
python -m scripts.database /path/to/speech.db
Configuration
config.ini allows you to set:

Input microphone device

Sensitivity threshold

Enabled classification modules

Data retention policy (days to keep transcripts)

Database Schema
---------------
Speech events are stored in ``speech_events``:

```
CREATE TABLE speech_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT,
  transcript TEXT,
  language TEXT,
  keywords TEXT,
  sentiment TEXT
);
```

Dashboard
Visit:

cpp
Copy code
http://<your-pi-ip>:5010
Features:

Timeline of speech events

Full transcripts

Classification tags

Search/filter by keyword, date, or category

Use Cases
Language and dialect detection

Meeting or workspace keyword/tone monitoring

Research projects on speech patterns

Security keyword alerts (with consent)

Privacy
HUMINT‑Pi is built for local use. All processing happens on your Raspberry Pi; raw audio is only stored if explicitly enabled.
