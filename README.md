# 🧠 F.R.I.D.A.Y — Personal Desktop AI System

> Not just an assistant. A system that thinks alongside you.

🚀 In active development — not publicly released yet

<p align="center">
  <img src="images/core-gold.png" width="800"/>
</p>

---

## ⚡ Overview

F.R.I.D.A.Y. is a local-first desktop AI system built for Windows — designed to go beyond traditional assistants.

Instead of relying on a single model or API, it uses **multi-model orchestration** combined with **direct OS-level control** to provide fast, reliable, and continuous interaction.

---

## 🔥 Key Features

- **Real-time voice interaction** — faster-whisper (local) + Groq fallback
- **Multi-model routing** — GPT-4.1-mini · o4-mini · Gemini 2.5 Flash · Ollama
- **84 integrated tools** — desktop control, web research, code execution, memory, and more
- **Persistent memory** — 173+ records, semantic search across sessions
- **Parallel tool execution** — up to 6 tools fire simultaneously
- **Streaming TTS** — speech starts on the first sentence, not after the full response
- **Local fallback** — Ollama keeps it running offline, for free
- **Automatic memory extraction** — learns from every conversation without being told to

---

## 🧩 How It Works

F.R.I.D.A.Y. dynamically decides how to handle each request before processing begins:

```
Simple command / chat    →  GPT-4.1-mini   (fast, cost-efficient)
Complex reasoning        →  o4-mini        (deep thinking, strategy, debug)
Offline / free queries   →  Ollama local   (zero cost, zero internet)
OpenAI failure (3x)      →  Gemini 2.5     (silent automatic fallback)
```

No manual switching. No interruptions.

---

## 🖥️ Interface

<p align="center">
  <img src="images/core-yellow.png" width="800"/>
</p>

Instead of a traditional chat interface, F.R.I.D.A.Y. uses a **reactive system UI** built in Qt 6 / QML:

- A central AI core that visually responds to state changes
- Wave-based feedback for listening, thinking, and speaking
- Real-time conversation history
- Always-on system awareness

The goal is an interface that feels alive, not like a browser tab.

---

## 🏗️ Architecture

<p align="center">
  <img src="images/core-orange.png" width="800"/>
</p>

| Layer | Technology |
|-------|------------|
| **UI** | PySide6 + QML (Qt 6) |
| **Voice Input** | faster-whisper (local) · Groq Whisper (cloud) |
| **Primary LLM** | OpenAI GPT-4.1-mini |
| **Reasoning LLM** | OpenAI o4-mini |
| **Local LLM** | Ollama (qwen2.5:7b) |
| **Fallback LLM** | Google Gemini 2.5 Flash |
| **Vision** | Gemini Vision (screen analysis) |
| **Voice Output** | edge-tts (tr-TR-EmelNeural) · pyttsx3 fallback |
| **Memory** | TF-IDF + semantic embeddings · JSON store |
| **Desktop Control** | Win32 API · pyautogui |

---

## 🎤 Example Commands

```
"Open Spotify"                          → app launches instantly
"Minimize Chrome"                       → Win32 SW_MINIMIZE, <1ms
"Set volume to 60%"                     → system audio adjusted
"What's on my screen?"                  → screenshot → Gemini vision analysis
"Who is Nikola Tesla?"                  → search + full Wikipedia read
"Fix the email I just copied"           → clipboard → GPT → back to clipboard
"Remind me about the meeting in 30 min" → fires at exact time, spoken aloud
"Draw a flowchart of this system"       → Mermaid → PNG → opens automatically
"Why is this code throwing a KeyError?" → o4-mini reasoning mode
"Launch CS2"                            → Steam integration, direct launch
```

---

## 🎯 Vision

F.R.I.D.A.Y. is an attempt to build a **persistent AI layer on top of the desktop** —  
a system that evolves with the user instead of acting as a stateless tool.

Every session, it knows more. Every command, it responds faster. Every conversation, it remembers.

---

## 📌 Status

Currently in active development.  
Public release, documentation, and setup instructions coming soon.

---

⭐ If you find this interesting, consider starring the repo.

**F.R.I.D.A.Y — by Ozzy**
