# FRIDAY Synapse Roadmap

This roadmap tracks the public-facing direction of FRIDAY Synapse. The private Windows runtime evolves separately from this showcase repository.

---

## Current Phase: Private Beta Showcase

The current goal is to present FRIDAY clearly without exposing sensitive code or private user data.

Completed in the showcase:

- Public architecture narrative
- High-level module map
- Privacy and public/private boundary
- Product positioning as a Windows-native assistant
- Links to public ecosystem modules

Implemented in the private runtime:

- PySide6/QML desktop shell
- Voice input and neural TTS
- BrainCore event architecture
- Multi-model routing and fallback strategy
- Persistent memory and session history
- Desktop, web, file, system, Steam, Telegram, and reminder tools
- Proactive and adaptive cognition modules

---

## Near-Term Priorities

### 1. Showcase Quality

- Add polished screenshots and short product clips
- Add a concise feature matrix
- Add better architecture visuals
- Add a security and privacy explainer
- Add Turkish documentation entry point

### 2. Runtime Stability

- Keep the private runtime aligned with the public architecture
- Improve dependency and setup clarity
- Strengthen import, tool registry, and smoke tests
- Separate design/spec documents from executable Python modules

### 3. Public Module Strategy

- Clarify which cognition modules are public
- Package standalone modules with clean examples
- Keep sensitive desktop-control runtime private
- Publish conceptual documentation without leaking implementation details

---

## Medium-Term Goals

### Memory Review Surface

Give the user a safe way to inspect, prune, and correct long-term assistant memory.

### Better Proactive Briefings

Improve startup briefings, idle thoughts, and unresolved-topic surfacing so the assistant feels useful without becoming noisy.

### App-Aware Behavior

Let FRIDAY adapt its behavior based on the foreground application and active workflow.

### Voice Calibration

Add user-level preferences for speaking speed, voice personality, and interruption behavior.

---

## Long-Term Direction

### Personal AI Operating Layer

FRIDAY should become a reliable local assistant layer across desktop work: planning, memory, automation, research, and voice.

### Cross-Device Context

Explore safe ways to sync context between desktop and mobile surfaces without exposing private memory.

### Local Intelligence Expansion

Move more low-risk reasoning and memory tasks to local models for cost, privacy, and latency benefits.

---

## Non-Goals

This project is not trying to become:

- A generic chatbot clone
- A public dump of private assistant code
- A cloud-only SaaS assistant
- A tool that hides unsafe automation behind vague claims

FRIDAY's direction is personal, local-first, privacy-aware, and deeply integrated with the user's own machine.

---

## Last Updated

May 2026
