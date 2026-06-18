# 🎸 TabSync — Spotify Guitar Tab App
Why I even made this because im too lazy to pull up the tabs if i forgot them every time im playing along to a song on spotify so this will see the song im playing along to on guitar and will auto pull up the guitar tabs on songsterr (I wish they had their own public API since it only allows to go to the search rather than actual tab so you have to do an extra click). Also added an ai assistant to help with tone or technique tips on the fly if i forget those as well which is pretty cool.
*Currently OpenAI API calls are not working on demo due to me only having a free plan on railway which doesnt allow for the calls to work unless i spend money great, it does work though locally i promise
Live website demo link: https://web-production-e301ab.up.railway.app/

## How It Works

Log in with your Spotify account
Play any song on Spotify
TabSync detects what's playing and automatically fetches a Songsterr tab link and generates an AI chord chart for the song
Use the AI tools to rate the song's difficulty, get a gear/tone breakdown, or get practice tips
Chat with the AI assistant to ask questions about the tab, chords, or technique

## Tech Stack

Python + Flask — backend server and routing
Spotipy — Spotify API integration for real-time now playing detection
OpenAI GPT — AI chord chart generation and guitar assistant features
Songsterr — tab search integration
HTML/CSS/JavaScript — frontend UI with dark mode

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
