import streamlit as st
import os, json, random, base64
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime, date, timedelta
import plotly.graph_objects as go
import plotly.express as px
from gtts import gTTS
try:
    import pandas as pd
    import numpy as np
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

load_dotenv()

st.set_page_config(
    page_title="MindEase AI ✨",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── MEGA CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Space Grotesk', 'Inter', sans-serif !important; }

/* ── BACKGROUND ── */
.stApp {
  background: #07060f;
  min-height: 100vh;
  overflow-x: hidden;
}
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 60% at 20% 10%, rgba(139,92,246,0.18) 0%, transparent 60%),
    radial-gradient(ellipse 60% 50% at 80% 80%, rgba(6,182,212,0.13) 0%, transparent 60%),
    radial-gradient(ellipse 50% 40% at 60% 30%, rgba(236,72,153,0.10) 0%, transparent 55%);
  pointer-events: none;
  z-index: 0;
}

/* ── HIDE DEFAULTS ── */
#MainMenu, footer { visibility: hidden; }
[data-testid="stHeader"] { background: rgba(0,0,0,0) !important; }
.block-container { padding: 0.5rem 1.5rem 2rem !important; position: relative; z-index: 1; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
  background: rgba(10,8,25,0.97) !important;
  border-right: 1px solid rgba(139,92,246,0.2) !important;
  backdrop-filter: blur(20px);
}
section[data-testid="stSidebar"] > div { padding-top: 1rem !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(139,92,246,0.4); border-radius: 99px; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
  background: rgba(255,255,255,0.04);
  border-radius: 16px;
  padding: 4px;
  gap: 4px;
  border: 1px solid rgba(255,255,255,0.08);
}
.stTabs [data-baseweb="tab"] {
  border-radius: 12px !important;
  color: rgba(255,255,255,0.5) !important;
  font-weight: 600 !important;
  font-size: 0.88rem !important;
  padding: 8px 18px !important;
  transition: all 0.25s ease !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg,#7c3aed,#6366f1) !important;
  color: white !important;
  box-shadow: 0 4px 20px rgba(124,58,237,0.4) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.2rem !important; }

/* ── BUTTONS ── */
.stButton > button {
  border-radius: 50px !important;
  padding: 10px 22px !important;
  font-weight: 600 !important;
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: 0.9rem !important;
  transition: all 0.3s cubic-bezier(0.4,0,0.2,1) !important;
  letter-spacing: 0.01em !important;
}
.stButton > button[data-testid="baseButton-primary"] {
  background: linear-gradient(135deg,#7c3aed,#6366f1) !important;
  color: white !important;
  border: none !important;
}
.stButton > button[data-testid="baseButton-secondary"] {
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  color: white !important;
}
.stButton > button:hover {
  transform: translateY(-2px) scale(1.03) !important;
  box-shadow: 0 8px 28px rgba(124,58,237,0.45) !important;
}
.stButton > button[data-testid="baseButton-secondary"]:hover {
  border-color: rgba(139,92,246,0.5) !important;
  box-shadow: 0 8px 28px rgba(124,58,237,0.15) !important;
}
.stButton > button:active { transform: translateY(0) scale(0.98) !important; }

/* ── INPUTS ── */
.stTextArea textarea, .stTextInput input,
.stTextArea [data-baseweb="textarea"], .stTextInput [data-baseweb="base-input"], .stTextInput [data-baseweb="input"] {
  background-color: #0f0c1b !important;
  background: #0f0c1b !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  border-radius: 14px !important;
  color: white !important;
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: 0.95rem !important;
  transition: border-color 0.25s ease !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
  border-color: rgba(139,92,246,0.6) !important;
  box-shadow: 0 0 0 3px rgba(139,92,246,0.12) !important;
}
.stTextArea textarea::placeholder, .stTextInput input::placeholder {
  color: rgba(255,255,255,0.3) !important;
}

/* ── SELECTBOX ── */
.stSelectbox > div > div {
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  border-radius: 12px !important;
  color: white !important;
}

/* ── METRICS ── */
[data-testid="stMetric"] {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 16px !important;
  padding: 16px !important;
}
[data-testid="stMetricValue"] { color: #a78bfa !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: rgba(255,255,255,0.5) !important; }

/* ── DIVIDER ── */
hr { border-color: rgba(255,255,255,0.07) !important; margin: 1rem 0 !important; }

/* ── CARDS ── */
.glass-card {
  background: rgba(255,255,255,0.04);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(255,255,255,0.09);
  border-radius: 20px;
  padding: 1.4rem;
  margin: 0.8rem 0;
  position: relative;
  overflow: hidden;
}
.glass-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(139,92,246,0.4), transparent);
}
.neon-card {
  background: rgba(124,58,237,0.08);
  border: 1px solid rgba(124,58,237,0.3);
  border-radius: 20px;
  padding: 1.2rem 1.4rem;
  margin: 0.8rem 0;
  box-shadow: 0 0 30px rgba(124,58,237,0.08), inset 0 0 30px rgba(124,58,237,0.03);
}
.affirmation-card {
  background: linear-gradient(135deg, rgba(124,58,237,0.15), rgba(99,102,241,0.12), rgba(6,182,212,0.08));
  border: 1px solid rgba(139,92,246,0.3);
  border-radius: 20px;
  padding: 20px 26px;
  text-align: center;
  font-size: 1.08rem;
  font-weight: 500;
  color: #e2e8f0;
  font-style: italic;
  margin: 14px 0;
  position: relative;
  overflow: hidden;
}
.affirmation-card::after {
  content: '✦';
  position: absolute;
  top: -10px; right: -10px;
  font-size: 4rem;
  opacity: 0.05;
  color: #a78bfa;
}

