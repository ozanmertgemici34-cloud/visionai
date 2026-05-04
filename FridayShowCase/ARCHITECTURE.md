# F.R.I.D.A.Y. — System Architecture

A high-level overview of how the system is structured. Implementation details are intentionally omitted.

---

## Layer Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Desktop UI (Qt/QML)                  │
│   Animated orb · Chat log · Status · Mic controls       │
└────────────────────────┬────────────────────────────────┘
                         │ user input (voice or text)
┌────────────────────────▼────────────────────────────────┐
│                    Voice Layer                          │
│   VAD → STT (Groq Whisper) → text pipeline             │
│   TTS (edge-tts, streaming) → Speaker                  │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                   LLM Router                            │
│   Local path (fast, offline-capable, conversational)    │
│   Cloud path (GPT-4.1-mini, tools, research)            │
└────────────────────────┬────────────────────────────────┘
                         │
        ┌────────────────┴─────────────────┐
        ▼                                  ▼
┌───────────────┐                 ┌────────────────────┐
│  Tool System  │                 │   Memory System    │
│  25+ tools    │                 │  5-category store  │
│  parallel     │                 │  auto-extraction   │
│  execution    │                 │  semantic recall   │
└───────────────┘                 └────────────────────┘
```

---

## Desktop UI

Built with Qt/QML. Runs as a native Windows application — no browser, no web runtime.

The visual centerpiece is a Canvas-rendered animated orb: a living, organic shape that breathes slowly at rest, reacts to incoming audio levels, and pulses with expanding radiate rings when speaking. All animation runs at 60 fps on the CPU.

Conversation history is displayed in a scrollable log alongside the orb. Text input and microphone controls are overlaid on the HUD. The UI communicates with the backend entirely through Qt signals — no polling, no shared state.

---

## Voice Layer

### Speech-to-Text

Microphone input is processed by a voice activity detection (VAD) loop that watches for the start and end of speech without blocking. When a complete utterance is captured, it is sent for transcription.

The transcription chain, in priority order:

1. **Groq Whisper large-v3** (cloud) — Turkish-locked with prompt biasing toward common commands and vocabulary. Fast and highly accurate for Turkish.
2. **faster-whisper** (local) — Offline fallback. Same Turkish constraints applied.
3. **Google STT** (cloud) — Final fallback if both Whisper paths are unavailable.

Hallucination filtering runs on all results: foreign-character detection, known Whisper artifacts, repetition patterns.

Barge-in monitoring runs in a background thread during TTS playback. If the microphone RMS exceeds a threshold, TTS stops immediately and the new utterance is processed.

### Text-to-Speech

Responses are synthesized using Microsoft's edge-tts service (Neural voices, Turkish). Playback uses pygame for low-latency audio output with barge-in support.

The TTS pipeline uses a **producer-consumer** architecture: as the LLM streams sentence N, the TTS producer is already generating the audio file for sentence N and queuing it. The consumer plays sentence N while the producer handles sentence N+1 in parallel. This eliminates the per-sentence generation gap that would otherwise occur in a sequential pipeline.

First audio typically plays within 1–2 seconds of the model starting to respond.

---

## LLM Router

The router decides whether each query goes to the local or cloud model based on query characteristics:

**Local path** — used for short, conversational, non-action queries. A small Ollama-hosted model with a rolling conversation history (last 10 turns). Fast response, no API cost, works offline for common exchanges.

**Cloud path** — used for research, tool use, web queries, complex reasoning, and anything requiring up-to-date information. Powered by GPT-4.1-mini with streaming output and parallel tool execution.

A circuit breaker monitors the local model's availability and response times. If it degrades, the router falls back to cloud automatically and silently.

---

## Memory System

A file-backed persistent store. Every entry has:

- `content` — the fact in plain Turkish text
- `category` — one of: `preference`, `fact`, `goal`, `event`, `context`
- `importance` — a 0–1 score used to prioritize retrieval
- `tags` — optional labels for fast filtering
- `created_at` — timestamp

**Auto-extraction** runs in a background thread after each conversation turn. A lightweight LLM call analyzes the exchange and identifies any new personal facts — preferences stated, goals mentioned, context revealed. Results are deduplicated before writing. A backup is created before every save.

**Retrieval** is semantic: when building context for a new query, the store finds the most relevant memories and surfaces them into the model's context window. The model can also trigger explicit `remember`, `recall`, and `forget` tool calls mid-conversation.

---

## Tool System

Tools are Python functions registered with the LLM. The model decides when to call them based on the conversation.

**Execution is parallel**: if the model calls multiple tools in one turn, they run concurrently. Each tool has a per-call timeout — a hanging tool does not block the conversation.

Tool categories:

| Category | Examples |
|----------|---------|
| Web | search, read page, Turkish news, world news, weather |
| System | CPU/RAM/disk/battery stats, process list |
| Desktop | open/close/minimize apps, focus windows, type, click, screenshot |
| Files | read, write, create, delete files and folders |
| Clipboard | read/write clipboard, summarize/translate/rewrite contents |
| Memory | remember, recall, forget, memory stats |
| Diagrams | flowchart, mind map, sequence diagram, ER diagram, Gantt |
| Time | current time, timezone conversion |

---

## Proactive Engine

A background engine that runs while the assistant is active:

- **Startup briefing** — runs once per session a few seconds after launch. Greets with the current time and system state (RAM, pending reminders). Goes directly to TTS — no LLM call.
- **Idle detection** — a brief check-in message after 25 minutes of silence.
- **Reminder system** — user-set reminders fire as voice announcements at the scheduled time.
- **System alerts** — RAM and battery warnings announced directly via TTS when thresholds are crossed.

---

## What Is Not Described Here

The following are intentionally excluded:

- System prompt content and structure
- Routing thresholds and decision logic
- Memory extraction prompts
- Tool implementation code
- Authentication and API configuration
- Personal user data and memory contents
