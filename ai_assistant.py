# Spotify guitar tab assistant with AI features by Isaac Acuna
# This file contains the AI-related functions that call OpenAI's API.

from openai import OpenAI # Open ai API used for chatbot and ai features
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY) #returns an instance of the OpenAI client, which is used to make API calls to OpenAI's services.


def _call_gpt(system_prompt, user_prompt, max_tokens=400):
    """Base helper for calling GPT-4o-mini."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[AI] Error: {e} lol gotta fix something bum haha")
        return None

#retrieves difficulty for tabbed songs
def get_difficulty(tab_content, title, artist):
    """Returns a difficulty rating and short explanation."""

    #prompt for the ai haha
    system = (
        "You are a guitar teacher. Given a guitar tab or chord chart, "
        "rate its difficulty (Beginner / Intermediate / Advanced / Expert / Virtuoso GOD) and give "
        "a 2-sentence explanation. Be concise and friendly as well as give how many years of guitar playing is usually needed to play the song."
    )
    user = f"Song: {title} by {artist}\n\nTab:\n{tab_content[:2000]}" 
    return _call_gpt(system, user, max_tokens=400)

#------------------------------------------------------------------     
def tone(tab_content, title, artist):
    """Returns a list of gear used by the guitarist for the song."""
    system = (
        "You are a guitar teacher and tone expert. Given a guitar tab or chord chart, "
        "create a rig rundown of the gear and settings needed to achieve the tone of the original recording. "
        "Make sure you give accurate information regarding the original guitarist and what gear they use. "
        "Keep it helpful and informative."
    )
    user = f"Song: {title} by {artist}\n\nOriginal tab:\n{tab_content[:2000]}"
    return _call_gpt(system, user, max_tokens=400)

#------------------------------------------------------------------
def get_practice_tips(tab_content, title, artist):
    """Returns 3 specific practice tips for the song."""
    system = (
        "You are a guitar teacher. Given a guitar tab, provide exactly 3 "
        "specific, actionable practice tips for this song. "
        "Format as a numbered list. Be concise and include different techniques to work on eg pinch harmonics or sweep picking or whatever."
    )
    user = f"Song: {title} by {artist}\n\nTab:\n{tab_content[:2000]}"
    return _call_gpt(system, user, max_tokens=400)

#------------------------------------------------------------------
def chat_about_tab(tab_content, title, artist, user_question, history=None):
    """
    Answers a freeform question about the tab.
    history: list of {"role": "user"/"assistant", "content": "..."} dicts
    """
    system = (
        f"You are a helpful guitar teacher assistant. The user is looking at "
        f"the guitar tab for '{title}' by {artist}. "
        f"Answer questions about the tab, chords, technique, or music theory. "
        f"Be concise and friendly.\n\nTab content:\n{tab_content[:1500]}"
    )

    messages = [{"role": "system", "content": system}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_question})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=1000,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[AI] Chat error: {e}")
        return "Sorry, I couldn't process that. Try again!"
