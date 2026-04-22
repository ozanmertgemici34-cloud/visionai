from __future__ import annotations

import asyncio
import base64
import io
import re
import threading
import time
import traceback
import uuid

import edge_tts
import mss
import numpy as np
import sounddevice as sd
from groq import Groq
from PIL import Image
from playsound3 import playsound
from scipy.io.wavfile import write

from .actions import extract_action_items
from .config import AppConfig
from .memory import MemoryStore
from .schemas import normalize_assistant_output
from .state import AssistantState


JARVIS_SYSTEM_PROMPT = """Sen J.A.R.V.I.S — kullanıcının kişisel masaüstü asistanısın.

YANITI SADECE JSON FORMATINDA VER:
{
  "next_step": "kullanıcının şu an yapacağı tek net adım",
  "confidence": 0.0-1.0,
  "needs_confirmation": true/false
}

KURALLAR:
- Türkçe yanıt ver.
- next_step en fazla 2 cümle olsun.
- Ekran odaklı sorularda buton/yazı isimlerini aynen kullan.
- Emin değilsen needs_confirmation=true dön.
"""


class JarvisAssistant:
    def __init__(self, config: AppConfig, state: AssistantState, memory: MemoryStore, update_ui):
        self.config = config
        self.state = state
        self.memory = memory
        self.update_ui = update_ui
        self.tts_lock = threading.Lock()
        self.client = Groq(api_key=config.runtime.groq_api_key) if config.runtime.groq_api_key else None

    def restore_status(self) -> None:
        if self.state.mic_active:
            self.update_ui("🎙️ Dinleniyor", "#00FFDD")
        elif self.state.monitor_active:
            self.update_ui("👁️ İzleniyor", "#00FFDD")
        else:
            self.update_ui("💤 Bekleme", "#444444")

    def speak_text(self, text: str) -> None:
        if not text or len(text.strip()) < 2:
            return
        self.update_ui("🤖 Konuşuyor", "#00FFAD")

        with self.tts_lock:
            temp_file = f"temp_speech_{uuid.uuid4().hex[:6]}.mp3"
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                communicate = edge_tts.Communicate(
                    text,
                    self.config.runtime.tts_voice,
                    rate=self.config.runtime.tts_rate,
                    pitch=self.config.runtime.tts_pitch,
                )
                loop.run_until_complete(communicate.save(temp_file))
                loop.close()
                playsound(temp_file)
            except Exception as e:
                print("TTS Hatası:", e)
            finally:
                try:
                    import os

                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                except Exception:
                    pass

    def capture_screen_base64(self) -> str:
        with mss.mss() as sct:
            monitor_index = 1 if len(sct.monitors) > 1 else 0
            monitor = sct.monitors[monitor_index]
            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            img = img.resize((1280, 720), Image.BILINEAR)
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=80)
            return base64.standard_b64encode(buffer.getvalue()).decode("utf-8")

    def _compose_messages(self, user_prompt: str, img_b64: str | None = None) -> list[dict]:
        messages = [{"role": "system", "content": JARVIS_SYSTEM_PROMPT}]
        messages.extend(self.memory.recent_conversations(limit=8))
        if img_b64:
            messages.append(
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}},
                    ],
                }
            )
        else:
            messages.append({"role": "user", "content": user_prompt})
        return messages

    def _llm_chat(self, model: str, messages: list[dict]) -> str:
        if self.client is None:
            return '{"next_step":"API anahtarı eksik. GROQ_API_KEY ayarla.","confidence":0.1,"needs_confirmation":true}'
        response = self.client.chat.completions.create(model=model, messages=messages, max_tokens=300)
        return (response.choices[0].message.content or "").strip()

    def ask_with_screen(self, user_prompt: str, img_b64: str) -> str:
        try:
            raw = self._llm_chat(
                model=self.config.models.vision_model,
                messages=self._compose_messages(user_prompt=user_prompt, img_b64=img_b64),
            )
        except Exception as e:
            print("Groq Vision Hatası:", e)
            raw = '{"next_step":"Görüntü analizi sırasında hata oluştu.","confidence":0.2,"needs_confirmation":true}'

        parsed = normalize_assistant_output(raw)
        answer = parsed.next_step
        if parsed.needs_confirmation and parsed.confidence < 0.65:
            answer = f"{answer} (Eminlik: %{int(parsed.confidence * 100)}. Onaylıyor musun?)"

        self.memory.add_conversation("user", user_prompt)
        self.memory.add_conversation("assistant", answer)
        self._store_actions(answer)
        return answer

    def ask_text_only(self, user_prompt: str) -> str:
        try:
            raw = self._llm_chat(
                model=self.config.models.text_model,
                messages=self._compose_messages(user_prompt=user_prompt),
            )
        except Exception as e:
            print("Groq Text Hatası:", e)
            raw = '{"next_step":"Yanıt alınırken bir sorun oluştu.","confidence":0.2,"needs_confirmation":true}'

        parsed = normalize_assistant_output(raw)
        answer = parsed.next_step
        if parsed.needs_confirmation and parsed.confidence < 0.65:
            answer = f"{answer} (Eminlik: %{int(parsed.confidence * 100)}. Onaylıyor musun?)"

        self.memory.add_conversation("user", user_prompt)
        self.memory.add_conversation("assistant", answer)
        self._store_actions(answer)
        return answer

    def transcribe_audio(self, wav_path: str) -> str:
        if self.client is None:
            raise RuntimeError("Groq API anahtarı ayarlanmadığı için ses çözümlenemiyor.")
        with open(wav_path, "rb") as f:
            transcription = self.client.audio.transcriptions.create(
                file=("audio.wav", f.read()),
                model=self.config.models.whisper_model,
                language="tr",
                response_format="text",
            )
        return transcription.strip()

    def _store_actions(self, answer_text: str) -> None:
        actions = extract_action_items(answer_text)
        count = self.memory.add_action_items(actions)
        if count:
            print(f"{count} aksiyon kaydedildi.")

    def monitor_loop(self) -> None:
        while not self.state.stop_event.is_set():
            try:
                if self.state.monitor_active and self.state.processing_lock.acquire(blocking=False):
                    self.state.is_processing = True
                    try:
                        img_b64 = self.capture_screen_base64()
                        prompt = "Ekrana bak. Bariz hata varsa tek adım düzeltme önerisi ver. Sorun yoksa JSON içinde next_step='ALL_GOOD' dön."
                        answer = self.ask_with_screen(prompt, img_b64)
                        if "ALL_GOOD" not in answer.upper() and len(answer) > 3:
                            self.speak_text(answer)
                    except Exception as e:
                        print(f"Monitor Hatası: {e}")
                    finally:
                        self.state.is_processing = False
                        self.state.processing_lock.release()
            except Exception as e:
                print(f"Monitor Loop Crash: {e}")
                self.state.is_processing = False
            time.sleep(self.config.runtime.monitor_interval_sec)

    def audio_callback(self, indata, frames, time_info, status):
        if self.state.mic_active:
            self.state.audio_queue.put(indata.copy())

    def continuous_mic_loop(self) -> None:
        fs = 16000
        voice_buffer = []
        is_recording = False
        silence_count = 0
        threshold = 500

        try:
            with sd.InputStream(
                samplerate=fs,
                channels=1,
                dtype="int16",
                blocksize=4000,
                callback=self.audio_callback,
            ):
                while not self.state.stop_event.is_set():
                    try:
                        if not self.state.mic_active:
                            time.sleep(0.3)
                            while not self.state.audio_queue.empty():
                                try:
                                    self.state.audio_queue.get_nowait()
                                except Exception:
                                    break
                            if is_recording:
                                is_recording = False
                                voice_buffer = []
                                silence_count = 0
                            continue

                        try:
                            data = self.state.audio_queue.get(timeout=0.15)
                        except Exception:
                            continue

                        amp = np.max(np.abs(data))
                        if amp > threshold:
                            if not is_recording:
                                is_recording = True
                                self.update_ui("🎙️ Dinliyor...", "#FFA500")
                            voice_buffer.append(data)
                            silence_count = 0
                        elif is_recording:
                            voice_buffer.append(data)
                            silence_count += 1
                            if silence_count > 5:
                                self.update_ui("⚙️ Düşünüyor", "#FFD700")
                                is_recording = False
                                silence_count = 0
                                final_audio = np.concatenate(voice_buffer)
                                voice_buffer = []

                                if len(final_audio) < fs:
                                    self.restore_status()
                                    continue
                                if self.state.is_processing:
                                    self.restore_status()
                                    continue
                                if not self.state.processing_lock.acquire(blocking=False):
                                    self.restore_status()
                                    continue

                                self.state.is_processing = True
                                try:
                                    write("temp_voice.wav", fs, final_audio)
                                    user_text = self.transcribe_audio("temp_voice.wav")
                                    if not user_text or len(user_text) < 2:
                                        self.restore_status()
                                        continue

                                    if self.state.monitor_active:
                                        img_b64 = self.capture_screen_base64()
                                        answer = self.ask_with_screen(user_text, img_b64)
                                    else:
                                        answer = self.ask_text_only(user_text)

                                    clean = re.sub(r"\[ANALİZ\].*?\[/ANALİZ\]", "", answer, flags=re.DOTALL)
                                    clean = clean.replace("*", "").replace("#", "").replace("`", "").strip()
                                    if clean:
                                        self.speak_text(clean)

                                    while not self.state.audio_queue.empty():
                                        try:
                                            self.state.audio_queue.get_nowait()
                                        except Exception:
                                            break
                                except Exception as e:
                                    err = str(e)
                                    print("Groq Hatası:", err)
                                    if "429" in err:
                                        self.update_ui("⏳ Kota (30sn)", "orange")
                                        time.sleep(30)
                                    else:
                                        self.update_ui("⚠️ Hata", "red")
                                        print(traceback.format_exc())
                                        time.sleep(2)
                                finally:
                                    self.state.is_processing = False
                                    self.state.processing_lock.release()
                                    self.restore_status()
                    except Exception as e:
                        print(f"Mic iç döngü hatası: {e}")
                        is_recording = False
                        voice_buffer = []
                        silence_count = 0
                        self.state.is_processing = False
                        time.sleep(1)
        except Exception as e:
            print(f"Mikrofon stream HATASI: {e}")
            print(traceback.format_exc())
