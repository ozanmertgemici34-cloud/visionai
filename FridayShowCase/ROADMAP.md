# F.R.I.D.A.Y. — Roadmap

Development status and direction. This reflects what is actually built.

---

## What Is Working Now

### Voice
- [x] Continuous microphone listening with voice activity detection (webrtcvad)
- [x] Groq Whisper large-v3 STT, Turkish-locked with prompt biasing
- [x] Local faster-whisper fallback (offline capable)
- [x] Hallucination filtering (foreign characters, Whisper artifacts, repetition)
- [x] Barge-in: interrupt FRIDAY mid-sentence by speaking
- [x] Echo suppression after TTS playback
- [x] Mic gain normalization and DC offset removal

### Text-to-Speech
- [x] Microsoft Neural TTS (edge-tts, Turkish voice)
- [x] Producer-consumer streaming: sentence N+1 generates while sentence N plays
- [x] Persistent asyncio event loop (eliminates per-call overhead)
- [x] Barge-in stop signal propagated to playback
- [x] Offline pyttsx3 fallback
- [x] Pre-initialized audio mixer (no cold-start delay on first utterance)

### LLM and Routing
- [x] Per-query routing between local and cloud models
- [x] Local path: Ollama-hosted small model, streaming, rolling 10-turn history
- [x] Cloud path: GPT-4.1-mini with streaming and tool calling
- [x] Gemini fallback when OpenAI quota is exhausted
- [x] Circuit breaker on local model (auto-fallback on degradation)
- [x] Local model keepalive (prevents cold-start delays)

### Memory
- [x] 5-category persistent store: preference, fact, goal, event, context
- [x] Importance scoring (0.0–1.0) per entry
- [x] Semantic retrieval (embedding similarity)
- [x] TF-IDF fallback when embeddings are unavailable
- [x] Keyword-based bulk deletion (exact-match, safe)
- [x] Similarity-based deletion (higher threshold, capped for safety)
- [x] Auto-extraction after each conversation turn (background, LLM-powered)
- [x] First-person to third-person normalization before extraction
- [x] Duplicate detection before writing
- [x] Automatic backup before every save
- [x] Restore from backup

### Tools
- [x] Parallel tool execution with per-tool timeout
- [x] Web search, page reading, search-and-read
- [x] Turkish news, world news
- [x] Weather (current conditions)
- [x] System stats (CPU, RAM, disk, battery, processes)
- [x] Window management (open, close, minimize, maximize, focus, list)
- [x] Keyboard and mouse automation
- [x] Screenshot capture
- [x] File read/write/create/delete
- [x] Clipboard read/write/process
- [x] Diagram generation (flowchart, mind map, sequence, ER, Gantt, pie)
- [x] Memory tools (remember, recall, forget, stats, restore)
- [x] Timer/reminder with voice announcement on fire
- [x] Python code execution

### UI
- [x] Qt/QML native Windows application
- [x] Canvas-rendered animated orb (60 fps, radial gradient glow, breathing animation)
- [x] Voice-reactive orb (expands and pulses with audio level)
- [x] Speaking state: expanding radiate rings
- [x] Scrollable conversation log
- [x] Text input (typed messages bypass STT, go directly to processing)
- [x] Status indicators (listening / thinking / speaking / error)

### Proactive Engine
- [x] Startup briefing: time + system status on every launch (direct TTS, no LLM call)
- [x] Idle detection: check-in after 25 minutes of silence
- [x] System alerts: RAM and battery warnings via direct TTS
- [x] Reminder firing: scheduled voice announcements

---

## What Is Next

### Short-term
- [ ] Session conversation log (persist full history to disk across restarts)
- [ ] Memory review UI (browse, edit, delete memories from the interface)
- [ ] Voice speed control (real-time adjustment without restart)
- [ ] Conversation summary ("what did we talk about recently?")

### Medium-term
- [ ] Plugin system (drop-in tool modules without modifying core)
- [ ] Offline-first mode (full functionality without internet)
- [ ] Scheduled tasks ("every morning at 8, tell me the weather and news")
- [ ] Screen awareness (describe what is visible, find UI elements)

### Long-term
- [ ] Multi-language support (while keeping Turkish as primary)
- [ ] Cross-device memory sync (encrypted)
- [ ] Custom TTS voice
- [ ] Autonomous multi-step task execution with confirmation gates

---

## Design Principles

- **Turkish-first** — every layer is optimized for Turkish before other languages
- **Local-capable** — core functionality works without cloud APIs; cloud enhances, not enables
- **No hallucinations out loud** — every fact FRIDAY states comes from a verified tool result or is flagged uncertain
- **Private by default** — personal memory, credentials, and behavioral data never leave the local machine
- **Fast first response** — the user hears FRIDAY start talking within 2 seconds of finishing their sentence
