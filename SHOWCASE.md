<div align="center">

# F.R.I.D.A.Y.
### Female Replacement Intelligent Digital Assistant Youth

*A real Iron Man AI — built from scratch, running on your desktop.*

---

**84 Tools &nbsp;·&nbsp; Dual-Model Intelligence &nbsp;·&nbsp; 170+ Memories &nbsp;·&nbsp; Parallel Execution &nbsp;·&nbsp; Streaming TTS**

</div>

---

## What Is This?

FRIDAY is a fully operational personal AI assistant that runs natively on Windows. It doesn't open a browser tab. It doesn't ask you to copy and paste. It **controls your computer**, **remembers you**, **reasons through hard problems**, and **speaks back to you** — in real time.

Think of it as the gap between a chatbot and a real AI assistant. FRIDAY lives on this side of that gap.

---

## Intelligence Architecture

### The Brain — Three-Tier Model System

Every query is automatically routed to the right model before processing begins:

```
Your voice or text
        │
        ▼
   Smart Router
   ├── Simple query (command, chat, lookup)
   │       └── GPT-4.1-mini   ──► fast, cheap, accurate       $0.40 / 1M tokens
   │
   ├── Complex query (analysis, debug, strategy, code)
   │       └── o4-mini        ──► deep reasoning, thinking     $1.10 / 1M tokens
   │
   └── Offline / free queries
           └── Ollama (local) ──► zero cost, zero internet
```

**How it decides:**
- "Open Chrome" → GPT-4.1-mini (command, instant)
- "Why is this code failing?" → o4-mini (reasoning required)
- "Compare these two approaches and suggest a strategy" → o4-mini
- "How are you?" → Ollama local (free, 0.8s)
- Queries over 18 words → o4-mini automatically

If OpenAI fails 3 times → Gemini 2.5 Flash takes over silently.

---

### Streaming Pipeline — You Hear the Answer While It's Still Thinking

```
GPT generates token #1  ──► sentence buffer
GPT generates token #2       │
GPT generates token #3       │ first sentence complete
        ...              ──► TTS starts speaking  ◄── ~400ms after you stop talking
GPT still generating         │
        ...              ──► next sentence queued
GPT done                 ──► last sentence spoken
```

No waiting for the full answer. Speech begins on the first sentence.

---

### Parallel Tool Execution

When multiple tools are needed, they run simultaneously:

```
Before:  get_weather(2s) → get_news(3s) → get_stats(1s) = 6 seconds
After:   ──── all three at once ────────────────────────= ~3 seconds
```

Up to 6 tools run in parallel. Results are returned in correct order.

---

### Conversation Memory — It Never Forgets

**Automatic extraction:** After every conversation turn, a background thread analyzes what was said and saves key facts — no "remember this" command needed.

```
You say:  "I'm working on a Python project and I prefer dark mode."
                              ↓  (background, non-blocking)
FRIDAY saves:  [PREFERENCE] Ozan prefers dark mode.
               [CONTEXT]    Ozan is working on a Python project.

Next session: FRIDAY already knows.
```

**Long session compression:** When a conversation reaches 20 messages, the oldest 12 are automatically summarized into a compact memory block. The context stays fresh. Nothing is lost.

**Current memory store: 170 records**
- 34 facts · 43 context entries · 38 events · 34 goals · 21 preferences
- Average importance score: 0.73
- Semantic search: "someone who codes Python" → finds the right memory

---

## Capabilities

### Desktop Control

FRIDAY controls Windows via Win32 API — millisecond response, no delays between operations.

| You say | What happens |
|---|---|
| "Open Spotify" | Application launches |
| "Minimize Chrome" | Win32 SW_MINIMIZE — instant |
| "Set volume to 60%" | System audio adjusted |
| "What's on my screen?" | Screenshot → AI vision analysis |
| "Click that button" | Mouse moves, clicks target element |
| "Open Notepad, write this, save it" | Multi-step automation, single command |
| "Minimize everything" | Win+D — all windows hidden |
| "Close VS Code" | Graceful WM_CLOSE, then force if needed |

