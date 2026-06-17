import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    SPOTIFY_REDIRECT_URI,
    SPOTIFY_SCOPE,
)


def get_auth_manager():
    """Returns a SpotifyOAuth manager — used for login flow."""
    return SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SPOTIFY_SCOPE,
        show_dialog=True,
    )


def get_spotify_client(token_info):
    """Returns an authenticated Spotify client from a stored token."""
    return spotipy.Spotify(auth=token_info["access_token"])


def get_currently_playing(sp):
    """
    Returns a dict with the current song info, or None if nothing is playing.

    Example return:
    {
        "title": "Wish You Were Here",
        "artist": "Pink Floyd",
        "album": "Wish You Were Here",
        "album_art": "https://...",
        "is_playing": True,
    }
    """
    try:
        result = sp.currently_playing()

        if not result or not result.get("item"):
            return None

        item = result["item"]
        return {
            "title": item["name"],
            "artist": item["artists"][0]["name"],
            "album": item["album"]["name"],
            "album_art": item["album"]["images"][0]["url"] if item["album"]["images"] else None,
            "is_playing": result["is_playing"],
        }

    except Exception as e:
        print(f"[Spotify] Error fetching currently playing: {e}")
        return None
