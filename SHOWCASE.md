# 🎬 F.R.I.D.A.Y. — System Showcase

> Everything listed here is verifiable from source code, live test results, and actual measurements.  
> No marketing fluff. No inflated numbers.

---

## 🧠 What It Actually Does

F.R.I.D.A.Y. is a **persistent desktop AI layer** — not a chatbot you open in a browser tab.  
It listens, thinks, acts, remembers, and speaks — all without you touching a mouse.

---

## ⚡ Speed Benchmarks — Real Numbers

Tested on: Windows 11 · RTX 4060 · 16 GB RAM · Python 3.14.2  
**82 tools tested · 80 passed · 97.6% success rate**

### Local Operations (no internet required)

| Operation | Time | Method |
|-----------|------|--------|
| Minimize / close / focus window | **< 0.01s** | Win32 `ShowWindow` / `WM_CLOSE` |
| Write / read file | **< 0.003s** | Direct disk I/O |
| Create folder | **< 0.001s** | `Path.mkdir` |
| Mute / unmute volume | **~0.04s** | VK_MUTE key event |
| Set volume to X% | **~0.10s** | pycaw COM + `SetMasterVolumeLevelScalar` |
| List open windows | **< 0.001s** | Win32 `EnumWindows` |
| Launch application | **~0.38s** | `subprocess.Popen` |
| Find file on disk | **~1.05s** | Depth-limited search (max depth 4, 500 items) |
| Get system stats (CPU/RAM) | **~0.50s** | psutil |
| Set reminder | **~0.01s** | `threading.Timer` |
| Run Python code snippet | **~0.05s** | subprocess spawn |

### Network-Dependent Operations

| Operation | Time | Notes |
|-----------|------|-------|
| Web search (snippets) | **~2.3s** | DuckDuckGo API |
| Read full webpage | **~2.4s** | HTTP + HTML parse |
| Search + full read | **~7.9s** | Combined pipeline |
| Get weather | **~0.6s** | HTTP API |
| Render diagram | **~1.7s** | Mermaid.ink API |

### AI-Dependent Operations

| Operation | Time | Notes |
|-----------|------|-------|
| Screen vision analysis | **~11.8s** | Screenshot → Gemini Vision |
| Find & click by description | **~3.5s** | Gemini Vision |
| Generate diagram from text | **~5.3s** | LLM → Mermaid → PNG |
| Store memory (embed + write) | **~4.8s** | Embedding model + vector store |

---

## 🔀 Intelligent Model Routing

Every request is classified before processing begins. No manual switching.

```
Simple command / chat       →  GPT-4.1-mini    fast, cost-efficient
Complex reasoning (28+ words) →  o4-mini        deep thinking, strategy, debug
OpenAI failure (3×)         →  Gemini 2.5 Flash silent automatic fallback
Offline / free queries      →  Ollama local    zero cost, zero internet
```

The **28-word threshold** for o4-mini was tuned through empirical testing —  
short commands don't need a reasoning model; long multi-part questions do.

---

## 🧩 Smart Tool Selection

With 84 tools registered, sending all of them to the LLM every request would be wasteful.  
F.R.I.D.A.Y. runs a **pre-filter** before each call:

- Analyzes the query semantically
- Selects only the tools relevant to that request
- Reduces token overhead by **86–97%** per query
- Keeps latency low without sacrificing capability

The model sees exactly what it needs. Nothing more.

---

## 🗃️ Memory System — 173 Records

F.R.I.D.A.Y. stores memories across sessions without being told to.  
After every conversation, an extractor runs silently in the background.

**Current memory breakdown (live data):**

| Type | Count | Example |
|------|-------|---------|
| `fact` | 35 | "User prefers dark mode" |
| `context` | 44 | "Working on JarvisBrain project" |
| `event` | 38 | "Discussed RAG pipeline on 2026-04-15" |
| `goal` | 34 | "Wants to publish FRIDAY publicly" |
| `preference` | 22 | "Responds better to direct answers" |
| **Total** | **173** | |

Retrieval uses **TF-IDF + semantic embeddings** — not just keyword matching.  
When you ask "what did we talk about last week?", it actually finds the right records.

---

## 🎤 Voice Pipeline

```
[You speak]
    ↓
STT — faster-whisper (local, small model)
    ↓  (fallback: Groq Whisper cloud)
Intent classification + tool selection
    ↓
LLM response generation (streaming)
    ↓
TTS — edge-tts (tr-TR-EmelNeural)
    speech starts on the FIRST sentence, not after full response
    ↓
[You hear the answer]
```

**End-to-end latency (real measurements):**

| Scenario | Total Time | Rating |
|----------|-----------|--------|
| "What time is it?" | ~2.0–3.5s | 🟢 Excellent |
| "Open Notepad" | ~2.5–4.0s | 🟢 Good |
| "Set volume to 50%" | ~2.0–3.5s | 🟢 Good |
| "Minimize Chrome" | ~2.0–3.5s | 🟢 Good |
| "What's the weather?" | ~3.0–5.5s | 🟡 Acceptable |
| "Who is Nikola Tesla?" | ~10–18s | 🟠 Web research |
| "Look at my screen" | ~13–20s | 🟠 Vision API |
| "Draw a flowchart" | ~7–12s | 🟠 LLM dependent |

