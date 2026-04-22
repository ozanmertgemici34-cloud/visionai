from __future__ import annotations

import queue
import threading
from dataclasses import dataclass, field


@dataclass
class AssistantState:
    monitor_active: bool = False
    mic_active: bool = False
    is_processing: bool = False
    processing_lock: threading.Lock = field(default_factory=threading.Lock)
    audio_queue: queue.Queue = field(default_factory=queue.Queue)
    conversation_history: list = field(default_factory=list)
    stop_event: threading.Event = field(default_factory=threading.Event)
