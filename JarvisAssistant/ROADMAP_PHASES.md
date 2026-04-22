# Jarvis Personal Assistant - Faz Durumu

Bu doküman, Faz 1-6 hedeflerinin teknik olarak projeye nasıl işlendiğini özetler.

## Faz 1 — Mimari modülerleşme
- `core/` katmanı eklendi (`config`, `state`, `assistant`, `memory`, `actions`, `schemas`).
- UI kodu `app_ui.py` dosyasına ayrıldı.
- `main.py` sadece entrypoint olarak sadeleştirildi.

## Faz 2 — Kişisel asistan çekirdeği
- `MemoryStore` (SQLite) eklendi.
- Konuşma geçmişi kalıcı tutuluyor (`conversations` tablosu).
- Basit `action_items` çıkarımı ve kayıt altyapısı eklendi.

## Faz 3 — Doğruluk ve güven katmanı
- Model yanıtı için JSON şema zorlaması eklendi.
- `normalize_assistant_output` ile parse/fallback + confidence/confirmation akışı eklendi.

## Faz 4 — Kullanılabilirlik
- Düşük confidence durumunda kullanıcıdan onay isteyen metin üretimi eklendi.
- Durum mesajları ve mod geçişleri korunarak UI düzeni sadeleştirildi.

## Faz 5 — EXE paketleme
- `build/windows/jarvis.spec` eklendi.
- `build/windows/build_exe.ps1` ile tek komut build akışı eklendi.

## Faz 6 — Release hazırlığı
- Fazların çıktıları ve dağıtım adımları bu dokümanda listelendi.

## Not
- Dağıtım hedefi Windows için `dist/JarvisAssistant.exe`.
