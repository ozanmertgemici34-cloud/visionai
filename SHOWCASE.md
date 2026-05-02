# F.R.I.D.A.Y — Kişisel Yapay Zeka Asistan Sistemi

> *"Female Replacement Intelligent Digital Assistant Youth"*
> Iron Man'in FRIDAY'inden ilham alınarak sıfırdan inşa edildi.

---

## Ne Bu?

FRIDAY, bir bilgisayar üzerinde gerçek anlamda çalışan kişisel bir yapay zeka asistanıdır. Siri veya Google Assistant'tan farkı şudur: **FRIDAY bilgisayarınızı gerçekten kontrol eder.** Uygulama açar, dosya yönetir, web araştırması yapar, kod çalıştırır, sizi hatırlar ve Türkçe konuşur.

Sesli veya yazılı komutla çalışır. Her komut için doğru yapay zeka modelini seçer — basit sorular için ücretsiz yerel model, araştırma ve eylem gerektiren işler için bulut API.

---

## Mimari — Nasıl Çalışır?

```
Kullanıcı (ses / yazı)
        ↓
   STT (Whisper)
        ↓
   Router — hangi model?
   ├── Basit soru    → Ollama (yerel, ücretsiz, ~1s)
   └── Araştırma     → OpenAI GPT-4.1-mini (streaming, araç çağırma)
                              ↓
                       82 Araç mevcut
                       (web, dosya, desktop, kod, hafıza...)
                              ↓
                         TTS (edge-tts)
                              ↓
                       Ses çıktısı + JARVIS HUD
```

**Akıllı Yönlendirme:** Sistem her sorguyu analiz eder.
- *"Nasılsın?"* → Yerel model. API masrafı yok, 0.8 saniye.
- *"Elon Musk kimdir?"* → OpenAI + web araması + Wikipedia okuma.
- *"Chrome'u aç, YouTube'u çal"* → OpenAI + desktop araçları.

---

## Yetenekler

### Desktop Kontrolü
Bilgisayarı komutla yönet.

| Komut Örneği | Ne Yapar |
|---|---|
| "Spotify'ı aç" | Uygulamayı başlatır |
| "Chrome'u küçült" | Pencereyi minimize eder |
| "Sesi %60'a ayarla" | Sistem sesini ayarlar |
| "Ekranda ne var?" | Ekran görüntüsü alır, AI ile analiz eder |
| "Şu butona tıkla" | Mouse'u doğru konuma götürür, tıklar |
| "Notepad'i aç, şunu yaz, kaydet" | Çok adımlı otomasyon, tek komut |
| "Tüm pencereleri küçült" | Masaüstünü gösterir |

### Web Araştırması — 3 Katmanlı
Soru tipine göre doğru aracı seçer:

| Araç | Ne Zaman | Derinlik |
|---|---|---|
| `search_web` | Hızlı bilgi, fiyat, kur | Özet (snippet) |
| `read_webpage` | Belirli URL okuma | Tam sayfa (4000 karakter) |
| `search_and_read` | "X kimdir / hakkında anlat" | Arama + makale okuma |

```
"Atatürk kimdir?" → search_and_read → Wikipedia makalesini okur → özetler
"Dolar kaç?" → search_web → anlık kur bilgisi
"Bu sayfayı oku: ..." → read_webpage → tam içerik
```

### Gerçek Zamanlı Bilgi
- Türkiye haberleri (Hürriyet, CNN Türk, vb.)
- Dünya haberleri
- Hava durumu (herhangi bir şehir)
- Borsa, döviz, kripto fiyatları

### Dosya ve Sistem Yönetimi
```
"Masaüstünde dosya ara: rapor"
"Bu klasörü listele"
"Dosyayı taşı / kopyala / sil"
"Disk alanı ne kadar kaldı?"
"Çalışan süreçleri göster"
```

### Python Kodu Çalıştırma
FRIDAY kod yazar ve anında çalıştırır:

