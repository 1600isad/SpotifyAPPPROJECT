// Isaac acuna 2026 - main.js


// ── State ────────────────────────────────────────────────────
let currentTrack  = null;   // { title, artist, album, album_art }
let currentTab    = null;   // { content, type, url }
let chatHistory   = [];
let chatOpen      = false;
let aiLoading     = false;

// ── Polling ──────────────────────────────────────────────────

async function pollNowPlaying() {
  try {
    const res  = await fetch("/api/now-playing");
    const data = await res.json();

    if (data.error === "not_logged_in") {
      window.location.href = "/";
      return;
    }

    if (!data.playing) {
      showIdle();
      return;
    }

    // Only update if the song changed
    const trackChanged = !currentTrack ||
      currentTrack.title  !== data.track.title ||
      currentTrack.artist !== data.track.artist;

    if (trackChanged) {
      currentTrack = data.track;
      currentTab   = data.tab;
      chatHistory  = [];   // reset chat on song change
      renderTrack(currentTrack);
      renderTab(currentTab);
    }

  } catch (err) {
    console.error("Poll error:", err);
  }
}

// Poll every 8 seconds
pollNowPlaying();
setInterval(pollNowPlaying, 8000);


// ── Render ───────────────────────────────────────────────────

function showIdle() {
  currentTrack = null;
  currentTab   = null;

  document.getElementById("idle-state").classList.remove("hidden");
  document.getElementById("now-playing").classList.add("hidden");
  document.getElementById("tab-idle").classList.remove("hidden");
  document.getElementById("tab-content").classList.add("hidden");
  document.getElementById("tab-loading").classList.add("hidden");
  document.getElementById("tab-not-found").classList.add("hidden");
  closeAiOutput();
}

function renderTrack(track) {
  document.getElementById("idle-state").classList.add("hidden");
  document.getElementById("now-playing").classList.remove("hidden");

  document.getElementById("album-art").src     = track.album_art || "";
  document.getElementById("track-title").textContent  = track.title;
  document.getElementById("track-artist").textContent = track.artist;
  document.getElementById("track-album").textContent  = track.album;

  closeAiOutput();
}

function renderTab(tab) {
  const loading  = document.getElementById("tab-loading");
  const content  = document.getElementById("tab-content");
  const notFound = document.getElementById("tab-not-found");
  const idle     = document.getElementById("tab-idle");

  idle.classList.add("hidden");
  loading.classList.add("hidden");
  content.classList.add("hidden");
  notFound.classList.add("hidden");

  if (!tab) {
    notFound.classList.remove("hidden");
    return;
  }

  document.getElementById("tab-type-badge").textContent   = tab.type || "Tab";
  document.getElementById("tab-source-link").href         = tab.url  || "#";
  document.getElementById("tab-text").textContent         = tab.content || "";

  content.classList.remove("hidden");

  // Auto-open if toggle is on
  const autoOpen = document.getElementById("auto-open-toggle").checked;
  if (autoOpen && tab.url) {
    window.open(tab.url, "_blank");}
  
}


// ── AI Actions ───────────────────────────────────────────────

const AI_LABELS = {
  difficulty: "Difficulty Rating",
  simplify:   "Recreate Tone",
  tips:       "Practice Tips",
};

async function aiAction(type) {
  if (!currentTab || !currentTrack || aiLoading) return;

  aiLoading = true;
  showAiOutput(AI_LABELS[type], "Loading...");

  try {
    const res = await fetch(`/api/ai/${type}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        tab:    currentTab.content,
        title:  currentTrack.title,
        artist: currentTrack.artist,
      }),
    });
    const data = await res.json();
    showAiOutput(AI_LABELS[type], data.result || "No response.");
  } catch (err) {
    showAiOutput(AI_LABELS[type], "Error — check your OpenAI key.");
  } finally {
    aiLoading = false;
  }
}

function showAiOutput(label, text) {
  document.getElementById("ai-output-label").textContent = label;
  document.getElementById("ai-output-text").textContent  = text;
  document.getElementById("ai-output").classList.remove("hidden");
}

function closeAiOutput() {
  document.getElementById("ai-output").classList.add("hidden");
}


// ── Chat ─────────────────────────────────────────────────────

function toggleChat() {
  chatOpen = !chatOpen;
  document.getElementById("chat-panel").classList.toggle("hidden", !chatOpen);
  if (chatOpen) document.getElementById("chat-input").focus();
}

async function sendChat() {
  const input = document.getElementById("chat-input");
  const msg   = input.value.trim();
  if (!msg || !currentTab) return;

  input.value = "";
  appendChatMsg("user", msg);
  chatHistory.push({ role: "user", content: msg });

  appendChatMsg("ai", "...");

  try {
    const res = await fetch("/api/ai/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        tab:     currentTab.content,
        title:   currentTrack.title,
        artist:  currentTrack.artist,
        message: msg,
        history: chatHistory.slice(-8),  // keep last 8 turns
      }),
    });
    const data = await res.json();
    const reply = data.result || "Sorry, I couldn't answer that.";

    // Replace the "..." bubble
    const msgs   = document.getElementById("chat-messages");
    const bubbles = msgs.querySelectorAll(".chat-msg.ai");
    bubbles[bubbles.length - 1].textContent = reply;

    chatHistory.push({ role: "assistant", content: reply });

  } catch (err) {
    const msgs   = document.getElementById("chat-messages");
    const bubbles = msgs.querySelectorAll(".chat-msg.ai");
    bubbles[bubbles.length - 1].textContent = "Error — try again.";
  }
}

function appendChatMsg(role, text) {
  const msgs = document.getElementById("chat-messages");
  const div  = document.createElement("div");
  div.className    = `chat-msg ${role}`;
  div.textContent  = text;
  msgs.appendChild(div);
  msgs.scrollTop   = msgs.scrollHeight;
}
