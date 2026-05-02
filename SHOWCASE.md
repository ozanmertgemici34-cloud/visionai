# F.R.I.D.A.Y — Personal AI Assistant System

> *"Female Replacement Intelligent Digital Assistant Youth"*
> Built from scratch, inspired by Iron Man's FRIDAY.

---

## What Is This?

FRIDAY is a fully functional personal AI assistant that runs on a Windows machine. Unlike Siri or Google Assistant, **FRIDAY actually controls your computer.** It opens applications, manages files, researches the web, runs code, remembers you, and speaks in your language.

It works via voice or text commands. For every request, it automatically picks the right AI model — a free local model for simple questions, a cloud API with tool-calling for research and actions.

---

## Architecture — How It Works

```
User (voice / text)
        ↓
   STT (Whisper / Google)
        ↓
   Smart Router — which model?
   ├── Simple question  → Ollama (local, free, ~0.8s)
   └── Research/action  → OpenAI GPT-4.1-mini (streaming + tool calling)
                                ↓
                          82 Tools available
                    (web, files, desktop, code, memory...)
                                ↓
                          TTS (edge-tts)
                                ↓
                      Voice output + JARVIS HUD
```

**Smart Routing:** Every query is analyzed before a model is chosen.
- *"How are you?"* → Local model. Zero API cost, 0.8 seconds.
- *"Who is Elon Musk?"* → OpenAI + web search + Wikipedia read.
- *"Open Chrome and play YouTube"* → OpenAI + desktop automation tools.

---

## Capabilities

### Desktop Control
Full computer control via natural language.

| Command | What It Does |
|---|---|
| "Open Spotify" | Launches the application |
| "Minimize Chrome" | Minimizes the window via Win32 API |
| "Set volume to 60%" | Adjusts system audio |
| "What's on my screen?" | Takes screenshot, analyzes with AI vision |
| "Click that button" | Moves mouse to correct position and clicks |
| "Open Notepad, write this, save it" | Multi-step automation, single command |
| "Minimize all windows" | Shows desktop (Win+D) |

### Web Research — 3-Tier System
Picks the right tool based on the question type:

| Tool | When Used | Depth |
|---|---|---|
| `search_web` | Quick info, prices, rates | Summary (snippets) |
| `read_webpage` | Read a specific URL | Full page (4,000 chars) |
| `search_and_read` | "Who is X / tell me about X" | Search + full article read |

```
"Who is Tesla?" → search_and_read → reads Wikipedia → summarizes
"What's the dollar rate?" → search_web → live exchange rate
"Read this page: ..." → read_webpage → full content
```

### Live Information
- Turkish news headlines (Hürriyet, CNN Türk, etc.)
- International news
- Weather for any city
- Stock prices, currency rates, crypto

### File & System Management
```
"Find file named: report"
"List this folder"
"Move / copy / delete a file"
"How much disk space is left?"
"Show running processes"
```

### Python Code Execution
FRIDAY writes and runs Python code on the fly:

```
"Calculate the sum of numbers from 1 to 100"
  → Writes Python → runs it → "Result: 5050"

"List the files on my Desktop"
  → os.listdir() code → runs it → reads results aloud

"Install pandas and analyze this CSV"
  → pip install → writes code → runs it
```

### Clipboard Integration
Copy → Say → Result goes straight back to your clipboard:

```
[Copy an English article]
"Translate this to Turkish"
→ Reads clipboard → translates with GPT → writes result back to clipboard → Ctrl+V and done

[Copy an email draft]
"Fix and make this more professional"
→ Reads it → improves it → puts result in clipboard

[Copy an error message]
"Explain this"
→ Analyzes the error → explains in plain language
```

### Memory System — It Remembers You

**Automatic:** Key facts are extracted from every conversation and saved in the background. No command needed.

```
Today: "I live in Istanbul and I'm a Python developer."
        → [FACT] Ozan lives in Istanbul.
        → [FACT] Ozan is a Python developer.

Tomorrow: "Suggest a project for me"
           → FRIDAY uses the Istanbul + Python context in its answer
```

**Manual:** `"Remember this: ..."` also works.

**170+ memory records** — preferences, goals, events, context, facts.

**Semantic search:** Ask "someone who codes in Python" → finds "Ozan is a Python developer."

### Reminders & Notes
```
"Remind me about the meeting in 30 minutes"
"Take a note: meeting with X tomorrow"
"Read my notes"
```

### Steam & Gaming
```
"Open Steam"
"List my installed games"
"Launch CS2"
"What's the price of Half Life 3?" → Steam store search
```

### YouTube Control
```
"Play lo-fi music on YouTube"
"Search Python tutorial on YouTube"
```

---