```
"1'den 100'e kadar sayıların toplamını hesapla"
  → Python kodu yazar → çalıştırır → "Sonuç: 5050"

"Masaüstündeki dosyaları listele"
  → os.listdir() kodu → çalıştırır → sonucu söyler

"pandas kur ve bir CSV analizi yap"
  → pip install → kod yazar → çalıştırır
```

### Clipboard (Pano) Entegrasyonu
Kopyala → Söyle → Sonuç direkt panona:

```
[İngilizce makale kopyala]
"Bunu Türkçeye çevir"
→ Metni panodan okur → GPT ile çevirir → Çeviriyi panona yazar → Ctrl+V yapabilirsin

[E-posta taslağı kopyala]
"Bunu düzelt ve profesyonelleştir"
→ Okur → Düzeltir → Panoya atar

[Hata mesajı kopyala]
"Bunu açıkla"
→ Hata mesajını analiz eder → Türkçe açıklar
```

### Hafıza Sistemi — Sizi Hatırlar

**Otomatik:** Her konuşmadan öğrenilen bilgiler arka planda kaydedilir. Hiçbir komut gerekmez.

```
Bugün: "Ben İstanbul'da yaşıyorum ve Python geliştiricisiyim."
        → [FACT] Ozan İstanbul'da yaşıyor.
        → [FACT] Ozan Python geliştiricisidir.

Yarın: "Bana proje öner"
        → FRIDAY İstanbul ve Python bilgisini kullanarak öneri yapar
```

**Manuel:** `"Bunu hatırla: ..."` komutuyla da kaydedilir.

**170+ hafıza kaydı** — tercihler, hedefler, olaylar, bağlamlar, gerçekler.

**Semantik arama:** "Python bilen biri" diye sorsan → "Ozan Python geliştiricisidir" kaydını bulur.

### Hatırlatıcı ve Not Sistemi
```
"30 dakika sonra toplantıyı hatırlat"
"Not al: yarın X ile görüşeceğim"
"Notlarımı oku"
```

### Steam & Oyun Yönetimi
```
"Steam'i aç"
"Yüklü oyunları listele"
"CS2'yi başlat"
"Half Life 3 fiyatı nedir?" → Steam mağaza araması
```

### YouTube Kontrolü
```
"YouTube'da lo-fi müzik çal"
"YouTube'da Python tutorial ara"
```

---

## Teknik Altyapı

| Bileşen | Teknoloji |
|---|---|
| **UI** | Qt / QML — JARVIS HUD tarzı arayüz |
| **Birincil LLM** | OpenAI GPT-4.1-mini (streaming, araç çağırma) |
| **Yerel LLM** | Ollama — qwen2.5:7b (ücretsiz, offline) |
| **Yedek LLM** | Google Gemini 2.5 Flash |
| **Vision** | Gemini Vision — ekran analizi |
| **STT** | faster-whisper / Google STT |
| **TTS** | edge-tts (tr-TR-AhmetNeural) + pyttsx3 fallback |
| **Hafıza** | TF-IDF + semantik embedding (OpenAI) |
| **Desktop otomasyon** | pyautogui + Win32 API |
| **Kod çalıştırma** | Python subprocess (sandbox, 30s timeout) |
| **Web araştırma** | httpx + BeautifulSoup4 + Wikipedia API |
| **Platform** | Windows 11, Python 3.14 |

---

## Araçlar — 82 Adet

