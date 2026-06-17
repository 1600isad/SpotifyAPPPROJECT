import requests
import urllib.parse

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
}

# Simple in-memory cache so we don't re-fetch the same song every 8 seconds
_cache = {}


def search_songsterr(title, artist):
    """Try multiple Songsterr endpoints until one works."""
    print(f"[Scraper] Searching Songsterr for: {title} - {artist}")

    attempts = [
        # Endpoint 1: pattern search with just title
        f"https://www.songsterr.com/a/ra/songs.json?pattern={urllib.parse.quote(title)}",
        # Endpoint 2: pattern search with title + artist
        f"https://www.songsterr.com/a/ra/songs.json?pattern={urllib.parse.quote(title + ' ' + artist)}",
        # Endpoint 3: artist-specific search
        f"https://www.songsterr.com/a/ra/songs.json?pattern={urllib.parse.quote(artist)}",
    ]

    for url in attempts:
        try:
            r = requests.get(url, headers=HEADERS, timeout=8)
            print(f"[Scraper] Requesting: {url} → Status: {r.status_code}")
            if r.status_code != 200:
                continue

            results = r.json()
            print(f"[Scraper] Raw results: {results[:2]}") 
            if not results:
                continue

            # Look for a title + artist match
            title_lower  = title.lower()
            artist_lower = artist.lower()

            for song in results[:10]:
                s_title  = song.get("title", "").lower()
                s_artist = song.get("artist", {}).get("name", "").lower()
                if title_lower in s_title and (artist_lower in s_artist or s_artist in artist_lower):
                    print(f"[Scraper] ✓ Found match: '{s_title}' by {s_artist} → {url}")
                    return song

            # Looser match — just title
            for song in results[:5]:
                s_title = song.get("title", "").lower()
                if title_lower in s_title:
                    print(f"[Scraper] ✓ Found title match: '{s_title}' by {s_artist} → {url}")
                    return song

        except Exception as e:
            print(f"[Scraper] Songsterr attempt failed: {e}")
            continue
    print(f"[Scraper] No Songsterr match found for: {title} - {artist}")
    return None


def get_chords_from_ai(title, artist):
    """Generate chord chart via OpenAI."""
    try:
        from openai import OpenAI
        from config import OPENAI_API_KEY

        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-5.4-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert guitarist. Write accurate, well-formatted guitar chord charts in plain text."
                },
                {
                    "role": "user",
                    "content": (
                        f"Write a guitar chord chart for '{title}' by {artist}. "
                        f"Include the key, capo if helpful, chord shapes, and the tuning used you can put multiple possible tunings especially if a 7 string can be used and get information from ultimate guitar website for best accuracy. "
                        f"no need to include lyrics double check and make sure key of the song is correct get info from online sources for accuracy. "
                        f"Plain text only, no markdown."
                    )
                }
            ],
            max_completion_tokens=1000,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"[Scraper] AI chord generation error: {e}")
        return None


def get_tab(title, artist):
    """
    Main entry. Uses cache to avoid redundant calls on the same song.
    Returns { content, type, url } or None.
    """
    cache_key = f"{title}::{artist}".lower()

    # Return cached result if we already looked this up
    if cache_key in _cache:
        print(f"[Scraper] Using cache for: {title} - {artist}")
        return _cache[cache_key]

    result = _fetch_tab(title, artist)
    _cache[cache_key] = result
    return result


def _fetch_tab(title, artist):
    query = urllib.parse.quote(f"{title} {artist}")
    songsterr_url = f"https://www.songsterr.com/?pattern={query}"

    content = (
        f"  {title} — {artist}\n"
        f"{'─' * 50}\n\n"
        f"▶  Search on Songsterr:\n"
        f"   {songsterr_url}\n\n"
        f"{'─' * 50}\n"
        f"  AI Chord Chart\n"
        f"{'─' * 50}\n\n")

    

    chords = get_chords_from_ai(title, artist)
    content += chords if chords else "⚠  Add OpenAI billing at platform.openai.com to enable AI chord charts."

    return {"content": content, "type": "Chords", "url": songsterr_url}

