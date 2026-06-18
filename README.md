# 🎸 TabSync — Spotify Guitar Tab App

Automatically fetches guitar tabs for whatever you're listening to on Spotify, with AI-powered tools to simplify chords, rate difficulty, and give practice tips.
Live website demo link: https://web-production-e301ab.up.railway.app/

## Screenshots

<img width="959" height="475" alt="pro1" src="https://github.com/user-attachments/assets/a6c5c795-221f-4963-976d-34160039e660" />

<img width="959" height="472" alt="pro2" src="https://github.com/user-attachments/assets/a8f3872e-5796-4526-9d2c-95ed9316a507" />

<img width="959" height="470" alt="pro3" src="https://github.com/user-attachments/assets/a9fbc5da-b829-4197-a2ff-443305fc76f0" />

<img width="958" height="470" alt="pro4" src="https://github.com/user-attachments/assets/be6d69a6-d74a-4abd-8c6b-a162a38d7b41" />

<img width="959" height="477" alt="pro5" src="https://github.com/user-attachments/assets/101043b4-4394-46b1-b1de-f31390df01b6" />

## Setup

### 1. Clone & install dependencies
```bash
pip install -r requirements.txt
```

### 2. Create your `.env` file
```bash
cp .env.example .env
```
Then fill in your keys:

**Spotify API:**
1. Go to https://developer.spotify.com/dashboard
2. Create a new app
3. Add `http://localhost:5000/callback` as a Redirect URI
4. Copy your Client ID and Client Secret into `.env`

**OpenAI API:**
1. Go to https://platform.openai.com/api-keys
2. Create a new key and paste it into `.env`

### 3. Run the app
```bash
python app.py
```

Open http://localhost:5000 in your browser, log in with Spotify, and play a song!

## Project Structure

```
spotify-tab-app/
├── app.py              # Flask routes
├── spotify_client.py   # Spotify auth + now playing
├── tab_scraper.py      # Ultimate Guitar scraping
├── ai_assistant.py     # OpenAI features
├── config.py           # Environment config
├── templates/
│   ├── index.html      # Main app UI
│   └── login.html      # Login page
├── static/
│   ├── css/style.css
│   └── js/main.js
├── requirements.txt
└── .env.example
```

## Features
- 🎵 Auto-detects currently playing Spotify song (polls every 8 seconds)
- 🎸 Fetches top-rated tab from Ultimate Guitar automatically
- ⚡ AI difficulty rating
- 🔰 AI chord simplifier for beginners
- 📋 AI practice tips
- 💬 Chat with AI about the tab