```
Desktop     : open_application, close_application, minimize_window,
              maximize_window, focus_window, minimize_all_windows,
              list_windows, set_window_size

Ekran       : look_at_screen, find_and_click, click_at, right_click_at,
              type_text, press_key, scroll

Web         : search_web, read_webpage, search_and_read,
              get_turkish_news, get_world_news, get_weather,
              youtube_search, youtube_play, google_search

Ses         : set_volume, volume_up, volume_down, mute_volume,
              media_play_pause, media_next, media_prev

Dosya       : find_file, list_folder, read_file, write_text_file,
              rename_file, move_file, copy_file, delete_file

Sistem      : get_system_stats, list_processes, kill_process,
              run_powershell, lock_screen, sleep_mode,
              get_clipboard, set_clipboard, get_disk_space_info

Kod         : run_python_code, run_python_file, install_package

Hafıza      : remember_this, recall_memory, forget_memory, memory_stats

Notlar      : take_note, read_notes, clear_notes

Hatırlatıcı: set_reminder, list_reminders, cancel_reminder

Tarayıcı    : youtube_search, youtube_play, google_search, open_website

Steam       : steam_open_library, steam_list_installed,
              steam_launch_game, steam_search_game, steam_install_game
```

---

## Konuşma Örnekleri

```
Sen: "Bugün hava nasıl?"
FRIDAY: "İstanbul'da 18°C, parçalı bulutlu. Şemsiye almana gerek yok."

Sen: "Einstein kimdir?"
FRIDAY: → Wikipedia'yı okur
         "Albert Einstein, 1879-1955 yılları arasında yaşamış teorik fizikçi.
          Görelilik teorisiyle tanınır, 1921'de Nobel Fizik Ödülü aldı..."

Sen: "Şu kopyaladığım e-postayı düzelt"
FRIDAY: → Panoyu okur → GPT ile düzeltir → Panoya yazar
         "Düzelttim ve panoya kopyaladım, yapıştırabilirsin."

Sen: "Masaüstündeki .py dosyalarını listele"
FRIDAY: → Python kodu yazar ve çalıştırır
         "Masaüstünde 7 Python dosyası var: friday_test.py, ..."

Sen: "30 dakika sonra kahve hatırlat"
FRIDAY: "Tamam, 30 dakika sonra hatırlatacağım."
         [30 dakika sonra]
         "Ozan, kahve vakti!"

Sen: "Steam'de yüklü oyunları göster, sonra CS2'yi başlat"
FRIDAY: → steam_list_installed → liste gösterir
         → steam_launch_game("CS2") → oyun başlar
         "CS2 başlatıldı."
```

---

## Mimari Kararlar

**Neden iki LLM?**
GPT-4.1-mini pahalı. "Nasılsın?" gibi basit sorular için API çağrısı yapmak saçma. Router her sorguyu analiz eder: kelime sayısı, web gerektiriyor mu, araç gerekiyor mu? Basit sorular yerel modelde kalır, maliyeti ~%70 düşürür.

**Neden streaming?**
TTS (metin-ses) cümle gelmeden başlayamaz. Streaming ile ilk cümle gelir gelmez TTS başlar — kullanıcı 400ms'de cevabı duymaya başlar, model yanıtı tamamlamayı beklemez.

**Neden otomatik hafıza?**
"Bunu hatırla" demek zorunda kalmamalısın. Her konuşmadan öğrenilen şeyler arka planda kaydedilir. Bir sonraki konuşmada FRIDAY bağlamı zaten bilir.

**Neden Win32 API?**
pyautogui pencere yönetimi güvenilir değil. Win32 API ile pencere minimize/maximize/close işlemleri milisaniyede tamamlanır, `time.sleep()` gerektirmez.

---

## Çalıştırma

```bash
# Gereksinimler
pip install -r requirements.txt

# Ollama (yerel model) — opsiyonel
ollama pull qwen2.5:7b

# Ortam değişkenleri
cp .env.example .env
# OPENAI_API_KEY, GEMINI_API_KEY gir

# Başlat
python app_qt.py
```

---

## Geliştirici

**Ozan** — JarvisBrain v2 projesi, 2025-2026
Windows 11 · Python 3.14 · GPT-4.1-mini · Ollama · edge-tts

---

*"Araç gerektiren bir işi araç çağırmadan yapmam. Yapabilirim demek yerine yaparım."*
— F.R.I.D.A.Y.
