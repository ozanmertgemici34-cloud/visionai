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

# ═══════════════════════════════════════════════
# 1. ORTAM VE API
# ═══════════════════════════════════════════════
load_dotenv()
GROQ_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_KEY:
    print("UYARI: GROQ_API_KEY bulunamadı!")
client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None

# Modeller
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
TEXT_MODEL = "llama-3.3-70b-versatile"  # Groq (Metin)
WHISPER_MODEL = "whisper-large-v3-turbo" # Groq (Ses Tanıma)

# ═══════════════════════════════════════════════
# 2. J.A.R.V.I.S KİŞİLİĞİ
# ═══════════════════════════════════════════════
JARVIS_SYSTEM_PROMPT = """Sen J.A.R.V.I.S — kullanıcının kişisel masaüstü asistanısın.

## KRİTİK KURAL: EKRANI OKU
Sana bir ekran görüntüsü verildiğinde, MUTLAKA önce ekrandaki durumu analiz et.
Ekranda tam olarak ne açık? Hangi pencere/uygulama görünüyor?
Hangi butonlar, menüler, sekmeler var?

## YANITLAMA
- Türkçe konuş. Selamlama YAPMA.
- Sadece ŞU ANKİ YAPILACAK TEK ADIMI söyle.
- Çok somut ol: "Ekranın sol üstündeki 'Steam' yazısına tıkla" gibi.
- Ekranda gördüğün buton/menü/yazı isimlerini AYNEN kullan.
- Yanıtın en fazla 2 cümle olsun.
- Kullanıcı 'tamam', 'yaptım', 'sonra', 'devam' derse bir sonraki adımı söyle.
- Kullanıcı sana ekranda ne gördüğünü sorarsa, gördüğünü kısaca anlat."""

# ═══════════════════════════════════════════════
# 3. DURUM YÖNETİMİ (OMI'dan İlham)
# ═══════════════════════════════════════════════
# OMI'nın mimarisi: Her modül bağımsız, merkezi state yönetimi var.
# Biz de aynı mantıkla: monitor ve mic tamamen ayrı kontrol ediliyor.

monitor_active = False   # Ekran İZLEME (proaktif tarama)
mic_active = False       # Mikrofon dinleme
is_processing = False    # İşlem kilidi (aynı anda 1 istek)
processing_lock = threading.Lock()
q = queue.Queue()
conversation_history = []

# ═══════════════════════════════════════════════
# 4. KOMPAKT ARAYÜZ
# ═══════════════════════════════════════════════
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("J.A.R.V.I.S")
app.geometry("220x120")
app.overrideredirect(True)
app.attributes("-topmost", True)
app.attributes("-alpha", 0.90)
app.configure(fg_color="#08080C")

app.update_idletasks()
app.geometry(f"+{app.winfo_screenwidth() - 240}+{app.winfo_screenheight() - 170}")

def start_move(event):
    app.x = event.x
    app.y = event.y

def do_move(event):
    x = app.winfo_x() + (event.x - app.x)
    y = app.winfo_y() + (event.y - app.y)
    app.geometry(f"+{x}+{y}")

title_frame = ctk.CTkFrame(app, corner_radius=0, fg_color="#101016", height=26)
title_frame.pack(fill="x", side="top")
title_frame.bind("<ButtonPress-1>", start_move)
title_frame.bind("<B1-Motion>", do_move)

title_label = ctk.CTkLabel(title_frame, text="⬡ J.A.R.V.I.S", font=("Consolas", 11, "bold"), text_color="#00E5FF")
title_label.pack(side="left", padx=8, pady=3)
title_label.bind("<ButtonPress-1>", start_move)
title_label.bind("<B1-Motion>", do_move)

def close_app():
    app.destroy()
    os._exit(0)

close_btn = ctk.CTkButton(title_frame, text="✕", width=24, height=20, font=("Consolas", 12, "bold"),
                           fg_color="transparent", hover_color="#FF4444", text_color="#666666",
                           command=close_app, corner_radius=4)
close_btn.pack(side="right", padx=4, pady=2)

separator = ctk.CTkFrame(app, height=1, fg_color="#00E5FF", corner_radius=0)
separator.pack(fill="x")

status_label = ctk.CTkLabel(app, text="💤 Bekleme", font=("Consolas", 10), text_color="#444444", height=18)
status_label.pack(pady=2)

