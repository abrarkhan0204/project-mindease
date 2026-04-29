# 🌿 MindEase – AI Mental Health Companion
### Complete Beginner's Setup Guide

---

## 📁 Project Files
```
mental_health_app/
├── app.py            ← Main application
├── requirements.txt  ← Python packages needed
└── README.md         ← This guide
```

---

## 🚀 STEP-BY-STEP SETUP (Do these in order)

---

### STEP 1 — Install Python
If you don't have Python installed:
- Go to: https://www.python.org/downloads/
- Download Python 3.10 or newer
- During install: ✅ CHECK "Add Python to PATH"
- Verify: Open terminal and type `python --version`

---

### STEP 2 — Open VS Code
1. Open VS Code
2. Click **File → Open Folder**
3. Select or create a folder called `mental_health_app`
4. Place `app.py` and `requirements.txt` inside this folder

---

### STEP 3 — Open Terminal in VS Code
- Press **Ctrl + ` ** (backtick key, next to 1)
- OR go to **Terminal → New Terminal**

---

### STEP 4 — Create a Virtual Environment (Recommended)
In the terminal, type these commands one by one and press Enter:

```bash
python -m venv venv
```

Then activate it:
- **Windows:**
  ```
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```
  source venv/bin/activate
  ```

You'll see `(venv)` appear in the terminal — that means it's working ✅

---

### STEP 5 — Install Required Packages
```bash
pip install -r requirements.txt
```
Wait for everything to install (takes 1-2 minutes).

---

### STEP 6 — Get Your Groq API Key
1. Go to: https://console.groq.com/
2. Sign up for a FREE account
3. Click **API Keys → Create API Key**
4. Copy the key (starts with `gsk_...`)
5. Keep it safe — you'll paste it into the app

---

### STEP 7 — Run the App!
```bash
streamlit run app.py
```

Your browser will automatically open to: **http://localhost:8501**

---

### STEP 8 — Use the App
1. In the **sidebar** (left side), paste your Groq API key
2. Type how you're feeling in the chat box
3. Click **Send** or use the emoji mood buttons
4. The AI will respond with empathy and coping strategies

---

## 🔑 Where to Enter API Key
- Look at the **LEFT SIDEBAR** in the app
- Find the **"Groq API Key"** field
- Paste your key there (starts with `gsk_`)
- The app connects automatically

---

## 🌟 Features Explained
| Feature | What it does |
|---|---|
| 💬 Chat | Talk to the AI companion |
| 🎭 Emotion Detection | Detects your emotional state from text |
| 💓 Sentiment Analysis | Positive / Negative / Neutral score |
| 📊 Intensity Meter | How strong the emotion is |
| 💡 Coping Strategies | Personalized tips in the sidebar |
| 🆘 Crisis Alert | Auto-detects crisis language and shows hotlines |
| 📈 Emotion Journey | Tracks your emotions across the conversation |
| 😊 Quick Mood Buttons | Tap an emoji to quickly share your mood |

---

## ❓ Troubleshooting

**Problem:** `command not found: streamlit`
**Fix:** Run `pip install streamlit` then try again

**Problem:** `ModuleNotFoundError: No module named 'groq'`
**Fix:** Run `pip install groq` then try again

**Problem:** App says "check your API key"
**Fix:** Make sure you pasted the full key from console.groq.com

**Problem:** Browser doesn't open automatically
**Fix:** Manually go to http://localhost:8501 in your browser

**Problem:** `venv\Scripts\activate` doesn't work on Windows
**Fix:** Run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` first, then try again

---

## 🛑 To Stop the App
Press **Ctrl + C** in the terminal

---

## ⚠️ Important Disclaimer
MindEase is an AI companion for emotional support only.
It does NOT replace professional mental health care.
In crisis situations, always contact:
- **988** (Suicide & Crisis Lifeline - US)
- **911** (Emergency)
- **findahelpline.com** (International)

---

*Built with Streamlit + Groq (LLaMA 3) 🌿*