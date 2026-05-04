"""
F.R.I.D.A.Y. Memory System — Public Preview

This file illustrates the structure and behavior of FRIDAY's memory layer.
It is simplified pseudocode intended to communicate design decisions,
not a functional implementation of the actual system.

The real implementation includes:
  - Embedding-based semantic retrieval
  - TF-IDF fallback when embeddings are unavailable
  - Automatic extraction from conversation turns (LLM-powered, background thread)
  - Importance-weighted ranking
  - Keyword and similarity-based deletion with safety caps
  - Automatic backup before every write
  - Duplicate detection before storing
  - First-person to third-person normalization ("I have X" -> "User has X")

What you see here is the shape of the system — how it thinks about memory.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import time


class MemoryCategory(Enum):
    """Five categories cover the full range of personal context."""
    PREFERENCE = "preference"   # likes, dislikes, habits, defaults
    FACT       = "fact"         # persistent facts (hardware, location, background)
    GOAL       = "goal"         # intentions, plans, things the user wants
    EVENT      = "event"        # things that happened
    CONTEXT    = "context"      # projects, tools, technologies in use


@dataclass
class Memory:
    """A single memory entry."""
    content:    str
    category:   MemoryCategory
    importance: float = 0.6          # 0.0 (trivial) -> 1.0 (critical)
    tags:       list[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)

    def __post_init__(self) -> None:
        self.importance = max(0.0, min(1.0, self.importance))


class MemoryPreview:
    """
    Simplified preview of the memory store.

    The real store uses semantic embeddings for recall and supports
    multi-field queries, category filtering, and importance-weighted ranking.
    This version uses word-overlap scoring to illustrate the retrieval concept.
    """

    def __init__(self) -> None:
        self._store: list[Memory] = []

    def remember(
        self,
        content: str,
        category: MemoryCategory,
        importance: float = 0.6,
        tags: Optional[list[str]] = None,
    ) -> bool:
        """
        Store a new memory.

        Before writing, the real system:
          - Checks for near-duplicate content (exact and embedding similarity)
          - Creates a backup of the current store
          - Normalizes first-person language to third-person

        Returns True if the memory was new and stored, False if duplicate.
        """
        content = content.strip()
        if not content:
            return False

        existing = {m.content.lower() for m in self._store}
        if content.lower() in existing:
            return False

        self._store.append(Memory(
            content=content,
            category=category,
            importance=importance,
            tags=tags or [],
        ))
        return True

    def recall(self, query: str, top_k: int = 5) -> list[Memory]:
        """
        Retrieve memories relevant to a query.

        The real system scores candidates using embedding cosine similarity,
        then re-ranks by importance. Memories below a relevance threshold
        are excluded regardless of importance score.

        This preview uses simple word overlap as a stand-in for semantic search.
        """
        query_words = set(query.lower().split())
        if not query_words:
            return []

        scored: list[tuple[Memory, float]] = []
        for mem in self._store:
            mem_words = set(mem.content.lower().split())
            overlap = len(query_words & mem_words) / max(len(query_words), 1)
            score = overlap * 0.7 + mem.importance * 0.3
            if score > 0.05:
                scored.append((mem, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [mem for mem, _ in scored[:top_k]]

    def forget(self, keyword: str) -> int:
        """
        Remove all memories whose content contains the keyword.

        The real system offers two deletion modes:
          - Keyword-based (exact substring match, fast and safe)
          - Similarity-based (semantic, high threshold, capped at 30 entries)

        Returns the number of entries removed.
        """
        keyword = keyword.lower().strip()
        before = len(self._store)
        self._store = [m for m in self._store if keyword not in m.content.lower()]
        return before - len(self._store)

    def stats(self) -> dict:
        """Summary statistics for the store."""
        if not self._store:
            return {"total": 0, "categories": {}, "avg_importance": 0.0}

        by_category: dict[str, int] = {}
        for m in self._store:
            key = m.category.value
            by_category[key] = by_category.get(key, 0) + 1

        avg_imp = sum(m.importance for m in self._store) / len(self._store)
        return {
            "total":          len(self._store),
            "categories":     by_category,
            "avg_importance": round(avg_imp, 2),
        }


# ── Example ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    store = MemoryPreview()

    # These would normally be extracted automatically after each conversation turn.
    # The auto-extractor runs in a background thread, using a lightweight LLM call
    # to identify personal facts worth storing.

    store.remember(
        "User prefers dark mode in all applications",
        MemoryCategory.PREFERENCE, importance=0.6, tags=["ui"],
    )
    store.remember(
        "User has an RTX 4060 GPU and 16 GB RAM",
        MemoryCategory.FACT, importance=1.0, tags=["hardware"],
    )
    store.remember(
        "User is building a local AI assistant called FRIDAY",
        MemoryCategory.CONTEXT, importance=0.9, tags=["project"],
    )
    store.remember(
        "User wants FRIDAY to eventually run fully offline",
        MemoryCategory.GOAL, importance=0.8,
    )
    store.remember(
        "User switched from cloud STT to Groq Whisper after accuracy issues",
        MemoryCategory.EVENT, importance=0.7, tags=["stt"],
    )

    print("=== Recall: hardware GPU performance ===")
    for mem in store.recall("hardware GPU performance", top_k=3):
        print(f"  [{mem.category.value}] (importance={mem.importance}) {mem.content}")

    print()
    print("=== Store Stats ===")
    for key, val in store.stats().items():
        print(f"  {key}: {val}")

    print()
    removed = store.forget("RTX")
    print(f"=== Forgot {removed} entry about RTX ===")
    print(f"  Store now has {store.stats()['total']} entries")