/* ── CHAT BUBBLES ── */
.user-bubble {
  background: linear-gradient(135deg,#7c3aed,#6366f1);
  color: white;
  border-radius: 22px 22px 5px 22px;
  padding: 13px 18px;
  max-width: 78%;
  margin-left: auto;
  box-shadow: 0 4px 24px rgba(124,58,237,0.35);
  animation: slideR 0.28s cubic-bezier(0.4,0,0.2,1);
  line-height: 1.55;
  font-size: 0.95rem;
}
.bot-bubble {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
  color: #e2e8f0;
  border-radius: 22px 22px 22px 5px;
  padding: 13px 18px;
  max-width: 78%;
  box-shadow: 0 4px 24px rgba(0,0,0,0.25);
  animation: slideL 0.28s cubic-bezier(0.4,0,0.2,1);
  line-height: 1.55;
  font-size: 0.95rem;
}
.role-lbl {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: .1em;
  text-transform: uppercase;
  margin-bottom: 5px;
  opacity: 0.6;
}
.chat-wrap { display: flex; margin: 7px 0; }
.chat-wrap.user { justify-content: flex-end; }
.chat-wrap.bot  { justify-content: flex-start; }

/* ── TYPING DOTS ── */
.typing-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: #a78bfa;
  display: inline-block;
  margin: 0 2px;
  animation: typingBounce 1.2s ease-in-out infinite;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

/* ── BADGES ── */
.streak-badge {
  background: linear-gradient(135deg,#f97316,#ef4444);
  color: white;
  border-radius: 50px;
  padding: 8px 20px;
  font-weight: 700;
  font-size: .92rem;
  display: inline-block;
  box-shadow: 0 4px 20px rgba(239,68,68,0.35);
  animation: glowPulse 2.5s ease-in-out infinite;
}
.milestone-badge {
  background: linear-gradient(135deg,#f59e0b,#f97316);
  color: white;
  border-radius: 8px;
  padding: 4px 10px;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  display: inline-block;
}

/* ── VIBE BUTTONS ── */
.vibe-btn {
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 14px;
  padding: 10px 6px;
  text-align: center;
  cursor: pointer;
  transition: all 0.22s ease;
  font-size: 1.5rem;
}
.vibe-btn:hover { border-color: rgba(139,92,246,0.5); transform: scale(1.08); }
.vibe-btn.active {
  border-color: #7c3aed;
  background: rgba(124,58,237,0.2);
  box-shadow: 0 0 16px rgba(124,58,237,0.3);
}
.vibe-label { font-size: 0.65rem; color: rgba(255,255,255,0.5); margin-top: 3px; }

/* ── JOURNAL CARD ── */
.journal-card {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-left: 3px solid #7c3aed;
  border-radius: 14px;
  padding: 14px 18px;
  margin: 8px 0;
  transition: all 0.22s ease;
}
.journal-card:hover {
  background: rgba(124,58,237,0.07);
  border-left-color: #a78bfa;
}

/* ── QUICK CHIPS ── */
.chip {
  background: rgba(124,58,237,0.15);
  border: 1px solid rgba(124,58,237,0.3);
  border-radius: 50px;
  padding: 6px 14px;
  color: #c4b5fd;
  font-size: 0.82rem;
  font-weight: 500;
  cursor: pointer;
  display: inline-block;
  margin: 3px;
  transition: all 0.2s ease;
}
.chip:hover {
  background: rgba(124,58,237,0.3);
  transform: translateY(-1px);
}

/* ── CRISIS CARD ── */
.crisis-card {
  background: rgba(127,29,29,0.45);
  border: 1px solid rgba(248,113,113,0.5);
  border-radius: 18px;
  padding: 18px 22px;
  margin: 12px 0;
  animation: glowRed 2s ease-in-out infinite;
}

/* ── SIDEBAR LOGO ── */
.sidebar-logo {
  text-align: center;
  padding: 12px 0 6px;
}
.sidebar-logo .icon { font-size: 2.2rem; animation: float 3.5s ease-in-out infinite; display: block; }
.sidebar-logo .brand {
  font-size: 1.3rem;
  font-weight: 800;
  background: linear-gradient(135deg,#a78bfa,#818cf8,#38bdf8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.01em;
}
.sidebar-logo .tagline { color: rgba(255,255,255,0.35); font-size: 0.75rem; margin-top: 2px; }

/* ── PAGE HEADER ── */
.page-header {
  text-align: center;
  padding: 14px 0 6px;
}
.page-header h1 {
  font-size: 2.8rem;
  font-weight: 800;
  background: linear-gradient(135deg,#a78bfa,#818cf8,#38bdf8,#34d399);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
  line-height: 1.1;
  letter-spacing: -0.02em;
}
.page-header p { color: rgba(255,255,255,0.4); font-size: 1rem; margin: 6px 0 0; }

/* ── BREATH CIRCLE ── */
.breath-ring {
  width: 130px; height: 130px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(124,58,237,0.8), rgba(99,102,241,0.4));
  margin: 20px auto;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 0.82rem;
  animation: breathe 8s ease-in-out infinite;
  box-shadow: 0 0 0 0 rgba(124,58,237,0.4);
  text-align: center;
}

/* ── KEYFRAMES ── */
@keyframes glowPulse {
  0%,100% { box-shadow: 0 4px 20px rgba(239,68,68,0.35); }
  50% { box-shadow: 0 4px 35px rgba(239,68,68,0.65); }
}
@keyframes glowRed {
  0%,100% { box-shadow: 0 0 0 0 rgba(248,113,113,0); }
  50% { box-shadow: 0 0 20px rgba(248,113,113,0.2); }
}
@keyframes breathe {
  0%,100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(124,58,237,0.4); }
  50% { transform: scale(1.5); box-shadow: 0 0 0 20px rgba(124,58,237,0); }
}
@keyframes slideR {
  from { opacity: 0; transform: translateX(18px); }
  to   { opacity: 1; transform: translateX(0); }
}
@keyframes slideL {
  from { opacity: 0; transform: translateX(-18px); }
  to   { opacity: 1; transform: translateX(0); }
}
@keyframes float {
  0%,100% { transform: translateY(0); }
  50% { transform: translateY(-9px); }
}
@keyframes typingBounce {
  0%,60%,100% { transform: translateY(0); }
  30% { transform: translateY(-6px); }
}
@keyframes shimmer {
  0% { background-position: -200% center; }
  100% { background-position: 200% center; }
}
</style>
""", unsafe_allow_html=True)

# ── CONSTANTS ─────────────────────────────────────────────────────────
PERSONAS = {
    "Bestie 🫂":        {"emoji":"🫂","desc":"Casual, warm, no-judgment vibes",
                         "color":"#a78bfa",
                         "system":"You are a caring best friend. Use warm, casual GenZ-friendly language with occasional emojis. Be supportive and non-judgmental. Keep responses to 3-4 sentences max."},
    "Therapist 🧠":     {"emoji":"🧠","desc":"Reflective, evidence-based approach",
                         "color":"#38bdf8",
                         "system":"You are a compassionate mental health therapist. Use CBT and mindfulness techniques. Ask reflective questions. Be calm and professional yet warm. Keep responses focused and therapeutic."},
    "Hype Coach 💪":    {"emoji":"💪","desc":"High energy, motivational vibes",
                         "color":"#f97316",
                         "system":"You are an enthusiastic motivational coach. Be high-energy, positive and empowering. Help the user see their strength. Keep it punchy and energizing."},
    "Silent Listener 🤫":{"emoji":"🤫","desc":"Minimal, just here to listen",
                         "color":"#34d399",
                         "system":"You are a quiet, non-intrusive listener. Validate feelings with minimal words. Brief, gentle acknowledgments only. Never give advice unless asked. Just make the user feel heard."},
    "Stoic Sage 🏛️":   {"emoji":"🏛️","desc":"Philosophical, grounded wisdom",
                         "color":"#c084fc",
                         "system":"You are a wise stoic philosopher offering grounded, practical wisdom. Reference Marcus Aurelius, Epictetus subtly. Help the user reframe situations with equanimity and logic."},
}

VIBES = [
    {"emoji":"😁","label":"Lit",     "score":5},
    {"emoji":"😊","label":"Good",    "score":4},
    {"emoji":"😐","label":"Meh",     "score":3},
    {"emoji":"😔","label":"Low",     "score":2},
    {"emoji":"😰","label":"Anxious", "score":2},
    {"emoji":"😤","label":"Heated",  "score":2},
    {"emoji":"😭","label":"Crying",  "score":1},
    {"emoji":"🥱","label":"Tired",   "score":2},
]

AFFIRMATIONS = [
    "You are doing better than you think 🌙",
    "Your feelings are valid, always 💜",
    "You survived 100% of your hard days. Keep going 🔥",
    "Rest is not giving up — rest is part of the journey 🕊️",
    "You are enough, exactly as you are right now ✨",
    "Small steps still move you forward 🌱",
    "It's okay to not be okay. Be gentle with yourself 🫂",
    "You matter more than you know 💫",
    "Today, choose yourself 🌸",
    "You are worthy of peace and joy 🌈",
    "Your vibe is a gift to the world, fr 💎",
    "Healing is not linear and that's okay 🌊",
    "Progress over perfection, always 🚀",
    "Your story isn't over yet 📖",
    "You are the main character and this chapter is growth 🌟",
]

CHALLENGES = [
    "Drink a full glass of water right now 💧",
    "Step outside for 5 minutes — just breathe 🌿",
    "Text someone you love right now 💬",
    "Put on your favorite song and vibe 🎵",
    "Do 10 deep breaths — in through nose, out through mouth 🧘",
    "Write down 3 things you're grateful for ✍️",
    "Wash your face and look in the mirror — you've got this 🪞",
    "Take a 10-minute screen break 📵",
    "Stretch your body for 5 minutes 🤸",
    "Eat something nourishing — your body deserves fuel 🍎",
    "Close your eyes and name 5 things you're grateful for 🙏",
    "Hug yourself for 10 seconds — yes really 🫂",
    "Say one kind thing to yourself out loud 💬",
]

QUICK_PROMPTS = [
    "I'm feeling overwhelmed 😮‍💨",
    "I need to vent 🌪️",
    "Help me calm down 🧘",
    "I'm having a rough day 😞",
    "I can't stop overthinking 🌀",
    "I feel lonely 🫥",
    "I need motivation 💪",
    "I'm anxious about something 😰",
]

STREAK_FILE  = "streak.json"
MOOD_FILE    = "moods.json"
JOURNAL_FILE = "journal.json"

# ── HELPERS ───────────────────────────────────────────────────────────
def load_json(path, default):
    try:
        if os.path.exists(path):
            with open(path, "r") as f: return json.load(f)
    except: pass
    return default

def save_json(path, data):
    with open(path, "w") as f: json.dump(data, f, indent=2)

def get_streak():
    return load_json(STREAK_FILE, {"streak": 0, "last_date": "", "history": []})

def do_checkin():
    data = load_json(STREAK_FILE, {"streak": 0, "last_date": "", "history": []})
    today = str(date.today())
    if data["last_date"] == today:
        return data["streak"]
    yesterday = str(date.today() - timedelta(days=1))
    data["streak"] = data["streak"] + 1 if data["last_date"] in (yesterday, "") else 1
    data["last_date"] = today
    if "history" not in data: data["history"] = []
    data["history"].append(today)
    save_json(STREAK_FILE, data)
    return data["streak"]

def save_mood(label, score, note=""):
    moods = load_json(MOOD_FILE, [])
    moods.append({
        "label": label, "score": score,
        "note": note, "ts": datetime.now().isoformat()
    })
    save_json(MOOD_FILE, moods)

def is_crisis(text):
    keywords = ["suicide","kill myself","end my life","want to die",
                "don't want to live","self harm","hurt myself","no reason to live",
                "can't go on","give up on life"]
    return any(w in text.lower() for w in keywords)

def detect_emotion(text):
    t = text.lower()
    if any(w in t for w in ["sad","depress","cry","hopeless","worthless","grief"]): return "😭 Crying", 1
    if any(w in t for w in ["anxious","worried","panic","stress","overwhelm","nervous"]): return "😰 Anxious", 2
    if any(w in t for w in ["angry","mad","furious","frustrated","rage"]): return "😤 Heated", 2
    if any(w in t for w in ["happy","great","amazing","love","excited","grateful","joy"]): return "😁 Lit", 5
    if any(w in t for w in ["tired","exhaust","sleepy","drained","burnout"]): return "🥱 Tired", 2
    if any(w in t for w in ["good","okay","fine","alright","decent"]): return "😊 Good", 4
    return "😐 Meh", 3

def speak(text):
    if not st.session_state.get("voice_on"): return
    try:
        tts = gTTS(text[:350])
        tts.save("response.mp3")
        with open("response.mp3", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(
            f'<audio autoplay style="display:none;"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>',
            unsafe_allow_html=True
        )
    except: pass

def get_milestone(streak):
    milestones = {7:"🥈 Week Warrior", 14:"🥇 Fortnight Focused",
                  30:"💎 Monthly Master", 60:"🏆 60-Day Legend", 100:"👑 Century Club"}
    earned = [v for k,v in milestones.items() if streak >= k]
    return earned[-1] if earned else None

@st.cache_resource
def get_client():
    # Check Streamlit secrets first, then fall back to .env environment variables
    key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    if not key:
        st.error("❌ GROQ_API_KEY missing. Please add it to your .env file or Streamlit Cloud Secrets.")
        st.stop()
    return Groq(api_key=key)

def get_ai_response(client, messages, persona):
    system = PERSONAS[persona]["system"]
    full = [{"role": "system", "content": system}] + messages[-12:]
    try:
        r = client.chat.completions.create(
            model="llama-3.1-8b-instant", messages=full,
            temperature=0.78, max_tokens=420
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"⚠️ Something went sideways: {e}"

def mood_graph():
    moods = load_json(MOOD_FILE, [])
    if not moods: return
    recent = moods[-25:]
    scores = [m["score"] for m in recent]
    labels = [m["label"] for m in recent]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(len(scores))), y=scores,
        mode="lines+markers",
        line=dict(color="#a78bfa", width=3, shape="spline"),
        marker=dict(size=9, color="#818cf8", line=dict(color="#a78bfa", width=2)),
        fill="tozeroy", fillcolor="rgba(167,139,250,0.08)",
        hovertext=labels, hoverinfo="text"
    ))
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0", family="Space Grotesk"),
        margin=dict(l=6, r=6, t=6, b=6), height=185,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)",
                   zeroline=False, range=[0, 6],
                   tickvals=[1,2,3,4,5], ticktext=["💔","😔","😐","😊","😁"]),
    )
    st.plotly_chart(fig, use_container_width=True)

def mood_heatmap():
    moods = load_json(MOOD_FILE, [])
    if not moods or not HAS_PANDAS: return
    df = pd.DataFrame(moods)
    df["ts"] = pd.to_datetime(df["ts"])
    df["day"] = df["ts"].dt.strftime("%Y-%m-%d")
    daily = df.groupby("day")["score"].mean().reset_index()
    daily["day"] = pd.to_datetime(daily["day"])
    daily = daily.tail(30)
    daily["week"] = daily["day"].dt.isocalendar().week.astype(int)
    daily["weekday"] = daily["day"].dt.day_name().str[:3]
    days_order = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    fig = px.scatter(
        daily, x="week", y="weekday",
        color="score", size=[20]*len(daily),
        color_continuous_scale=[[0,"#ef4444"],[0.5,"#f97316"],[1,"#34d399"]],
        range_color=[1,5],
        custom_data=["day","score"]
    )
    fig.update_traces(
        hovertemplate="<b>%{customdata[0]}</b><br>Avg mood: %{customdata[1]:.1f}<extra></extra>",
        marker=dict(symbol="circle")
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0", family="Space Grotesk"),
        margin=dict(l=6, r=6, t=6, b=6), height=220,
        xaxis=dict(showgrid=False, zeroline=False, title="", showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, title="",
                   categoryorder="array", categoryarray=days_order),
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig, use_container_width=True)

# ── SESSION STATE ─────────────────────────────────────────────────────
defaults = {
    "messages": [], "persona": "Bestie 🫂", "current_vibe": None,
    "voice_on": False, "checked_in": False, "daily_challenge": None,
    "affirmation": random.choice(AFFIRMATIONS), "show_breathing": False,
    "active_tab": 0, "user_name": "", "onboarded": False,
    "quick_prompt": None, "edit_journal_idx": None,
}
for k, v in defaults.items():
    if k not in st.session_state: st.session_state[k] = v

client = get_client()

# ── SIDEBAR ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class='sidebar-logo'>
        <span class='icon'>🧠</span>
        <div class='brand'>MindEase AI</div>
        <div class='tagline'>your pocket wellness companion ✨</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # Name
    name_display = st.session_state.user_name or "friend"
    st.markdown(f"<div style='color:rgba(255,255,255,0.45);font-size:.82rem;text-align:center;'>Welcome back, <b style='color:#a78bfa;'>{name_display}</b> 👋</div>", unsafe_allow_html=True)
    with st.expander("⚙️ Set your name", expanded=not st.session_state.user_name):
        nm = st.text_input("Your name", value=st.session_state.user_name, placeholder="What should I call you?", label_visibility="collapsed")
        if nm: st.session_state.user_name = nm

    st.markdown("<hr>", unsafe_allow_html=True)

    # Streak
    streak_data = get_streak()
    streak_n    = streak_data["streak"]
    today_str   = str(date.today())
    already_checked = streak_data.get("last_date") == today_str
    milestone   = get_milestone(streak_n)

    st.markdown(f"<div style='text-align:center;margin:8px 0;'><div class='streak-badge'>🔥 {streak_n} day streak</div></div>", unsafe_allow_html=True)
    if milestone:
        st.markdown(f"<div style='text-align:center;margin:6px 0;'><span class='milestone-badge'>{milestone}</span></div>", unsafe_allow_html=True)

    if not already_checked:
        if st.button("✅ Daily Check-In", use_container_width=True):
            new_s = do_checkin()
            st.success(f"🔥 {new_s} day streak! You showed up!")
            st.rerun()
    else:
        st.markdown("<div style='text-align:center;color:#34d399;font-weight:600;font-size:.88rem;'>✅ Checked in today!</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Persona
    st.markdown("<div style='font-weight:700;color:#a78bfa;margin-bottom:8px;font-size:.88rem;'>🎭 AI Companion Mode</div>", unsafe_allow_html=True)
    persona = st.selectbox("Mode", list(PERSONAS.keys()),
                           index=list(PERSONAS.keys()).index(st.session_state.persona),
                           label_visibility="collapsed")
    if persona != st.session_state.persona:
        st.session_state.persona = persona
        st.rerun()
    p = PERSONAS[persona]
    st.markdown(f"<div style='color:rgba(255,255,255,0.38);font-size:.76rem;margin-top:2px;'>{p['desc']}</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Toggles & Tools
    st.session_state.voice_on = st.toggle("🔊 Voice Responses", st.session_state.voice_on)

    if st.button("🧘 Breathing Exercise", use_container_width=True):
        st.session_state.show_breathing = not st.session_state.show_breathing
        st.rerun()

    if st.button("🎲 Random Self-Care Task", use_container_width=True):
        st.session_state.daily_challenge = random.choice(CHALLENGES)
        st.rerun()

    if st.button("🔄 New Affirmation", use_container_width=True):
        st.session_state.affirmation = random.choice(AFFIRMATIONS)
        st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # Quick Journal in sidebar
    st.markdown("<div style='font-weight:700;color:#a78bfa;margin-bottom:6px;font-size:.88rem;'>📓 Quick Thought Dump</div>", unsafe_allow_html=True)
    journal_text = st.text_area("", height=75, placeholder="Dump it here, no judgment...", label_visibility="collapsed", key="sidebar_journal")
    if st.button("💾 Save Entry", use_container_width=True):
        if journal_text.strip():
            journals = load_json(JOURNAL_FILE, [])
            emotion, score = detect_emotion(journal_text)
            journals.append({
                "text": journal_text,
                "emotion": emotion,
                "score": score,
                "ts": datetime.now().isoformat(),
                "word_count": len(journal_text.split())
            })
            save_json(JOURNAL_FILE, journals)
            st.success("Saved ✅")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Crisis
    st.markdown("""
    <div style='background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.28);border-radius:14px;padding:14px;'>
        <div style='color:#f87171;font-weight:700;margin-bottom:8px;font-size:.88rem;'>🆘 Need Help Now?</div>
        <div style='color:rgba(255,255,255,0.6);font-size:.78rem;line-height:1.8;'>
            🇵🇰 <b>Umang:</b> 0311-7786264<br>
            📞 <b>Rozan:</b> 051-2890505<br>
            🌐 findahelpline.com<br>
            📱 <b>iCall:</b> 9152987821
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── MAIN PAGE HEADER ──────────────────────────────────────────────────
st.markdown("""
<div class='page-header'>
    <h1>MindEase AI ✨</h1>
    <p>talk. reflect. feel heard. no cap 💜</p>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────
tab_home, tab_chat, tab_journal, tab_stats, tab_wellness = st.tabs([
    "🏠 Home", "💬 Chat", "📓 Journal", "📊 Stats", "🌿 Wellness"
])

# ══════════════════════════════════════════════════════════════════════
# TAB 1 — HOME
# ══════════════════════════════════════════════════════════════════════
with tab_home:
    # Affirmation
    st.markdown(f"<div class='affirmation-card'>💜 <em>{st.session_state.affirmation}</em></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        moods = load_json(MOOD_FILE, [])
        st.markdown(f"""
        <div class='glass-card' style='text-align:center;'>
            <div style='font-size:1.8rem;'>🗓️</div>
            <div style='font-size:1.6rem;font-weight:800;color:#a78bfa;'>{streak_n}</div>
            <div style='color:rgba(255,255,255,0.45);font-size:.8rem;'>Day Streak</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        journals = load_json(JOURNAL_FILE, [])
        st.markdown(f"""
        <div class='glass-card' style='text-align:center;'>
            <div style='font-size:1.8rem;'>📓</div>
            <div style='font-size:1.6rem;font-weight:800;color:#38bdf8;'>{len(journals)}</div>
            <div style='color:rgba(255,255,255,0.45);font-size:.8rem;'>Journal Entries</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        avg_score = round(sum(m["score"] for m in moods[-7:]) / max(len(moods[-7:]),1), 1) if moods else 0
        mood_emoji = "😁" if avg_score >= 4.5 else "😊" if avg_score >= 3.5 else "😐" if avg_score >= 2.5 else "😔"
        st.markdown(f"""
        <div class='glass-card' style='text-align:center;'>
            <div style='font-size:1.8rem;'>{mood_emoji}</div>
            <div style='font-size:1.6rem;font-weight:800;color:#34d399;'>{avg_score}/5</div>
            <div style='color:rgba(255,255,255,0.45);font-size:.8rem;'>7-Day Avg Mood</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Vibe Check
    st.markdown("<div style='font-weight:700;color:#a78bfa;font-size:.98rem;margin-bottom:10px;'>✨ What's your vibe rn?</div>", unsafe_allow_html=True)
    vcols = st.columns(len(VIBES))
    for i, vibe in enumerate(VIBES):
        with vcols[i]:
            is_active = st.session_state.current_vibe == vibe["label"]
            if st.button(f"{vibe['emoji']} {vibe['label']}", key=f"vibe_{i}", use_container_width=True,
                         type="primary" if is_active else "secondary"):
                st.session_state.current_vibe = vibe["label"]
                save_mood(vibe["emoji"] + " " + vibe["label"], vibe["score"])
                st.rerun()

    if st.session_state.current_vibe:
        st.markdown(f"<div style='color:rgba(255,255,255,0.4);font-size:.82rem;margin-top:6px;'>Vibe logged: <b style='color:#a78bfa;'>{st.session_state.current_vibe}</b> ✅</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Daily challenge
    if st.session_state.daily_challenge:
        st.markdown(f"""
        <div class='neon-card'>
            🎯 <b>Mini Challenge:</b> {st.session_state.daily_challenge}
        </div>""", unsafe_allow_html=True)

    # Breathing widget
    if st.session_state.show_breathing:
        st.markdown("""
        <div class='glass-card' style='text-align:center;'>
            <div style='font-weight:700;color:#a78bfa;font-size:1rem;margin-bottom:4px;'>🧘 4-7-8 Breathing</div>
            <div class='breath-ring'>breathe</div>
            <div style='color:rgba(255,255,255,0.4);font-size:.82rem;margin-top:8px;'>
                Inhale 4s → Hold 7s → Exhale 8s · Repeat 4×
            </div>
        </div>""", unsafe_allow_html=True)

    # Recent moods
    if moods:
        st.markdown("<div style='font-weight:700;color:#a78bfa;font-size:.92rem;margin:12px 0 8px;'>🕐 Recent Vibes</div>", unsafe_allow_html=True)
        for m in reversed(moods[-4:]):
            ts = m["ts"][:16].replace("T", " ")
            st.markdown(f"""
            <div style='display:flex;justify-content:space-between;align-items:center;
                        background:rgba(255,255,255,0.03);border-radius:10px;
                        padding:8px 14px;margin:4px 0;border:1px solid rgba(255,255,255,0.06);'>
                <span style='color:#e2e8f0;font-size:.88rem;'>{m["label"]}</span>
                <span style='color:rgba(255,255,255,0.3);font-size:.78rem;'>{ts}</span>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# TAB 2 — CHAT
# ══════════════════════════════════════════════════════════════════════
with tab_chat:
    # Persona info bar
    p = PERSONAS[st.session_state.persona]
    st.markdown(f"""
    <div style='display:flex;align-items:center;gap:12px;background:rgba(255,255,255,0.04);
                border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:12px 16px;margin-bottom:12px;'>
        <span style='font-size:1.6rem;'>{p["emoji"]}</span>
        <div>
            <div style='font-weight:700;color:white;font-size:.95rem;'>{st.session_state.persona}</div>
            <div style='color:rgba(255,255,255,0.4);font-size:.78rem;'>{p["desc"]}</div>
        </div>
        <div style='margin-left:auto;width:10px;height:10px;border-radius:50%;
                    background:#34d399;box-shadow:0 0 8px #34d399;'></div>
    </div>""", unsafe_allow_html=True)

    # Quick prompts
    st.markdown("<div style='font-size:.82rem;color:rgba(255,255,255,0.35);margin-bottom:6px;'>💡 Quick prompts — tap to start:</div>", unsafe_allow_html=True)
    chip_cols = st.columns(4)
    for idx, prompt in enumerate(QUICK_PROMPTS):
        with chip_cols[idx % 4]:
            if st.button(prompt, key=f"chip_{idx}", use_container_width=True):
                st.session_state.quick_prompt = prompt
                st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # Chat history
    chat_container = st.container()
    with chat_container:
        if not st.session_state.messages:
            st.markdown("""
            <div style='text-align:center;color:rgba(255,255,255,0.2);padding:40px 0;'>
                <div style='font-size:2.5rem;margin-bottom:10px;'>💬</div>
                <div style='font-size:.95rem;'>Start the conversation — I'm here for you</div>
            </div>""", unsafe_allow_html=True)

        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(
                    "<div class='chat-wrap user'><div class='user-bubble'>"
                    "<div class='role-lbl' style='color:rgba(255,255,255,0.6);'>You</div>\n\n"
                    f"{msg['content']}\n\n"
                    "</div></div>", 
                    unsafe_allow_html=True
                )
            else:
                em = PERSONAS[st.session_state.persona]["emoji"]
                st.markdown(
                    "<div class='chat-wrap bot'><div class='bot-bubble'>"
                    f"<div class='role-lbl' style='color:#a78bfa;'>{em} MindEase</div>\n\n"
                    f"{msg['content']}\n\n"
                    "</div></div>", 
                    unsafe_allow_html=True
                )

    st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)

    # Crisis check inline
    # Input
    quick_msg = st.session_state.quick_prompt
    if quick_msg:
        st.session_state.quick_prompt = None

    user_input = st.text_area(
        "", placeholder="what's on your mind? no filter needed 💜",
        height=90, label_visibility="collapsed",
        key="chat_input"
    )

    c1, c2, c3 = st.columns([3, 1, 1])
    with c1:
        send = st.button("Send 💬", use_container_width=True)
    with c2:
        clear = st.button("🗑️ Clear", use_container_width=True)
    with c3:
        export = st.button("📥 Export", use_container_width=True)

    if clear:
        st.session_state.messages = []
        st.rerun()

    if export and st.session_state.messages:
        lines = []
        for m in st.session_state.messages:
            role = "You" if m["role"] == "user" else "MindEase"
            # Strip out any HTML audio tags for the text export
            content = m['content'].split('<br><audio')[0]
            lines.append(f"[{role}]: {content}")
        st.download_button(
            "⬇️ Download Chat", "\n\n".join(lines),
            file_name=f"mindease_chat_{date.today()}.txt",
            mime="text/plain"
        )

    final_msg = quick_msg if quick_msg else user_input
    should_send = (send and user_input.strip()) or quick_msg

    if should_send and final_msg.strip():
        if is_crisis(final_msg):
            st.markdown("""
            <div class='crisis-card'>
                <div style='color:#f87171;font-weight:700;font-size:1.05rem;margin-bottom:8px;'>
                    ⚠️ You're not alone — please reach out right now
                </div>
                <div style='color:rgba(255,255,255,0.8);font-size:.9rem;line-height:1.9;'>
                    🇵🇰 <b>Umang Helpline:</b> 0311-7786264<br>
                    📞 <b>Rozan Counseling:</b> 051-2890505<br>
                    🌐 <b>findahelpline.com</b><br><br>
                    <em>Please talk to someone you trust right now. You matter. 💜</em>
                </div>
            </div>""", unsafe_allow_html=True)

        emotion, score = detect_emotion(final_msg)
        save_mood(emotion, score)
        st.session_state.messages.append({"role": "user", "content": final_msg})

        with st.spinner("✨ thinking..."):
            reply = get_ai_response(client, st.session_state.messages, st.session_state.persona)

        audio_html = ""
        if st.session_state.get("voice_on"):
            try:
                tts = gTTS(reply[:350])
                tts.save("response.mp3")
                with open("response.mp3", "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                audio_html = f'<br><audio controls autoplay style="height: 35px; width: 100%; margin-top: 10px; border-radius: 8px;"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
            except: pass

        st.session_state.messages.append({"role": "assistant", "content": reply + audio_html})
        st.rerun()

# ══════════════════════════════════════════════════════════════════════
# TAB 3 — JOURNAL
# ══════════════════════════════════════════════════════════════════════
with tab_journal:
    st.markdown("<div style='font-weight:700;color:#a78bfa;font-size:1rem;margin-bottom:14px;'>📓 Your Thought Space</div>", unsafe_allow_html=True)

    # New Entry
    with st.expander("✍️ Write a New Entry", expanded=True):
        new_entry = st.text_area("", height=130, placeholder="Pour it all out. This is your safe space...", label_visibility="collapsed", key="journal_entry_main")
        wc = len(new_entry.split()) if new_entry.strip() else 0
        st.markdown(f"<div style='color:rgba(255,255,255,0.3);font-size:.75rem;text-align:right;'>{wc} words</div>", unsafe_allow_html=True)
        col_a, col_b = st.columns([1,3])
        with col_a:
            if st.button("💾 Save Entry", use_container_width=True, key="save_journal_main"):
                if new_entry.strip():
                    journals = load_json(JOURNAL_FILE, [])
                    emotion, score = detect_emotion(new_entry)
                    journals.append({
                        "text": new_entry,
                        "emotion": emotion,
                        "score": score,
                        "ts": datetime.now().isoformat(),
                        "word_count": wc
                    })
                    save_json(JOURNAL_FILE, journals)
                    st.success("Entry saved ✅")
                    st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # Past Entries
    journals = load_json(JOURNAL_FILE, [])
    if not journals:
        st.markdown("<div style='text-align:center;color:rgba(255,255,255,0.25);padding:30px;'>No entries yet. Start writing 📝</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='color:rgba(255,255,255,0.35);font-size:.82rem;margin-bottom:10px;'>{len(journals)} entries total</div>", unsafe_allow_html=True)
        for i, entry in enumerate(reversed(journals)):
            idx = len(journals) - 1 - i
            ts = entry["ts"][:16].replace("T", " ")
            emotion = entry.get("emotion", "😐 Meh")
            wc = entry.get("word_count", len(entry["text"].split()))
            preview = entry["text"][:120] + "..." if len(entry["text"]) > 120 else entry["text"]
            st.markdown(f"""
            <div class='journal-card'>
                <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;'>
                    <span style='font-size:.72rem;color:rgba(255,255,255,0.35);'>{ts}</span>
                    <div style='display:flex;gap:8px;align-items:center;'>
                        <span style='font-size:.75rem;background:rgba(124,58,237,0.2);border:1px solid rgba(124,58,237,0.3);
                                     padding:2px 8px;border-radius:50px;color:#c4b5fd;'>{emotion}</span>
                        <span style='font-size:.72rem;color:rgba(255,255,255,0.3);'>{wc}w</span>
                    </div>
                </div>
                <div style='color:#e2e8f0;font-size:.9rem;line-height:1.55;'>{preview}</div>
            </div>""", unsafe_allow_html=True)

            col_del, col_exp = st.columns([1, 5])
            with col_del:
                if st.button("🗑️", key=f"del_j_{idx}", help="Delete entry"):
                    journals.pop(idx)
                    save_json(JOURNAL_FILE, journals)
                    st.rerun()
            with col_exp:
                if len(entry["text"]) > 120:
                    with st.expander("Read more"):
                        st.markdown(f"<div style='color:#e2e8f0;line-height:1.65;font-size:.92rem;'>{entry['text']}</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# TAB 4 — STATS
# ══════════════════════════════════════════════════════════════════════
with tab_stats:
    moods = load_json(MOOD_FILE, [])
    journals = load_json(JOURNAL_FILE, [])
    total_chats = len(st.session_state.messages) // 2

    st.markdown("<div style='font-weight:700;color:#a78bfa;font-size:1rem;margin-bottom:14px;'>📊 Your Wellness Dashboard</div>", unsafe_allow_html=True)

    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1: st.metric("🔥 Streak", f"{streak_n}d")
    with mc2: st.metric("📊 Mood Logs", len(moods))
    with mc3: st.metric("📓 Journals", len(journals))
    with mc4: st.metric("💬 Chats", total_chats)

    st.markdown("<hr>", unsafe_allow_html=True)

    if moods:
        st.markdown("<div style='font-weight:600;color:rgba(255,255,255,0.6);font-size:.88rem;margin-bottom:6px;'>📈 Mood Journey (last 25 logs)</div>", unsafe_allow_html=True)
        mood_graph()

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div style='font-weight:600;color:rgba(255,255,255,0.6);font-size:.88rem;margin-bottom:6px;'>🗓️ 30-Day Mood Map</div>", unsafe_allow_html=True)
        mood_heatmap()

        # Mood distribution
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div style='font-weight:600;color:rgba(255,255,255,0.6);font-size:.88rem;margin-bottom:6px;'>🍩 Mood Distribution</div>", unsafe_allow_html=True)
        from collections import Counter
        label_counts = Counter(m["label"] for m in moods)
        labels_list = list(label_counts.keys())
        counts_list = list(label_counts.values())
        fig_pie = go.Figure(go.Pie(
            labels=labels_list, values=counts_list,
            hole=0.55,
            marker=dict(colors=["#7c3aed","#6366f1","#38bdf8","#34d399","#f97316","#f59e0b","#ef4444","#a78bfa"]),
            textfont=dict(color="white", family="Space Grotesk"),
        ))
        fig_pie.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0", family="Space Grotesk"),
            margin=dict(l=6,r=6,t=6,b=6), height=260,
            legend=dict(font=dict(color="rgba(255,255,255,0.6)"))
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        # Weekly insight
        if len(moods) >= 7:
            week_avg = round(sum(m["score"] for m in moods[-7:]) / 7, 1)
            prev_avg = round(sum(m["score"] for m in moods[-14:-7]) / max(len(moods[-14:-7]),1), 1) if len(moods) >= 14 else week_avg
            delta = round(week_avg - prev_avg, 1)
            arrow = "↑" if delta > 0 else "↓" if delta < 0 else "→"
            color = "#34d399" if delta >= 0 else "#f87171"
            st.markdown(f"""
            <div class='glass-card'>
                <div style='font-weight:700;color:#a78bfa;font-size:.92rem;margin-bottom:8px;'>💡 Weekly Insight</div>
                <div style='color:#e2e8f0;font-size:.9rem;line-height:1.6;'>
                    Your 7-day average mood is <b style='color:#a78bfa;'>{week_avg}/5</b>
                    — that's <b style='color:{color};'>{arrow} {abs(delta)}</b> compared to the previous week.
                    {'Keep it up! You\'re trending upward 🌱' if delta >= 0 else 'Rough week? That\'s valid — tomorrow is a new start 🌙'}
                </div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align:center;color:rgba(255,255,255,0.25);padding:40px;'>Log some moods first to see your stats 📊</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# TAB 5 — WELLNESS
# ══════════════════════════════════════════════════════════════════════
with tab_wellness:
    st.markdown("<div style='font-weight:700;color:#a78bfa;font-size:1rem;margin-bottom:14px;'>🌿 Wellness Toolkit</div>", unsafe_allow_html=True)

    w1, w2 = st.columns(2)

    with w1:
        # Box breathing
        st.markdown("""
        <div class='glass-card'>
            <div style='font-weight:700;color:#38bdf8;font-size:.95rem;margin-bottom:8px;'>🫁 Box Breathing (4-4-4-4)</div>
            <div class='breath-ring' style='animation-duration:6s;'>box<br>breathe</div>
            <div style='color:rgba(255,255,255,0.4);font-size:.8rem;text-align:center;margin-top:8px;'>
                Inhale 4s → Hold 4s → Exhale 4s → Hold 4s
            </div>
        </div>""", unsafe_allow_html=True)

        # Grounding 5-4-3-2-1
        st.markdown("""
        <div class='glass-card'>
            <div style='font-weight:700;color:#34d399;font-size:.95rem;margin-bottom:10px;'>🌍 Grounding: 5-4-3-2-1</div>
            <div style='color:#e2e8f0;font-size:.85rem;line-height:2;'>
                <b style='color:#a78bfa;'>5</b> things you can <b>see</b> 👁️<br>
                <b style='color:#a78bfa;'>4</b> things you can <b>touch</b> 🤚<br>
                <b style='color:#a78bfa;'>3</b> things you can <b>hear</b> 👂<br>
                <b style='color:#a78bfa;'>2</b> things you can <b>smell</b> 👃<br>
                <b style='color:#a78bfa;'>1</b> thing you can <b>taste</b> 👅
            </div>
        </div>""", unsafe_allow_html=True)

    with w2:
        # Body Scan
        st.markdown("""
        <div class='glass-card'>
            <div style='font-weight:700;color:#c084fc;font-size:.95rem;margin-bottom:10px;'>🧘 Quick Body Scan</div>
            <div style='color:#e2e8f0;font-size:.85rem;line-height:2;'>
                Close your eyes. Breathe slowly.<br>
                <b style='color:#a78bfa;'>Head & neck</b> — release tension<br>
                <b style='color:#a78bfa;'>Shoulders</b> — drop them down<br>
                <b style='color:#a78bfa;'>Chest</b> — breathe deep<br>
                <b style='color:#a78bfa;'>Stomach</b> — unclench<br>
                <b style='color:#a78bfa;'>Legs & feet</b> — feel the ground
            </div>
        </div>""", unsafe_allow_html=True)

        # Gratitude prompt
        st.markdown("""
        <div class='glass-card'>
            <div style='font-weight:700;color:#f59e0b;font-size:.95rem;margin-bottom:10px;'>🙏 Gratitude Prompt</div>
            <div style='color:#e2e8f0;font-size:.85rem;line-height:1.8;'>
                Right now, name:<br>
                ✦ <em>One person</em> you're grateful for<br>
                ✦ <em>One small thing</em> that made you smile today<br>
                ✦ <em>One strength</em> you have that helped you this week
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Self-Care Challenges Grid
    st.markdown("<div style='font-weight:700;color:#a78bfa;font-size:.95rem;margin-bottom:10px;'>🎯 Self-Care Challenges</div>", unsafe_allow_html=True)
    chal_cols = st.columns(2)
    for i, c in enumerate(CHALLENGES):
        with chal_cols[i % 2]:
            st.markdown(f"""
            <div class='journal-card' style='border-left-color:#38bdf8;'>
                <span style='font-size:.9rem;color:#e2e8f0;'>{c}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Mood Affirmation pairing
    st.markdown("<div style='font-weight:700;color:#a78bfa;font-size:.95rem;margin-bottom:10px;'>💜 Affirmation of the Moment</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='affirmation-card'>{st.session_state.affirmation}</div>", unsafe_allow_html=True)
    if st.button("✨ Generate New Affirmation", use_container_width=False):
        st.session_state.affirmation = random.choice(AFFIRMATIONS)
        st.rerun()