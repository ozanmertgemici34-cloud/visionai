# F.R.I.D.A.Y. — Desktop AI Assistant

**F**emale **R**eplacement **I**ntelligent **D**igital **A**ssistant **Y**outh

A personal AI assistant for Windows — built around Turkish-first voice interaction, persistent memory, and real desktop control. Inspired by Tony Stark's FRIDAY, designed for daily use.

---

## What It Does

FRIDAY listens, thinks, remembers, and acts. You talk to it (or type), it responds in natural Turkish, and it can reach into your desktop, the web, or its own memory to give you a useful answer.

- **Talks back** — Natural Turkish voice responses using Microsoft Neural TTS, streamed sentence by sentence so the first word plays within ~1 second of the model finishing
- **Listens continuously** — Voice activity detection keeps the mic open, transcription happens automatically when you speak
- **Remembers you** — Every conversation is analyzed in the background; preferences, facts, goals, and context are extracted and stored persistently
- **Uses tools** — Web search, system stats, weather, window management, clipboard, file operations, diagram generation, and more
- **Routes intelligently** — Simple conversational queries go to a fast local model; research, tool use, and complex questions go to a cloud model
- **Acts proactively** — Greets you on startup with the current time and system status, reminds you when things are due, checks in after long silences

---

## Interface

A custom Qt/QML desktop interface with a full-screen animated HUD. At the center is a live orb — an organic, breathing shape that reacts to voice activity, speaks with glowing rings when talking, and pulses quietly when idle. The conversation appears as a scrollable log alongside it.

No web browser. No Electron. Native Windows application.

---

## Voice Pipeline

```
Microphone
    ↓  (webrtcvad — detects when you start and stop speaking)
Audio capture
    ↓  (Turkish-locked Whisper via Groq cloud — fast, accurate)
Transcribed text
    ↓
LLM Router
    ↓  (local model for simple queries / cloud model for complex ones)
Response text  →  Memory extraction (background)
    ↓
Streaming TTS  (sentence N plays while sentence N+1 is being generated)
    ↓
Speaker
```

Barge-in is supported: speak while FRIDAY is talking and it stops immediately.

---

## Memory System

FRIDAY maintains a personal memory database organized into five categories:

| Category | What's stored |
|----------|--------------|
| `preference` | Things you like, dislike, or prefer |
| `fact` | Persistent facts about you (hardware, location, background) |
| `goal` | Plans, intentions, things you want to do |
| `event` | Things that happened |
| `context` | Projects, tools, technologies you work with |

Memories are extracted automatically after each conversation — no manual tagging needed. Each entry has an importance score. The most relevant memories for any given query are surfaced into the model's context window at inference time.

---

## Tool System

FRIDAY can call tools mid-conversation. Tools are grouped by category:

- **Web** — search, read pages, get news (Turkish and international), get weather
- **System** — CPU/RAM/disk stats, process list, battery status
- **Desktop** — open/close/minimize/maximize applications and windows, type text, click, take screenshots
- **Files** — read, write, create, delete files and folders
- **Clipboard** — read and write the clipboard; summarize, translate, or rewrite clipboard content
- **Memory** — explicit remember/recall/forget commands
- **Diagrams** — generate flowcharts, mind maps, sequence diagrams, and more from natural language

All tool calls happen within the same conversation turn — FRIDAY calls the tool, reads the result, and continues the response seamlessly.

---

## Language

FRIDAY speaks and understands Turkish exclusively. The STT pipeline is locked to Turkish, the LLM is instructed to respond only in Turkish, and all tool outputs are summarized in Turkish before being spoken.

---

## What This Repo Is

This folder is a public-facing showcase of the project's current capabilities, design decisions, and direction. The full source code — including the prompting framework, routing logic, memory engine, tool implementations, and personal configuration — is kept private.

> *"Most of what FRIDAY does is invisible. This is the part we can show."*
