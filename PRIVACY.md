# Privacy and Security Boundary

FRIDAY is designed as a personal desktop assistant. That means it may interact with sensitive local context in the private runtime: user preferences, session history, local files, app state, reminders, and automation commands.

This showcase repository intentionally does not contain that private runtime data.

---

## What Is Never Published Here

- API keys or provider credentials
- `.env` files
- Local memory files
- Session logs
- Personal assistant conversations
- Desktop automation secrets
- Private prompts containing personal data
- User-specific behavior profiles
- Runtime cache files

---

## Local-First Philosophy

FRIDAY is designed to feel present on the user's own machine. The assistant stores and retrieves personal context locally in the private runtime.

The public repository only explains the product and architecture. It is not a hosted assistant backend and does not collect user data.

---

## Why Some Code Stays Private

The private runtime includes desktop automation and personal memory behavior. Publishing that code directly could expose:

- Unsafe automation surfaces
- Personal workflow assumptions
- Internal prompt and routing policies
- Private runtime configuration
- Sensitive data-handling paths

The public showcase keeps the architecture understandable while keeping the actual user environment protected.

---

## Public Module Boundary

Some cognition concepts may be published as standalone libraries when they are safe, reusable, and do not expose private runtime behavior.

See [PUBLIC_MODULES.md](PUBLIC_MODULES.md).

---

## Responsible Disclosure

If you notice a security or privacy concern in a public FRIDAY-related repository, please open a GitHub issue with a clear description. Do not include secrets or private user data in the issue body.
