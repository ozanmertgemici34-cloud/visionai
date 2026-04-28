# Architecture Preview

This document describes the public, high-level architecture of JarvisBrain_v2 without exposing private implementation details.

## Core Flow

```text
Input
  -> UI Controller
  -> Assistant Brain
  -> Context Builder
  -> Memory Recall
  -> LLM Reasoning
  -> Tool Decision
  -> Safe Action Layer
  -> Response Renderer
  -> TTS / Live Audio Output
```

## Main Components

### Desktop UI

The assistant uses a native desktop-style interface designed for fast interaction, visual feedback, and future holographic/ambient modes.

Publicly safe details:

- Chat input.
- Microphone control.
- Assistant status states.
- Animated visual core.
- Response display.

Private details:

- Internal QML wiring.
- Runtime bridge code.
- Local file paths.
- Personal UI state.

### Assistant Brain

The brain coordinates model calls, tool calls, memory context, and final responses.

Publicly safe details:

- Provider-based reasoning.
- Tool-aware response flow.
- Turkish-first interaction style.
- Fallback-capable design.

Private details:

- Full system prompt.
- Provider keys.
- Tool schema internals.
- Safety-critical prompt instructions.

### Memory Layer

The memory layer stores structured long-term facts and retrieves relevant context before a response.

Publicly safe categories:

- preference
- fact
- event
- goal
- context

Private details:

- Real user memory files.
- Personal facts.
- Full extraction prompt.
- Runtime memory database.

### Tool Layer

The tool layer enables the assistant to perform useful desktop actions.

Publicly safe examples:

- Open an application.
- Search the web.
- Get current time.
- Read safe system status.
- Recall memory.

Private details:

- Destructive file operations.
- Screen automation internals.
- Exact command execution logic.
- Bypass or permission handling.

## Safety Boundary

The public showcase should describe capabilities without publishing dangerous implementation details. Any tool capable of modifying files, controlling the mouse/keyboard, reading personal data, or executing commands should be documented at a conceptual level only.

## Suggested Public Diagram

```text
                       +----------------+
                       | Desktop UI     |
                       +-------+--------+
                               |
                               v
                       +-------+--------+
                       | Assistant Brain|
                       +---+--------+---+
                           |        |
              +------------+        +-------------+
              v                                   v
      +-------+--------+                  +-------+--------+
      | Memory Layer   |                  | Tool Router    |
      +-------+--------+                  +-------+--------+
              |                                   |
              v                                   v
      +-------+--------+                  +-------+--------+
      | Context Builder|                  | Safe Actions   |
      +----------------+                  +----------------+
```

## Design Principle

The assistant should feel personal and capable, but the implementation must remain private until safety, permissions, packaging, and user-data controls are mature.
