<p align="center">
  <img src="images/core-orange.png" width="800"/>
</p>
# 🧠 F.R.I.D.A.Y — Personal Desktop AI System

> Not just an assistant. A system that thinks alongside you.

🚀 In development — not publicly available yet

---

## ⚡ Overview

F.R.I.D.A.Y. is a local-first desktop AI system designed to go beyond traditional assistants.

Instead of relying on a single model or API, it uses multi-model orchestration combined with local execution to provide fast, reliable, and uninterrupted interaction.

---

## 🔥 Key Features

- Real-time voice interaction (Gemini Live Audio)
- Multi-model routing (GPT, Gemini, Groq, Ollama)
- Local execution (instant commands, zero latency)
- Automatic fallback (no interruptions if a model fails)
- Full desktop control (apps, system, media)
- Modular architecture (plugin-based system)
- Persistent memory (sessions, preferences)
- Steam integration (launch games via voice)

---

## 🧩 How It Works

F.R.I.D.A.Y. dynamically decides how to process each request:

- Simple tasks → executed locally  
- Complex queries → routed to the most suitable AI model  
- Failures → handled seamlessly via fallback  

No manual switching. No interruptions.

---

## 🖥️ Interface
<p align="center">
  <img src="images/core-gold.png" width="600"/>
</p>

Instead of a traditional chat interface, F.R.I.D.A.Y. uses a reactive system UI:

- A central AI core that visually responds  
- Wave-based feedback for thinking and speaking states  
- Real-time system status awareness  

The goal is to create an interface that feels responsive and alive.

---

## 🏗️ Architecture

- PySide6 + QML (UI layer)
- Gemini Live Audio (voice interaction)
- GPT / Gemini / Groq / Ollama (LLM layer)
- Edge-TTS (speech output)
- SQLite + JSON (memory system)

---

## 🎤 Example Commands

- "Who is Mauro Icardi?"
- "Launch Counter-Strike 2"
- "Show my games"
- "Set a reminder for tomorrow at 3 PM"
- "Set volume to 60%"
- "Take a note: buy groceries"
- "What’s on my screen?"

---

## 🎯 Vision

F.R.I.D.A.Y. is an attempt to build a persistent AI layer on top of the desktop —  
a system that evolves with the user instead of acting as a simple tool.

---

## 📌 Status

Currently in active development.  
Public release, documentation, and setup instructions will be shared soon.

---

⭐ If you find this interesting, consider starring the repo.

F.R.I.D.A.Y — by Ozzy
