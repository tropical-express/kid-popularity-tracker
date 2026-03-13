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
