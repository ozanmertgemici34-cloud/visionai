# Friday Showcase

Public preview repository for ** F.R.I.D.A.Y. Desktop Assistant**.

This repository is intentionally a showcase, not the full source code. It presents the product vision, UI direction, high-level architecture, safety boundaries, and selected pseudocode-style examples without exposing private prompts, local automation internals, API keys, personal memory data, or security-sensitive desktop control logic.

## What Is JarvisBrain_v2?

JarvisBrain_v2 is a Windows-focused desktop AI assistant inspired by cinematic systems like F.R.I.D.A.Y. and JARVIS. It combines a native desktop interface, voice interaction, long-term memory, LLM reasoning, text-to-speech, live audio mode, and controlled desktop tools.

The full project is developed privately while the public preview focuses on safe technical storytelling.

## Feature Preview

- Native desktop assistant experience.
- Turkish-first conversational flow.
- Text and microphone command input.
- Gemini/OpenAI-style reasoning pipeline.
- Optional live audio interaction mode.
- Persistent personal memory layer.
- Desktop automation tools with planned safety controls.
- Holographic QML interface experiments.
- Voice response through a TTS fallback chain.

## Architecture Preview

```text
User
  -> Desktop UI
  -> Assistant Brain
  -> LLM Provider
  -> Memory Layer
  -> Tool Router
  -> Desktop Actions / Web / Files / Voice
  -> Response + TTS
```

The private implementation includes provider-specific orchestration, tool schemas, local environment handling, UI integration, and personal runtime data. Those details are not included in this showcase.

## Memory Preview

The assistant keeps structured long-term memories such as:

- User preferences.
- Project context.
- Important events.
- Goals and plans.
- Conversation summaries.

The real memory data is private and never shipped in this repository.

## Safe Pseudocode Example

```python
class MemoryStore:
    def remember(self, content: str, category: str, importance: float) -> str:
        """Store a safe, user-approved memory item."""
        ...

    def recall(self, query: str, limit: int = 5) -> list[str]:
        """Return relevant memories for assistant context."""
        ...
```

This is not production code. It only communicates the design shape.

## Repository Contents

```text
FridayShowCase/
  README.md
  ARCHITECTURE.md
  SECURITY.md
  ROADMAP.md
  NOTICE.md
  preview/
    memory_preview.py
```

## Screenshots And Demo

Add screenshots or short GIFs here when ready:

```text
assets/
  screenshot-home.png
  holographic-ui-demo.gif
```

Recommended public media:

- Main assistant window.
- Holographic QML core UI.
- Short voice interaction demo.
- Memory inspector concept mockup.

Avoid sharing local paths, personal data, API keys, terminal logs, or real memory files.

## Status

This is a public showcase. The complete assistant source remains private during active development, safety hardening, and packaging work.
