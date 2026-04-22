import google.generativeai as genai
import os, time
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

print("Kota testi başlıyor... 15 saniye bekleniyor...")
time.sleep(15)

try:
    response = model.generate_content("Merhaba, sadece 'Çalışıyorum' de.")
    print("BAŞARILI:", response.text.strip())
except Exception as e:
    print("HATA:", e)