---

### Web Research — Three-Tier System

```
search_web(query)        Fast search — titles + snippets
                         When: quick facts, prices, current events

read_webpage(url)        Full page content — up to 4,000 chars
                         When: read a specific article or page

search_and_read(query)   Search + read the best result in full
                         When: "who is X", "tell me about Y"
```

**Automatic routing:**
- "Weather in Istanbul" → `get_weather()` (direct API, not web)
- "Who is Nikola Tesla?" → `search_and_read()` (Wikipedia-level depth)
- "Dollar exchange rate" → `search_web()` (live result, fast)
- "Read this URL for me" → `read_webpage()` (full content)
- Turkish news → `get_turkish_news()` · World news → `get_world_news()`

---

### Python Code Execution

FRIDAY writes and runs Python in a sandboxed subprocess. 30-second timeout. Full stdout + stderr capture.

```
You:    "Calculate the factorial of 20"
FRIDAY: → writes Python → runs it → "2432902008176640000"

You:    "List all Python files on my Desktop"
FRIDAY: → os.listdir() → runs it → reads results aloud

You:    "Install requests and fetch data from this API"
FRIDAY: → pip install requests → writes fetch code → runs it → shows output

You:    "Run hesap.py"
FRIDAY: → finds the file → runs it → returns output
```

---

### Diagram Generation

From a natural language description to a rendered diagram — no Mermaid knowledge required.

```
You:    "Draw a flowchart of FRIDAY's architecture"
FRIDAY: → GPT writes Mermaid code → mermaid.ink renders PNG
         → saved to Desktop/FRIDAY_Diagrams/ → opens automatically
```

**Supported diagram types:**

| Type | Use case |
|---|---|
| `flowchart` | Process flow, decision trees, system architecture |
| `sequenceDiagram` | API calls, component communication |
| `mindmap` | Brainstorming, concept maps |
| `gantt` | Project timelines, schedules |
| `pie` | Ratios, percentages, distributions |
| `erDiagram` | Database schemas, data models |
| `classDiagram` | OOP class structure |
| `stateDiagram` | State machines, lifecycles |
| `timeline` | Historical events, chronology |

No npm. No Node.js. No local renderer. Rendered via mermaid.ink API — dark theme, instant output.

---

### Clipboard Integration

Copy something → tell FRIDAY what to do → result goes straight back to your clipboard.

```
[Copy English article]
"Translate this to Turkish"
→ reads clipboard → GPT translates → writes result back → Ctrl+V

[Copy email draft]
"Make this more professional"
→ reads it → rewrites → puts in clipboard

[Copy error message]
"Explain this error"
→ analyzes → explains in plain language → result in clipboard
```

---

### File & System Management

```
"Find file named: report"
"List this folder"
"Move / copy / rename / delete a file"
"How much disk space is left?"
"Show running processes — sorted by CPU"
"Run this PowerShell command"
```

---

### Reminders, Notes & Tasks

```
"Remind me in 30 minutes about the meeting"     → fires at exact time, spoken aloud
"Take a note: call X tomorrow"                  → saved permanently
"Read my notes"                                 → reads them back
"Cancel reminder #2"                            → cancelled
```

---

### Steam & Gaming

```
"Open Steam"
"List my installed games"
"Launch CS2"
"Search for Half Life 3 on Steam"              → price, AppID, store link
```

---

### YouTube

```
"Play lo-fi music on YouTube"                  → searches, opens browser, plays
"Search Python tutorial on YouTube"            → opens results
```

---

## Tech Stack

