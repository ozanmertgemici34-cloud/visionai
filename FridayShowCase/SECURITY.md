# Security And Privacy Notes

This showcase repository is designed to be safe for public GitHub visibility.

## Do Not Publish

Never include these files or details in the public showcase:

- `.env`
- API keys or tokens
- Local user paths
- Personal memory files
- Real conversation logs
- Full system prompts
- Destructive tool implementations
- Raw desktop automation code
- Browser/session credentials
- Command execution internals
- Private screenshots containing personal data

## Sensitive Runtime Files

The private project may produce local runtime files. Keep them out of the public repository:

```text
.friday_memory.json
.friday_memory.db
.friday_*.json
.friday_*.jsonl
.friday_neural_memory/
.env
*.log
```

## Public Sharing Rules

Use public-safe language:

- Say "desktop automation tools" instead of publishing exact automation code.
- Say "provider-based LLM routing" instead of exposing provider prompts.
- Say "persistent memory layer" instead of publishing real memories.
- Say "tool safety layer planned" if permission gating is still in progress.

## Recommended Safety Message

Use this note in the public README or release page:

> The full source code is private while security controls, local action permissions, and packaging are being developed. This repository is a technical and visual preview only.

## Before Pushing To GitHub

Check the showcase folder manually:

```powershell
Get-ChildItem -Recurse FridayShowCase
```

Then search for accidental secrets:

```powershell
Select-String -Path FridayShowCase\* -Pattern "API_KEY","SECRET","TOKEN","sk-","AIza" -Recurse
```

If anything private appears, remove it before publishing.
