# TÜM <<<<<<< ======= >>>>>>> SATIRLARI SİLİNDİ

import os
import time
import threading
import asyncio
import edge_tts
import mss
from PIL import Image
from groq import Groq
from dotenv import load_dotenv
from playsound3 import playsound
import customtkinter as ctk
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import queue
import base64
import io
import traceback
import uuid
import re

load_dotenv()
GROQ_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_KEY:
    print("UYARI: GROQ_API_KEY bulunamadı!")
client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None

VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
TEXT_MODEL = "llama-3.3-70b-versatile"
WHISPER_MODEL = "whisper-large-v3-turbo"

monitor_active = False
mic_active = False
is_processing = False
processing_lock = threading.Lock()
q = queue.Queue()
conversation_history = []

ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("J.A.R.V.I.S")
app.geometry("220x120")

# (UI kodların aynen devam ediyor...)

# ⬇️ EN ÖNEMLİ DÜZELTME
# threadleri başlat

threading.Thread(target=monitor_loop, daemon=True).start()
threading.Thread(target=continuous_mic_loop, daemon=True).start()

# ⬇️ APP BAŞLAT
app.mainloop()