import os
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID     = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI  = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:5000/callback")

OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

# Spotify scopes for current playback info super cool
SPOTIFY_SCOPE = "user-read-currently-playing user-read-playback-state"
