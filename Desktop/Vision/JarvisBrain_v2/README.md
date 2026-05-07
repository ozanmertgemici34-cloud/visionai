# 🧠 F.R.I.D.A.Y. — Personal Desktop AI System

> Not just an assistant. A system that thinks alongside you.

![Status](https://img.shields.io/badge/Status-Active%20Development-blue?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows%2011-brightgreen?style=flat-square&logo=windows)
![License](https://img.shields.io/badge/License-Apache%202.0-green?style=flat-square)
![Language](https://img.shields.io/badge/Multimodal-Turkish%20+%20English-red?style=flat-square)

---

## 🎯 What is F.R.I.D.A.Y.?

F.R.I.D.A.Y. (Female Replacement Intelligent Digital Assistant Youth) is a Windows-native personal AI desktop assistant inspired by Tony Stark's JARVIS. Unlike cloud-dependent assistants, it runs **entirely on your machine** with optional cloud fallback.

Built with modular architecture, persistent memory, and adaptive learning layers — it evolves with you over time.

---

## 🚀 Development Roadmap

### ✅ Completed
- [x] Core architecture (Brain + Router + Memory layers)
- [x] Windows desktop control (pyautogui + Win32 API)
- [x] Persistent memory system (5 categories, semantic + TF-IDF)
- [x] Voice interaction (faster-whisper STT + edge-tts TTS)
- [x] 50+ integrated tools (desktop, filesystem, browser, code execution)
- [x] Telegram bot integration (remote access)
- [x] Adaptive learning stones (MindStone, EchoStone, BondStone, IntuitionStone)
- [x] Multi-model routing (GPT-4.1-mini, o4-mini, Gemini, Ollama)
- [x] Streaming TTS (response starts before completion)

### 🔄 In Progress
- [ ] Memory deletion bug (forget command not working properly)
- [ ] Skills/plugin system implementation
- [ ] Test suite (CI/CD ready)
- [ ] Telegram user session (send files directly to user)

### 📋 Planned
- [ ] Wake-on-LAN (wake PC remotely via Telegram)
- [ ] Skills marketplace (community-contributed plugins)
- [ ] Cross-platform support (WSL2, Linux)
- [ ] Public beta release

---

## 📊 Project Stats

| Metric | Value |
|--------|-------|
| **Tools Integrated** | 50+ |
| **Memory Categories** | 5 (Preferences, Facts, Goals, Events, Context) |
| **Languages** | Turkish (primary), English |
| **Platform** | Windows 11 |
| **Models Supported** | GPT-4.1-mini, o4-mini, Gemini 2.5 Flash, Ollama |
| **STT** | faster-whisper (local), Groq Whisper (cloud) |
| **TTS** | edge-tts (tr-TR-EmelNeural/AhmetNeural), pyttsx3 |

---

## 🧩 Core Capabilities

### 🧠 Persistent Memory
Five-category memory system that learns continuously:
- **Preferences** — Movies, habits, communication style
- **Facts** — User profile, hardware, location
- **Goals** — Projects, ambitions, plans
- **Events** — Past conversations, completed tasks
- **Context** — Active projects, technical details

### 🖥️ Desktop Control
- Application launch/close (any Windows app)
- File operations (create, delete, move, copy, search)
- Screenshot + AI vision analysis (Gemini Vision)
- System stats (CPU, RAM, disk, battery)
- Steam game launcher
- Volume/media control
- Clipboard management

### 🎙️ Voice & Remote Access
- **Local voice:** Microphone → STT → Brain → TTS → Speaker
- **Telegram bot:** Control FRIDAY from anywhere in the world
- **Wake-on-LAN:** Wake sleeping PC via Telegram (planned)

### 🧬 Adaptive Learning
Four "stone" systems that evolve with each interaction:
- **MindStone** — Learns communication preferences
- **EchoStone** — Tracks comprehension patterns
- **BondStone** — Models user world knowledge
- **IntuitionStone** — Predicts conversation flow

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      app_new.py                       │
│                  (Qt Desktop UI)                     │
└─────────────────────┬───────────────────────────────┘
                      │
         ┌───────────┴───────────┐
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│  SafeBrainRouter │     │   Voice Backend  │
│                 │     │                 │
│  ┌───────────┐  │     │  ┌───────────┐  │
│  │LocalLLM   │  │     │  │LiveAudio  │  │  (Gemini Native)
│  │(Ollama)   │  │     │  └───────────┘  │
│  └───────────┘  │     │  ┌───────────┐  │
│  ┌───────────┐  │     │  │LocalVoice │  │  (STT→Router→TTS)
│  │   Brain   │  │     │  └───────────┘  │
│  │ (OpenAI)  │  │     │                 │
│  └───────────┘  │     └─────────────────┘
└─────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│                      Tools (50+)                       │
├─────────┬──────────┬──────────┬──────────┬──────────────┤
│Desktop │ System   │ Memory  │Browser  │Code Runner │
│(pyautogui)│Control │(5 categories)│(YouTube)│(Python)   │
├─────────┼──────────┼──────────┼──────────┼──────────────┤
│Filesystem│Steam   │Reminder │Notes    │Diagrams   │
│(read/write)│Tools │(timer)  │(quick notes)│(Mermaid)│
└─────────┴──────────┴──────────┴──────────┴──────────────┘
```

---

## 💻 Tech Stack

| Layer | Technology |
|-------|------------|
| **UI** | PySide6 + QML (Qt 6) |
| **Primary LLM** | OpenAI GPT-4.1-mini |
| **Reasoning LLM** | OpenAI o4-mini |
| **Local LLM** | Ollama (qwen2.5, llama variants) |
| **Fallback LLM** | Google Gemini 2.5 Flash |
| **Vision** | Gemini Vision (screen analysis) |
| **STT** | faster-whisper (local) · Groq Whisper (cloud) |
| **TTS** | edge-tts (Neural) · pyttsx3 (offline fallback) |
| **Memory** | TF-IDF + semantic embeddings · JSON store |
| **Desktop Control** | pyautogui · Win32 API |
| **Remote Access** | Telegram Bot API |

---

## 🎬 Example Commands

```
"Open Spotify"                    → App launches instantly
"What's on my screen?"             → Screenshot → Gemini Vision → AI analysis
"Who is Nikola Tesla?"             → Search + full Wikipedia read
"Fix the email I just copied"       → Clipboard → GPT → back to clipboard
"Remind me about the meeting in 30min" → Fires at exact time, spoken aloud
"Draw a flowchart of this system"   → Mermaid → PNG → opens automatically
"Why is this code throwing KeyError?" → o4-mini reasoning mode
"Launch CS2"                       → Steam integration, direct launch
```

---

## 📫 Contact & Links

- **Developer:** [Ozan Mert Gemici](https://github.com/codedbyOzzy)
- **Project Repo:** [codedbyOzzy/ProjectFRIDAY](https://github.com/codedbyOzzy/ProjectFRIDAY)
- **Showcase:** [showcasefridayv2.netlify.app](https://showcasefridayv2.netlify.app)

---

## 📌 Status

Currently in **active development**.  
Public beta and open-source release planned for future milestones.

⭐ Follow the repo for updates!

---

<p align="center">
  <em>"I am F.R.I.D.A.Y. How can I assist you today?"</em>
</p>