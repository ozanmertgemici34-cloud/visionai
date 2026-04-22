from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass(frozen=True)
class ModelConfig:
    vision_model: str = "meta-llama/llama-4-scout-17b-16e-instruct"
    text_model: str = "llama-3.3-70b-versatile"
    whisper_model: str = "whisper-large-v3-turbo"


@dataclass(frozen=True)
class RuntimeConfig:
    groq_api_key: str | None
    tts_voice: str = "tr-TR-EmelNeural"
    tts_rate: str = "-8%"
    tts_pitch: str = "+0Hz"
    monitor_interval_sec: int = 30


@dataclass(frozen=True)
class AppConfig:
    runtime: RuntimeConfig
    models: ModelConfig



def load_config() -> AppConfig:
    load_dotenv()
    runtime = RuntimeConfig(groq_api_key=os.getenv("GROQ_API_KEY"))
    return AppConfig(runtime=runtime, models=ModelConfig())