| Component | Technology | Role |
|---|---|---|
| **UI** | Qt 6 / QML | JARVIS HUD — canvas reactor, voice waveform, chat history |
| **Primary LLM** | OpenAI GPT-4.1-mini | Fast queries, tool calling, streaming |
| **Reasoning LLM** | OpenAI o4-mini | Complex analysis, debug, strategy |
| **Local LLM** | Ollama qwen2.5:7b | Free, offline, zero API cost |
| **Fallback LLM** | Google Gemini 2.5 Flash | Emergency — activates after 3 OpenAI failures |
| **Vision** | Gemini Vision | Screen analysis, find-and-click |
| **STT** | faster-whisper + Google STT | Local transcription with cloud fallback |
| **TTS** | edge-tts (tr-TR-AhmetNeural) | Streaming sentence-by-sentence, pyttsx3 fallback |
| **Memory** | TF-IDF + OpenAI embeddings | Semantic search across 170+ records |
| **Desktop automation** | pyautogui + Win32 API | Pixel-perfect, millisecond window ops |
| **Code execution** | Python subprocess | Sandboxed, 30s timeout, full I/O capture |
| **Web research** | httpx + BeautifulSoup4 | Three-tier: search / read / deep-read |
| **Diagram rendering** | Mermaid.js + mermaid.ink | 9 diagram types, dark theme, PNG output |
| **Parallel execution** | ThreadPoolExecutor | Up to 6 tools simultaneously |
| **Platform** | Windows 11, Python 3.14 | Native Win32, no WSL |

---

## All 84 Tools

```
Desktop Control    open_application · close_application · minimize_window
                   maximize_window · focus_window · minimize_all_windows
                   close_window · list_windows · set_window_size

Screen             look_at_screen · find_and_click · click_at · right_click_at
                   type_text · press_key · scroll

Web                search_web · read_webpage · search_and_read
                   get_turkish_news · get_world_news · get_weather
                   youtube_search · youtube_play · google_search · open_website

Audio              set_volume · volume_up · volume_down · mute_volume
                   get_volume · media_play_pause · media_next · media_prev

Files              find_file · list_folder · read_file · write_text_file
                   open_and_write_file · rename_file · move_file
                   copy_file · delete_file · delete_file_safe · get_file_info

System             get_system_stats · get_disk_space_info · list_processes
                   get_process_info · kill_process · run_powershell
                   lock_screen · sleep_mode · shutdown_computer · restart_computer
                   cancel_shutdown · empty_recycle_bin · shutdown_friday

Clipboard          get_clipboard · set_clipboard

Code               run_python_code · run_python_file · install_package

Diagrams           generate_diagram · render_mermaid

Memory             remember_this · recall_memory · forget_memory · memory_stats

Notes              take_note · read_notes · clear_notes

Reminders          set_reminder · list_reminders · cancel_reminder

Browser            youtube_search · youtube_play · google_search

Steam              steam_open_library · steam_list_installed · steam_launch_game
                   steam_search_game · steam_install_game

Window             minimize_window · maximize_window · close_window
                   focus_window · list_windows · minimize_all_windows
                   set_window_size
```

---

## Real Conversations

```
You:    "What's the weather like?"
FRIDAY: "Istanbul, 18°C, partly cloudy. No umbrella needed."

You:    "Who is Nikola Tesla?"
FRIDAY: → search_and_read() — reads full Wikipedia entry
         "Nikola Tesla (1856–1943) was a Serbian-American inventor and
          electrical engineer. Best known for developing alternating current
          electrical systems, he held over 300 patents..."

You:    "Fix the email I just copied"
FRIDAY: → get_clipboard() → GPT rewrites → set_clipboard()
         "Done. Fixed version is in your clipboard."

You:    "Why is my code throwing a KeyError on line 47?"
FRIDAY: → routes to o4-mini (reasoning mode)
         "The KeyError on line 47 happens because you're accessing
          data['user'] before checking if the API response actually
          contains that key. The response structure changes when..."

You:    "Draw a mindmap of machine learning concepts"
FRIDAY: → generate_diagram() → Mermaid → PNG rendered
         "Diagram created. Saved to Desktop/FRIDAY_Diagrams/. Opening now."

You:    "Give me today's news, weather, and system status"
FRIDAY: → 3 tools fire in parallel (~3s instead of ~7s)
         "Top story: ... Istanbul: 18°C ... CPU: 23%, RAM: 61%..."

You:    "Remind me about coffee in 20 minutes"
FRIDAY: "Got it."
         [20 minutes later, spoken aloud]
         "Coffee time."

You:    "Launch CS2"
FRIDAY: → steam_launch_game() → "CS2 is running."
```