## Tech Stack

| Component | Technology |
|---|---|
| **UI** | Qt / QML — JARVIS HUD-style interface |
| **Primary LLM** | OpenAI GPT-4.1-mini (streaming + tool calling) |
| **Local LLM** | Ollama — qwen2.5:7b (free, offline) |
| **Fallback LLM** | Google Gemini 2.5 Flash |
| **Vision** | Gemini Vision — screen analysis |
| **STT** | faster-whisper / Google Speech-to-Text |
| **TTS** | edge-tts (tr-TR-AhmetNeural) + pyttsx3 fallback |
| **Memory** | TF-IDF + semantic embeddings (OpenAI) |
| **Desktop automation** | pyautogui + Win32 API |
| **Code execution** | Python subprocess (sandboxed, 30s timeout) |
| **Web research** | httpx + BeautifulSoup4 + Wikipedia REST API |
| **Platform** | Windows 11, Python 3.14 |

---

## Tools — 82 Total

```
Desktop     : open_application, close_application, minimize_window,
              maximize_window, focus_window, minimize_all_windows,
              list_windows, set_window_size

Screen      : look_at_screen, find_and_click, click_at, right_click_at,
              type_text, press_key, scroll

Web         : search_web, read_webpage, search_and_read,
              get_turkish_news, get_world_news, get_weather,
              youtube_search, youtube_play, google_search

Audio       : set_volume, volume_up, volume_down, mute_volume,
              media_play_pause, media_next, media_prev

Files       : find_file, list_folder, read_file, write_text_file,
              rename_file, move_file, copy_file, delete_file

System      : get_system_stats, list_processes, kill_process,
              run_powershell, lock_screen, sleep_mode,
              get_clipboard, set_clipboard, get_disk_space_info

Code        : run_python_code, run_python_file, install_package

Memory      : remember_this, recall_memory, forget_memory, memory_stats

Notes       : take_note, read_notes, clear_notes

Reminders   : set_reminder, list_reminders, cancel_reminder

Browser     : youtube_search, youtube_play, google_search, open_website

Steam       : steam_open_library, steam_list_installed,
              steam_launch_game, steam_search_game, steam_install_game
```

---

## Example Conversations

```
You: "What's the weather like today?"
FRIDAY: "Istanbul, 18°C, partly cloudy. No need for an umbrella."

You: "Who is Einstein?"
FRIDAY: → reads Wikipedia
         "Albert Einstein (1879–1955) was a theoretical physicist best known
          for his theory of relativity. He received the Nobel Prize in
          Physics in 1921..."

You: "Fix the email I just copied"
FRIDAY: → reads clipboard → rewrites with GPT → puts result in clipboard
         "Done. Fixed version is in your clipboard, just paste it."

You: "List all .py files on my Desktop"
FRIDAY: → writes and runs Python code
         "Found 7 Python files on your Desktop: friday_test.py, ..."

You: "Remind me about coffee in 30 minutes"
FRIDAY: "Got it. I'll remind you in 30 minutes."
         [30 minutes later]
         "Hey — coffee time."

You: "Show my installed Steam games, then launch CS2"
FRIDAY: → steam_list_installed → shows list
         → steam_launch_game("CS2") → game starts
         "CS2 is running."
```

---

## Design Decisions

**Why two LLMs?**
GPT-4.1-mini is not free. Calling the cloud API for *"how are you?"* is wasteful. The router checks every query: word count, does it need the web, does it need tools? Simple queries stay local — this cuts API costs by ~70%.

**Why streaming?**
TTS can't start speaking until it has text. With streaming, the first sentence is spoken while GPT is still writing the rest — the user hears a response in ~400ms instead of waiting for the full answer.

**Why automatic memory?**
You shouldn't have to say "remember this." Important facts are extracted from every conversation in a background thread and stored. Next time, FRIDAY already knows the context.

**Why Win32 API for windows?**
pyautogui window management is unreliable. Win32 API handles minimize / maximize / close in milliseconds with no `time.sleep()` needed between operations.

**Why a code runner?**
When FRIDAY can execute code, it stops making things up. Need to calculate something? Run it. Need to list files? Run it. The result is always accurate.

---

## Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Ollama (local model) — optional
ollama pull qwen2.5:7b

# Set up environment variables
cp .env.example .env
# Add your OPENAI_API_KEY and GEMINI_API_KEY

# Run
python app_qt.py
```

---

## Developer

**Ozan** — JarvisBrain v2, 2025–2026
Windows 11 · Python 3.14 · GPT-4.1-mini · Ollama · edge-tts

---

*"I don't claim to have done something without calling the right tool. Instead of saying I can — I do."*
— F.R.I.D.A.Y.