The bottleneck is never local processing — it's always network or cloud AI.

---

## 🛠️ 84 Tools Across 15 Categories

```
Window Management     ████████  8 tools   — minimize, maximize, focus, close, list
File System           ██████████ 10 tools  — read, write, find, move, copy, delete
Audio Control         █████████  9 tools   — volume, mute, media keys
Application Control   ██████     6 tools   — open, close, kill by name
Desktop Control       ██████████ 10 tools  — click, type, scroll, screenshot
Browser Control       ███        3 tools   — search, YouTube, open URL
Web Research          ██████     6 tools   — search, read page, search+read, news, weather
Process Control       ███        3 tools   — list, info, kill
Clipboard             ██         2 tools   — get, set
Memory                ████       4 tools   — remember, recall, forget, stats
Notes & Reminders     ██████     6 tools   — take note, read notes, set/list/cancel reminder
Code Execution        █████      5 tools   — run Python, run PowerShell, install package
Diagrams              ██         2 tools   — render Mermaid, generate from description
System Info           ████       4 tools   — CPU/RAM, disk, time, process list
Steam                 ███        3 tools   — list installed, search, launch game
```

---

## 🔧 Notable Engineering Decisions

### Parallel Tool Execution
Up to **6 tools fire simultaneously**. If you ask "minimize all windows, set volume to 40%, and open Spotify" — those three operations run in parallel, not sequentially.

### Barge-In Detection
You can interrupt F.R.I.D.A.Y. mid-sentence. VAD detects voice activity during TTS playback, stops audio immediately, and processes the new command. No waiting for it to finish talking.

### Streaming TTS
Speech begins on the **first sentence** of the LLM response — not after the complete answer is generated. For a 5-sentence answer, you hear sentence 1 while sentences 2–5 are still being generated.

### Local Fallback
Ollama (qwen2.5:7b) keeps the system running with **zero internet, zero cost**. If OpenAI goes down, you don't notice.

### Automatic Memory Extraction
After each session, a background process scans the conversation for facts, preferences, and events — and stores them. You never have to say "remember that". It just does.

### Proactive System
Five background triggers run continuously:
- **Morning briefing** — daily summary at startup
- **Battery monitor** — alerts below threshold
- **RAM monitor** — warns on high memory pressure
- **Reminder engine** — fires spoken alerts at exact scheduled times
- **Routine suggestions** — detects patterns (3+ occurrences, 2+ days) and suggests automations

---

## 🏗️ Architecture

| Layer | Technology |
|-------|------------|
| **UI** | PySide6 + QML (Qt 6) |
| **Voice Input** | faster-whisper (local) · Groq Whisper (cloud fallback) |
| **Primary LLM** | OpenAI GPT-4.1-mini |
| **Reasoning LLM** | OpenAI o4-mini (28+ word queries) |
| **Local LLM** | Ollama qwen2.5:7b |
| **Fallback LLM** | Google Gemini 2.5 Flash |
| **Vision** | Gemini Vision (screen analysis) |
| **Voice Output** | edge-tts tr-TR-EmelNeural · pyttsx3 fallback |
| **Memory** | TF-IDF + OpenAI embeddings · JSON store |
| **Desktop Control** | Win32 API · pyautogui |
| **Audio Control** | pycaw (COM) · VK media keys |
| **Web** | DuckDuckGo API · BeautifulSoup · RSS |

---

## 📊 Test Coverage

```
Total tools tested:     82  (2 skipped — require human interaction)
Passed:                 80
Failed:                  2  (app launch: mspaint/wordpad removed in Windows 11)
Success rate:         97.6%

Categories passing 100%:
  Window Management, File System, Audio Control, Notes/Reminders,
  Browser Control, Web Research, Clipboard, Diagrams, System Info, Steam

Time to run full test suite:  106 seconds
```

The 2 failures are not bugs in F.R.I.D.A.Y. — they're Windows 11 removing classic apps (Paint, WordPad) from PATH. All other tools pass.

---

## 💡 Real Commands It Handles

```bash
"Open Spotify"                          # app launches in ~0.38s
"Minimize Chrome"                       # Win32 SW_MINIMIZE, <1ms
"Set volume to 60%"                     # pycaw, ~100ms
"What's on my screen?"                  # screenshot → Gemini Vision
"Who is Ada Lovelace?"                  # DuckDuckGo → full Wikipedia read
"Fix the text I just copied"            # clipboard → GPT → back to clipboard
"Remind me about the meeting in 30 min" # fires at exact time, spoken aloud
"Draw a flowchart of this codebase"     # Mermaid → PNG → auto-opens
"Why is this code throwing a KeyError?" # routes to o4-mini reasoning
"Launch CS2"                            # Steam integration, direct launch
"What did we talk about last week?"     # semantic memory retrieval
"Run this Python snippet"               # sandboxed subprocess, result returned
```

---

## 📌 Status

Active development. Not publicly released.  
Public release, setup guide, and documentation coming soon.

---

**F.R.I.D.A.Y — by Ozzy**