---

## Design Decisions

**Why two cloud models?**
o4-mini costs 2.75x more than GPT-4.1-mini per token. Using it for every query is wasteful. The classifier routes only genuinely hard problems — analysis, debugging, strategy — to o4-mini. Simple commands and lookups stay on 4.1-mini. Net result: better answers where it matters, lower cost everywhere else.

**Why parallel tools?**
Sequential tool execution is an artificial bottleneck. If you ask for weather, news, and system stats simultaneously, there's no reason to wait for each one to finish before starting the next. ThreadPoolExecutor removes the bottleneck with six lines of code.

**Why automatic memory?**
Saying "remember this" shouldn't be a workflow step. A real assistant pays attention. Every conversation is scanned in a background thread — facts, preferences, goals — and stored without interrupting the response. By the next session, FRIDAY already has context.

**Why conversation compression?**
Language models have context limits. Without compression, long sessions degrade as old turns fall out of the window. With compression, the oldest turns are summarized before they're dropped — key information survives in compact form, and the conversation quality stays consistent across hours of use.

**Why Win32 API for windows?**
pyautogui-based window management requires `time.sleep()` calls between operations and is unreliable under load. Win32 SW_MINIMIZE and WM_CLOSE are synchronous OS calls — they complete in under a millisecond. No sleep. No race conditions.

**Why a local model at all?**
"How are you?" costs API money. So does "what time is it?" The local model (Ollama) handles conversational and simple factual queries for free. The router checks query complexity before touching the cloud. On typical usage patterns, this reduces API spend by 60–70%.

**Why streaming TTS?**
Without streaming, the user waits for the entire LLM response before hearing a single word. With sentence-by-sentence streaming, TTS begins on the first sentence while GPT is still writing the second. Perceived response time drops from 3–5 seconds to under 500ms.

---

## What Makes This Different

| Capability | FRIDAY | Typical AI Chatbot |
|---|---|---|
| Controls your computer | ✅ 84 tools | ❌ Text only |
| Remembers you across sessions | ✅ 170+ memories, semantic search | ❌ Resets every time |
| Chooses the right model per query | ✅ 3-tier routing | ❌ One model for everything |
| Works offline | ✅ Ollama local model | ❌ Always needs internet |
| Runs Python code | ✅ Sandboxed execution | ❌ |
| Generates diagrams | ✅ 9 types, instant render | ❌ |
| Parallel tool execution | ✅ Up to 6 simultaneous | ❌ Sequential |
| Speaks responses | ✅ Streaming TTS, <400ms | ❌ |
| Reads your clipboard | ✅ Translate/fix/summarize | ❌ |
| Manages Steam & games | ✅ | ❌ |
| Cost per day (typical use) | ~$0.05–0.20 | N/A |

---

## Getting Started

```bash
# Dependencies
pip install -r requirements.txt

# Local model (optional — enables free offline queries)
ollama pull qwen2.5:7b

# Environment
cp .env.example .env
# Set: OPENAI_API_KEY, GEMINI_API_KEY

# Run
python app_qt.py
```

**Optional `.env` overrides:**
```
OPENAI_LLM_MODEL=gpt-4.1-mini       # fast model (default)
OPENAI_COMPLEX_MODEL=o4-mini         # reasoning model (default)
FRIDAY_LOCAL_MODE=auto               # enable local model routing
FRIDAY_TTS_VOICE=tr-TR-AhmetNeural  # TTS voice
FRIDAY_WHISPER_MODEL=small           # STT model size
```

---

## Developer

**Ozan** — JarvisBrain v2 &nbsp;·&nbsp; 2025–2026
Windows 11 &nbsp;·&nbsp; Python 3.14 &nbsp;·&nbsp; GPT-4.1-mini + o4-mini &nbsp;·&nbsp; Ollama &nbsp;·&nbsp; Qt 6

---

<div align="center">

*"I don't claim to have done something without calling the right tool.*
*Instead of saying I can — I do."*

**— F.R.I.D.A.Y.**

</div>