def update_ui(text, color="white"):
    try:
        app.after(0, lambda: status_label.configure(text=text, text_color=color))
    except:
        pass

btn_frame = ctk.CTkFrame(app, fg_color="transparent")
btn_frame.pack(pady=2, fill="x", padx=8)

def toggle_monitor():
    global monitor_active
    monitor_active = sw_mon.get() == 1
    if monitor_active:
        update_ui("👁️ İzleniyor", "#00FFDD")
    elif not mic_active:
        update_ui("💤 Bekleme", "#444444")

def toggle_mic():
    global mic_active
    mic_active = sw_mic.get() == 1
    if mic_active:
        update_ui("🎙️ Dinleniyor", "#00FFDD")
    elif not monitor_active:
        update_ui("💤 Bekleme", "#444444")

sw_mon = ctk.CTkSwitch(btn_frame, text="Ekran", font=("Consolas", 10), width=40,
                        command=toggle_monitor, progress_color="#00E5FF",
                        button_color="#00E5FF", button_hover_color="#00B8D4")
sw_mon.pack(side="left", padx=4)

sw_mic = ctk.CTkSwitch(btn_frame, text="Mikrofon", font=("Consolas", 10), width=40,
                        command=toggle_mic, progress_color="#00E5FF",
                        button_color="#00E5FF", button_hover_color="#00B8D4")
sw_mic.pack(side="right", padx=4)

# ═══════════════════════════════════════════════
# 5. TÜRKÇE SES (EmelNeural)
# ═══════════════════════════════════════════════
TTS_VOICE = "tr-TR-EmelNeural"
TTS_RATE = "-8%"
TTS_PITCH = "+0Hz"

tts_lock = threading.Lock()

def speak_text(text):
    if not text or len(text.strip()) < 2:
        return
    print(f"J.A.R.V.I.S: {text}\n")
    update_ui("🤖 Konuşuyor", "#00FFAD")
    
    with tts_lock:
        temp_file = f"temp_speech_{uuid.uuid4().hex[:6]}.mp3"
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            communicate = edge_tts.Communicate(text, TTS_VOICE, rate=TTS_RATE, pitch=TTS_PITCH)
            loop.run_until_complete(communicate.save(temp_file))
            loop.close()
            playsound(temp_file)
            try:
                os.remove(temp_file)
            except:
                pass
        except Exception as e:
            print("TTS Hatası:", e)

def _restore_status():
    if mic_active:
        update_ui("🎙️ Dinleniyor", "#00FFDD")
    elif monitor_active:
        update_ui("👁️ İzleniyor", "#00FFDD")
    else:
        update_ui("💤 Bekleme", "#444444")

# ═══════════════════════════════════════════════
# 6. GROQ API FONKSİYONLARI
# ═══════════════════════════════════════════════
def capture_screen_base64():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        img = img.resize((1280, 720), Image.BILINEAR)
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=80)
        return base64.standard_b64encode(buffer.getvalue()).decode("utf-8")

