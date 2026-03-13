# Kid Popularity Tracker 📊

[![Python](https://img.shields.io/badge/python-3.10+-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.27-orange?logo=streamlit)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A backend and dashboard system to track YouTube kid mentions in comments.  
It fetches comments from a channel, counts mentions of specific kids’ names, and visualizes popularity trends over time.

---

## Features

- Fetches up to 100 recent videos from a YouTube channel
- Analyzes up to 300 comments per video
- Tracks mentions of specified kids
- Saves current data and appends historical trends
- Visualizes current leaderboard and historical trends via Streamlit dashboard

---

## Setup

1. **Clone the repository:**
```bash
git clone https://github.com/tropical-express/kid-popularity-tracker.git
cd kid-popularity-tracker
```
2. **Create virtual enviroment (recommended)**

   ## Windows
   ```
   python -m venv venv venv\Scripts\activate
   ```

   ## Mac/Linux
   ```
   python -m venv venv source venv/bin/activate
   ```

   3. **Install dependencies**
      ```
      pip install -r requirements.txt
      ```
      ---
      # Enviroment setup
      Create a .env file based on .env.example

      Example:
      ```
      YOUTUBE_API_KEY=YOUR_API_KEY_HERE
      CHANNEL_ID=YOUR_CHANNEL_ID_HERE
      ```
   You can get an API key from Google Cloud Console.

   ---
   #Running the Backend 
    the backend fetches comments and calculates popularity.
   ```
   python kid_backend_engine.py
   ```

## This will generate:
kid_current.csv
kid_current.json
kid_history.csv

---

# Running the Dashboard
 Start the dashboard:
 ```
streamlit run kid_dashboard.py
```
Then open the local URL shown in the terminal.

The dashboard displays:
-Current Popularity Leaderboard
-Pie Chart Distribution
-Historical Display Trends
---
# Data Files
  Generated files (not included in git):
  -kid_current.csv
  -kid_current.json
  -kid_history.csv
  These are ignored in .gitignore.
  ---
  # Security Notes
   This repository does not include API keys.

   Enviroment Variables are stored in .env, which is excluded from version control.
   ---
   # Requirements
   The project depends on:

   -pandas
   -streamlit
   -plotly
   -python-dotenv
   -google-api-python-client
   Install them using:
   ```
pip install -r requirements.txt
```
---
# License
MIT License
---
# Disclaimer

This project uses the official Youtube Data API and analyzes publicly availible comments.
It does not scrape private data or bypass API restrictions.
