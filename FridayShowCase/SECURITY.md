# Security and Privacy Guidelines

Guidelines for what can and cannot be shared publicly from this project.

---

## Never Share

| Category | Examples |
|----------|---------|
| Credentials | API keys, tokens, passwords, secrets |
| Configuration | `.env` files, any file containing `API_KEY` or `SECRET` |
| System prompts | LLM instructions, persona definitions, routing logic |
| Personal data | Memory database files, conversation logs |
| Runtime state | Session files, cached responses, model outputs |
| Internal logic | Tool implementation code, routing thresholds, circuit breaker config |
| Screenshots | Anything showing memory contents or personal information |

---

## Safe to Share

- High-level architecture descriptions (like `ARCHITECTURE.md`)
- Capability lists and feature status (like `ROADMAP.md`)
- Simplified pseudocode that illustrates a concept without revealing implementation
- General design decisions and tradeoffs
- Technology stack (what tools/libraries are used, not how they are configured)

---

## Pre-Publication Checklist

Before pushing any file to a public branch:

- [ ] No API keys, tokens, or passwords
- [ ] No `.env` file or partial `.env` content
- [ ] No system prompt text
- [ ] No memory database contents
- [ ] No full tool implementation code
- [ ] No screenshots with personal data visible
- [ ] All code samples clearly labeled as pseudocode or simplified examples

---

## Runtime Files to Exclude

Always verify these are absent before committing:

```
.env
*.backup.json
.friday_*.json
*.log
__pycache__/
*.pyc
.friday_app_cache.json
```