def ask_with_screen(user_prompt, img_b64):
    """Ekran görüntüsü + metin ile soru sor (Groq Vision modeli)"""
    global conversation_history
    
    # Her sorguda detaylı düşünmesini sağlayan zorlayıcı prompt
    full_prompt = f"""Kullanıcı sana şunu söylüyor: \"{user_prompt}\"

YANITLAMA KURALLARI:
1. Eğer soru veya istek ekranla YAKINDAN İLGİLİ DEĞİLSE (örn: "Nasılsın?", "Hava nasıl?"): 
   Sadece doğal, kısa bir asistan gibi yanıt ver. Ekrandan hiç bahsetme.
2. Eğer soru ekranla alakalıysa (yardım istiyor, bir menüyü soruyor vb.):
   - MUTLAKA önce [ANALİZ] ve [/ANALİZ] etiketleri arasına ekranda tam olarak neler açık, şuan hangi sekmeler ve butonlar gözüküyor yaz (Bu senin iç düşüncen).
   - Sonra bu etiketlerin DIŞINA çıkıp, kullanıcıya SADECE yapması gereken sıradaki TEK adımı (Nereye tıklayacağını) çok net ve kısa söyle.

Örnek Durum (Ekran odaklıysa):
[ANALİZ] Windows masaüstü açık, sol altta Başlat menüsü var. [/ANALİZ]
Sol alttaki Başlat ikonuna tıklayın."""

    messages = [{"role": "system", "content": JARVIS_SYSTEM_PROMPT}]
    messages += conversation_history[-4:]
    messages.append({
        "role": "user",
        "content": [
            {"type": "text", "text": full_prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
        ]
    })
    
    if client is None:
        answer = "Groq API anahtarı ayarlanmadığı için görüntü analizi yapılamıyor."
    else:
        try:
            response = client.chat.completions.create(model=VISION_MODEL, messages=messages, max_tokens=250)
            answer = response.choices[0].message.content.strip()
        except Exception as e:
            print("Groq Vision Hatası:", e)
            answer = "Görüntü analizinde sorun çıktı."

    conversation_history.append({"role": "user", "content": user_prompt})
    conversation_history.append({"role": "assistant", "content": answer})
    if len(conversation_history) > 10:
        conversation_history = conversation_history[-6:]
    return answer

def ask_text_only(user_prompt):
    """Sadece metin ile soru sor - EKRAN KULLANMAZ (Text model)"""
    global conversation_history
    messages = [{"role": "system", "content": JARVIS_SYSTEM_PROMPT}]
    messages += conversation_history[-4:]
    messages.append({"role": "user", "content": user_prompt})
    if client is None:
        answer = "Groq API anahtarı ayarlanmadığı için metin yanıtı üretilemiyor."
    else:
        try:
            response = client.chat.completions.create(model=TEXT_MODEL, messages=messages, max_tokens=300)
            answer = response.choices[0].message.content.strip()
        except Exception as e:
            print("Groq Text Hatası:", e)
            answer = "Metin yanıtı alınırken bir sorun oluştu."
    conversation_history.append({"role": "user", "content": user_prompt})
    conversation_history.append({"role": "assistant", "content": answer})
    if len(conversation_history) > 10:
        conversation_history = conversation_history[-6:]
    return answer

def transcribe_audio(wav_path):
    if client is None:
        raise RuntimeError("Groq API anahtarı ayarlanmadığı için ses çözümlenemiyor.")
    with open(wav_path, "rb") as f:
        transcription = client.audio.transcriptions.create(
            file=("audio.wav", f.read()),
            model=WHISPER_MODEL,
            language="tr",
            response_format="text"
        )
    return transcription.strip()

# ═══════════════════════════════════════════════
# 7. EKRAN İZLEME (Proaktif - Sadece toggle açıkken)
# ═══════════════════════════════════════════════
def monitor_loop():
    global is_processing
    while True:
        try:
            if monitor_active and processing_lock.acquire(blocking=False):
                is_processing = True
                try:
                    img_b64 = capture_screen_base64()
                    prompt = "Ekrana bak. Bariz HATA (exception, error, crash) varsa 1 cümleyle Türkçe uyar. Hata yoksa sadece 'ALL_GOOD' yaz."
                    answer = ask_with_screen(prompt, img_b64)
                    if "ALL_GOOD" not in answer.upper() and len(answer) > 3:
                        speak_text(answer)
                except Exception as e:
                    print(f"Monitor Hatası: {e}")
                finally:
                    is_processing = False
                    processing_lock.release()
        except Exception as e:
            print(f"Monitor Loop Crash: {e}")
            is_processing = False
        time.sleep(30)

# ═══════════════════════════════════════════════
# 8. SÜREKLİ MİKROFON & VAD (OMI'dan İlham)
# ═══════════════════════════════════════════════
# OMI'nın VAD sistemi: Ses seviyesi eşiği + zamanlayıcı ile konuşma algılama.
# Ek: Ekran toggle'ı kapalıysa EKRAN GÖRMESİN. Sadece sesle cevaplasın.

def audio_callback(indata, frames, time_info, status):
    if mic_active:
        q.put(indata.copy())

def continuous_mic_loop():
    global is_processing
    fs = 16000
    voice_buffer = []
    is_recording = False
    silence_count = 0
    THRESHOLD = 500

    try:
        with sd.InputStream(samplerate=fs, channels=1, dtype='int16', blocksize=4000, callback=audio_callback):
            print("Mikrofon stream'i başarıyla açıldı.")
            while True:
                try:
                    if not mic_active:
                        time.sleep(0.3)
                        while not q.empty():
                            try: q.get_nowait()
                            except: break
                        # Kayıt durumunu sıfırla
                        if is_recording:
                            is_recording = False
                            voice_buffer = []
                            silence_count = 0
                        continue
                    
                    try:
                        data = q.get(timeout=0.15)
                    except queue.Empty:
                        continue
                    
                    amp = np.max(np.abs(data))
                    
                    if amp > THRESHOLD:
                        if not is_recording:
                            is_recording = True
                            update_ui("🎙️ Dinliyor...", "#FFA500")
                        voice_buffer.append(data)
                        silence_count = 0
                    else:
                        if is_recording:
                            voice_buffer.append(data)
                            silence_count += 1
                            
                            # Gecikmeyi azaltmak için sessizlik eşiğini 8'den 5'e düşürdük (Yaklaşık 0.75 saniye)
                            if silence_count > 5:
                                update_ui("⚙️ Düşünüyor", "#FFD700")
                                is_recording = False
                                silence_count = 0
                                final_audio = np.concatenate(voice_buffer)
                                voice_buffer = []
                                
                                # Çok kısa ses = gürültü, atla
                                if len(final_audio) < fs:
                                    _restore_status()
                                    continue
                                
                                # Başka işlem çalışıyorsa bekle
                                if is_processing:
                                    _restore_status()
                                    continue
                                
                                if not processing_lock.acquire(blocking=False):
                                    _restore_status()
                                    continue
                                is_processing = True
                                try:
                                    write("temp_voice.wav", fs, final_audio)
                                    user_text = transcribe_audio("temp_voice.wav")
                                    print(f"Kullanıcı: {user_text}")
                                    
                                    if not user_text or len(user_text) < 2:
                                        is_processing = False
                                        _restore_status()
                                        continue
                                    
                                    # ═══ KRİTİK DÜZELTME ═══
                                    # Ekran toggle'ı KAPALI → ekranı GÖRMEZ, sadece metinle cevaplar
                                    # Ekran toggle'ı AÇIK → ekranı görür ve bağlam olarak kullanır
                                    if monitor_active:
                                        img_b64 = capture_screen_base64()
                                        answer = ask_with_screen(user_text, img_b64)
                                    else:
                                        answer = ask_text_only(user_text)
                                    
                                    # Markdown temizle
                                    # [ANALİZ] ile [/ANALİZ] arasındaki tüm düşünceleri TTS okumasın diye siliyoruz
                                    clean = re.sub(r'\[ANALİZ\].*?\[/ANALİZ\]', '', answer, flags=re.DOTALL)
                                    clean = clean.replace("*", "").replace("#", "").replace("`", "").strip()
                                    if clean:
                                        speak_text(clean)
                                    
                                    # Çok Önemli: Asistan konuşurken kendi sesini duymuş olabilir, bu yankıyı çöpe at
                                    while not q.empty():
                                        try: q.get_nowait()
                                        except: break
                                    
                                except Exception as e:
                                    err = str(e)
                                    print("Groq Hatası:", err)
                                    if "429" in err:
                                        update_ui("⏳ Kota (30sn)", "orange")
                                        time.sleep(30)
                                    else:
                                        update_ui("⚠️ Hata", "red")
                                        print(traceback.format_exc())
                                        time.sleep(3)
                                finally:
                                    is_processing = False
                                    processing_lock.release()
                                    _restore_status()
                except Exception as e:
                    print(f"Mic iç döngü hatası: {e}")
                    is_recording = False
                    voice_buffer = []
                    silence_count = 0
                    is_processing = False
                    time.sleep(1)
    except Exception as e:
        print(f"Mikrofon stream HATASI: {e}")
        print(traceback.format_exc())


if __name__ == "__main__":
    print("═══════════════════════════════════════")
    print("  J.A.R.V.I.S v3.2 | Groq Ultimate Vision")
    print("  Ses : EmelNeural (Türkçe)")
    print("  AI  : Llama 4 Scout Vision + Whisper")
    print("═══════════════════════════════════════")
    print("  Ekran ON  + Mikrofon ON = Tam mod")
    print("  Ekran OFF + Mikrofon ON = Sadece ses")
    print("═══════════════════════════════════════")
    threading.Thread(target=monitor_loop, daemon=True).start()
    threading.Thread(target=continuous_mic_loop, daemon=True).start()
    app.mainloop()
