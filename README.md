# 🎸 TabSync — Spotify Guitar Tab App

Automatically fetches guitar tabs for whatever you're listening to on Spotify, with AI-powered tools to simplify chords, rate difficulty, and give practice tips.

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

## Deploying (for your portfolio)
1. Push to GitHub
2. Create an account on [Railway](https://railway.app) or [Render](https://render.com)
3. Connect your GitHub repo
4. Add your `.env` variables in the dashboard
5. Update your Spotify app's Redirect URI to your live URL
