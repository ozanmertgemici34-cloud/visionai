# JarvisBrain_v2 — F.R.I.D.A.Y. Desktop Assistant

JarvisBrain_v2 is a Windows-focused Turkish desktop assistant inspired by
F.R.I.D.A.Y. It provides a PySide6 chat UI, microphone input, Gemini/OpenAI
reasoning, text-to-speech, Gemini Live audio mode, and desktop automation tools.

The current codebase is a local desktop app. Older MCP/LiveKit/control-panel
entry points mentioned in previous documentation are not present in this folder.

## Current Entry Point

Run the desktop app:

```powershell
pip install -r requirements.txt
python app_new.py
```

The app opens a dark F.R.I.D.A.Y. interface where you can:

- Type commands in Turkish.
- Use the microphone button for short speech-to-text commands.
- Use Live mode for Gemini Native Audio.
- Hear responses through the TTS engine.
- Let the assistant call desktop tools when a command requires real action.

## Architecture

```text
app_new.py
  -> friday.brain.Brain
       -> Gemini 2.5 Flash primary
       -> OpenAI fallback after repeated Gemini failures
       -> friday.tools.actions.ALL_TOOLS
  -> friday.tts_engine.speak
  -> friday.live_audio.LiveAudioThread
```

### `app_new.py`

Main PySide6 desktop UI. It owns the chat window, text input, microphone button,
Live mode button, reset shortcut, worker threads, and TTS trigger.

Normal microphone mode records audio with `sounddevice`, converts it to WAV, and
uses `SpeechRecognition` Google STT with `tr-TR`.

### `friday/brain.py`

LLM orchestration layer. Gemini is the primary model:

- Default Gemini model: `gemini-2.5-flash`
- Default OpenAI fallback model: `gpt-4.1-mini`
- Tool calling is enabled for both Gemini and OpenAI.
- The system prompt requires Turkish, short answers, and real tool calls before
  claiming an action was completed.

### `friday/tools/actions.py`

General assistant tools:

- Open and close Windows applications.
- Create folders and delete files/folders.
- Open websites.
- Get current time and system stats.
- Fetch weather, Turkish news, world news, and web search results.
- Control volume and media keys.
- Discover installed apps from Start Menu shortcuts and the Windows registry.

### `friday/tools/desktop.py`

Desktop control tools using `pyautogui` and Gemini Vision:

- Type text.
- Press keys and hotkeys.
- Click and right-click coordinates.
- Scroll and wait.
- Look at the screen with Gemini Vision.
- Find a UI element from a screenshot and click it.
- Write files directly or open them in Notepad.

### `friday/live_audio.py`

Gemini Native Audio mode. It streams microphone PCM directly to Gemini Live and
plays PCM audio responses back through `sounddevice`.

This mode bypasses the classic STT/TTS path:

```text
microphone PCM -> Gemini Live API -> audio response -> speakers
```

### `friday/tts_engine.py`

Text-to-speech fallback chain:

1. Fish Audio, if `FISH_AUDIO_API_KEY` is configured.
2. `edge-tts`, using `FRIDAY_TTS_VOICE`.
3. `pyttsx3`, offline Windows fallback.

## Environment

Create a local `.env` file from `.env.example` and fill the keys you use.

Important variables used by the current code:

```env
GEMINI_API_KEY=
GOOGLE_API_KEY=
OPENAI_API_KEY=
GEMINI_LLM_MODEL=gemini-2.5-flash
OPENAI_LLM_MODEL=gpt-4.1-mini
FISH_AUDIO_API_KEY=
FISH_AUDIO_VOICE_ID=
FRIDAY_TTS_VOICE=tr-TR-EmelNeural
FRIDAY_TTS_RATE=+6%
FRIDAY_TTS_PITCH=+0Hz
FRIDAY_TTS_VOLUME=+0%
```

`GEMINI_API_KEY` or `GOOGLE_API_KEY` is required for the main Gemini brain,
Gemini Vision tools, and Live Audio mode. `OPENAI_API_KEY` is only needed for the
fallback path.

## Command Flow

Normal text flow:

```text
user text
  -> app_new.py
  -> Brain.process()
  -> Gemini/OpenAI
  -> tool calls when needed
  -> assistant response
  -> TTS
```

Normal microphone flow:

```text
microphone
  -> sounddevice recording
  -> SpeechRecognition Google STT
  -> Brain.process()
  -> tools/response
  -> TTS
```

Live audio flow:

```text
microphone PCM
  -> Gemini Live
  -> optional tool calls
  -> PCM audio response
  -> speakers
```

## Desktop Capabilities

The assistant can currently perform direct desktop actions, including:

- `open_application`
- `close_application`
- `create_folder`
- `delete_file`
- `open_website`
- `get_weather`
- `get_turkish_news`
- `get_world_news`
- `search_web`
- `set_volume`, `volume_up`, `volume_down`, `mute_volume`
- `media_play_pause`, `media_next`, `media_prev`
- `type_text`
- `press_key`
- `click_at`
- `right_click_at`
- `look_at_screen`
- `find_and_click`
- `write_text_file`
- `open_and_write_file`

## Known Gaps

- README previously referenced `server.py`, `agent_friday.py`, `app_qt.py`,
  `start.ps1`, and `.bat` launchers. Those files are not present in this
  current folder.
- `.env.example` still contains some provider options for Ollama, faster-whisper,
  LiveKit, and MCP that are not wired into the current `app_new.py` path.
- High-risk desktop actions are currently direct tool calls. There is no active
  confirmation token or arming policy in the present implementation.
- `pyautogui.FAILSAFE` is disabled in `desktop.py`, so mouse automation should be
  used carefully.
- The speech-to-text button depends on Google STT through `SpeechRecognition`;
  offline faster-whisper is listed in dependencies but not used by this UI path.

## Suggested Next Steps

- Add a safety/permission layer before destructive or high-risk desktop tools.
- Align `.env.example` with the actual runtime path or implement the provider
  switches it documents.
- Add simple launch scripts for Windows if double-click startup is desired.
- Add a small smoke test for tool schema generation and basic tool calls.
