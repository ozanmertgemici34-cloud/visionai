from __future__ import annotations

import re


ACTION_PATTERNS = [
    re.compile(r"(?:yapılacak|todo|görev)[:\-]\s*(.+)", re.IGNORECASE),
    re.compile(r"^- \[ \]\s+(.+)$", re.IGNORECASE | re.MULTILINE),
]


def extract_action_items(text: str) -> list[str]:
    actions: list[str] = []
    if not text:
        return actions

    for pattern in ACTION_PATTERNS:
        actions.extend([m.strip() for m in pattern.findall(text) if m.strip()])

    lines = [line.strip(" -•\t") for line in text.splitlines() if line.strip()]
    for line in lines:
        if line.lower().startswith(("1)", "2)", "3)", "4)", "5)")) and any(
            kw in line.lower() for kw in ("ara", "yaz", "gönder", "oluştur", "kontrol et", "tamamla")
        ):
            actions.append(line)

    # de-dup preserving order
    uniq: list[str] = []
    for action in actions:
        if action not in uniq:
            uniq.append(action)
    return uniq[:10]
