import os

from flask import (
    Flask, render_template, redirect, request,
    session, jsonify, url_for
)
from config import FLASK_SECRET_KEY
from spotify_client import get_auth_manager, get_spotify_client, get_currently_playing
from tab_scraper import get_tab
from ai_assistant import get_difficulty, tone, get_practice_tips, chat_about_tab
import time

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',


    
)

# ─── Auth Routes ────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Home page — show the app if logged in, otherwise show login page."""
    if "token_info" not in session:
        return render_template("login.html")
    return render_template("index.html")


@app.route("/login")
def login():
    """Redirect user to Spotify login."""
    auth_manager = get_auth_manager()
    auth_url = auth_manager.get_authorize_url()
    return redirect(auth_url)


@app.route("/callback")
def callback():
    """Spotify redirects here after login — exchange code for token."""
    code = request.args.get("code")
    if not code:
        return "Login failed — no code returned.", 400

    auth_manager = get_auth_manager()
    token_info = auth_manager.get_access_token(code)
    session["token_info"] = token_info
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# ─── Helper ─────────────────────────────────────────────────────────────────

def get_valid_token():
    """Returns a refreshed token or None if not logged in."""
    token_info = session.get("token_info")
    if not token_info:
        return None

    # Refresh if expired
    auth_manager = get_auth_manager()
    if auth_manager.is_token_expired(token_info):
        token_info = auth_manager.refresh_access_token(token_info["refresh_token"])
        session["token_info"] = token_info

    return token_info


# ─── API Routes (called by frontend JS) ─────────────────────────────────────

@app.route("/api/now-playing")
def now_playing():
    """Returns the current Spotify track + fetches its tab."""
    token_info = get_valid_token()
    if not token_info:
        return jsonify({"error": "not_logged_in"}), 401

    sp = get_spotify_client(token_info)
    track = get_currently_playing(sp)

    if not track:
        return jsonify({"playing": False})

    # Fetch tab for this song
    tab_data = get_tab(track["title"], track["artist"])

    return jsonify({
        "playing": True,
        "track": track,
        "tab": tab_data,  # { content, type, url } or None
    })


@app.route("/api/ai/difficulty", methods=["POST"])
def ai_difficulty():
    data = request.json
    result = get_difficulty(data["tab"], data["title"], data["artist"])
    return jsonify({"result": result})


@app.route("/api/ai/simplify", methods=["POST"])
def ai_simplify():
    data = request.json
    result = tone(data["tab"], data["title"], data["artist"])
    return jsonify({"result": result})


@app.route("/api/ai/tips", methods=["POST"])
def ai_tips():
    data = request.json
    result = get_practice_tips(data["tab"], data["title"], data["artist"])
    return jsonify({"result": result})


@app.route("/api/ai/chat", methods=["POST"])
def ai_chat():
    data = request.json
    result = chat_about_tab(
        tab_content=data["tab"],
        title=data["title"],
        artist=data["artist"],
        user_question=data["message"],
        history=data.get("history", []),
    )

    return jsonify({"result": result})


# ─── Run ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)

