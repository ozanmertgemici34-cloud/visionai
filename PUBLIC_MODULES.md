# Public Modules and Private Runtime

FRIDAY Synapse is split into two worlds:

1. Public showcase and reusable cognition ideas
2. Private Windows assistant runtime

This boundary keeps the project presentable without exposing private code, local data, or unsafe automation internals.

---

## Public

These are appropriate for public repositories or documentation:

- High-level architecture
- Conceptual diagrams
- Standalone cognition modules
- Non-sensitive examples
- Product roadmap
- Privacy model
- Showcase images and demos

Examples:

- [ProjectFridaySynapse](https://github.com/codedbyOzzy/ProjectFridaySynapse)
- [Intelligence-Stones](https://github.com/codedbyOzzy/Intelligence-Stones)
- [THESingularity](https://github.com/codedbyOzzy/THESingularity)

---

## Private

These stay inside the private FRIDAY runtime:

- Full desktop assistant source code
- Local user memory and session files
- API credentials and provider setup
- Sensitive prompt chains
- Tool execution internals
- Desktop automation safety logic
- User-specific behavioral profiles
- Private logs and caches

---

## Why This Split Exists

FRIDAY is not only a research demo. It is a personal assistant that can operate around local files, apps, voice, and memory. The system needs a stronger privacy boundary than a normal sample project.

The public side should be useful enough to understand the architecture, but not detailed enough to reproduce a user's private runtime or expose sensitive control surfaces.

---

## Future Public Candidates

Potential future public modules:

- Voice pipeline reference implementation
- Stone architecture starter template
- Turkish STT/VAD tuning notes
- Lightweight memory scoring examples
- Example-only tool schema patterns

Each candidate should be reviewed for privacy, safety, and reuse value before publication.
