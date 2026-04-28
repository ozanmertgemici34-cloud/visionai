"""Public-safe memory preview.

This file is intentionally simplified pseudocode. It is not the production
JarvisBrain_v2 memory implementation and does not include private prompts,
runtime files, user data, embeddings, or provider-specific logic.
"""

from dataclasses import dataclass
from enum import Enum


class MemoryCategory(str, Enum):
    PREFERENCE = "preference"
    FACT = "fact"
    EVENT = "event"
    GOAL = "goal"
    CONTEXT = "context"


@dataclass
class PublicMemory:
    content: str
    category: MemoryCategory
    importance: float = 0.5
    confidence: float = 0.8


class MemoryPreview:
    """Small public example that shows the intended API shape."""

    def __init__(self) -> None:
        self._items: list[PublicMemory] = []

    def remember(
        self,
        content: str,
        category: MemoryCategory = MemoryCategory.FACT,
        importance: float = 0.5,
    ) -> None:
        self._items.append(
            PublicMemory(
                content=content,
                category=category,
                importance=max(0.0, min(1.0, importance)),
            )
        )

    def recall(self, query: str, limit: int = 5) -> list[PublicMemory]:
        query_words = set(query.lower().split())

        def score(item: PublicMemory) -> float:
            content_words = set(item.content.lower().split())
            overlap = len(query_words & content_words)
            return overlap + item.importance + item.confidence

        return sorted(self._items, key=score, reverse=True)[:limit]


if __name__ == "__main__":
    memory = MemoryPreview()
    memory.remember(
        "The user prefers concise Turkish responses.",
        category=MemoryCategory.PREFERENCE,
        importance=0.8,
    )
    memory.remember(
        "The assistant UI uses a holographic desktop style.",
        category=MemoryCategory.CONTEXT,
        importance=0.7,
    )

    for item in memory.recall("What response style does the user prefer?"):
        print(f"[{item.category.value}] {item.content}")
