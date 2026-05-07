# Katkıda Bulunma Rehberi

Teşekkürler! FRIDAY'i daha iyi hale getirmek için katkıda bulunmak istemen harika.

---

## Nasıl Katkıda Bulunulur

### 1. Issue Açma

Yeni bir özellik, hata raporu veya soru için GitHub Issues kullanın:

- **Bug report:** Lütfen reproducible adımlar, beklenen davranış ve gerçek davranışı belirtin
- **Feature request:** Ne işe yarayacağını ve neden gerekli olduğunu açıklayın
- **Soru:** Issue yerine tartışma bölümünü kullanabilirsiniz

### 2. Kod Değişikliği Yapma

```bash
# 1. Fork yapın (GitHub arayüzünden)

# 2. Projeyi klonlayın
git clone https://github.com/YOUR_USERNAME/JarvisBrain_v2.git
cd JarvisBrain_v2

# 3. Feature branch oluşturun
git checkout -b feature/yeni-ozellik
# veya
git checkout -b fix/hata-duzeltmesi

# 4. Değişiklikleri yapın

# 5. Test edin
python -m unittest tests.test_router
python test_system_full.py

# 6. Commit yapın
git add .
git commit -m "feat: kısa açıklama"

# 7. Push edin
git push origin feature/yeni-ozellik
```

### 3. Pull Request Açma

1. GitHub'da "Compare & pull request" seçeneğine tıklayın
2. Açıklama yazın:
   - Ne değişti?
   - Neden değişti?
   - Nasıl test edildi?
3. Reviewer atanmasını bekleyin

---

## Kod Standartları

### Python Stil Rehberi

- **PEP 8** takip edilir
- 4 boşluk indentation
- Türkçe yorumlar tercih edilir (ama İngilizce de kabul edilir)
- Fonksiyon docstring'leri zorunludur

```python
def fonksiyon_adi(param1: str, param2: int) -> bool:
    """Fonksiyonun ne yaptığını açıklar.

    Args:
        param1: Birinci parametrenin açıklaması
        param2: İkinci parametrenin açıklaması

    Returns:
        Dönüş değerinin açıklaması
    """
    ...
```

### Dosya Organizasyonu

```
friday/
├── brain.py              # Ana LLM pipeline
├── router.py             # Routing mantığı
├── memory.py             # Hafıza sistemi
├── tools/
│   ├── actions.py        # Tool registry (DEĞİŞTİRME!)
│   ├── desktop.py        # Yeni desktop araçları
│   └── ...
└── stones/              # Adaptif katmanlar
```

### Yeni Tool Ekleme

1. İlgili `tools/*.py` dosyasına fonksiyonu ekleyin
2. `DESKTOP_TOOLS`, `MEMORY_TOOLS` vb. listeye ekleyin
3. `ALL_TOOLS` için `actions.py`'yi güncelleyin
4. Test yazın

```python
# Örnek: friday/tools/desktop.py'ye yeni araç
def yeni_arac(param: str) -> str:
    """Açıklama.

    Args:
        param: Parametre açıklaması

    Returns:
        Sonuç açıklaması
    """
    # ... kod ...
    return "Sonuç"

# Listeye ekle
DESKTOP_TOOLS = [
    ...
    yeni_arac,
]
```

---

## Test Standartları

### Test Edilmesi Gerekenler

| Tip | Açıklama |
|-----|----------|
| Unit Test | Her fonksiyon için temel test |
| Entegrasyon Testi | Modüller arası etkileşim |
| E2E Test | Tam akış testleri |

### Test Çalıştırma

```powershell
# Tüm testler
python -m unittest discover tests

# Belirli test
python -m unittest tests.test_router

# Smoke test
python test_system_full.py
```

---

## Commit Mesaj Formatı

```
<tip>: <kısa açıklama>

<opsiyonel detay>

<opsiyonel footer>
```

### Tipler

| Tip | Kullanım |
|-----|----------|
| `feat` | Yeni özellik |
| `fix` | Hata düzeltmesi |
| `docs` | Dokümantasyon |
| `refactor` | Kod yeniden yapılandırma |
| `test` | Test ekleme/güncelleme |
| `chore` | Bakım, bağımlılık güncelleme |

### Örnekler

```
feat: Telegram bot için dosya gönderme eklendi

-fix: memory silme komutu çalışmıyordu
Düzeltildi: forget_by_content threshold 0.45'ten 0.30'a düşürüldü

docs: README güncellendi
```

---

## Issue & PR Template

### Bug Report Template

```markdown
## Hata Açıklaması
Kısa ve net açıklama

## Adımlar
1. ...
2. ...
3. ...

## Beklenen Davranış
Ne olması gerektiği

## Gerçek Davranış
Ne oluyor

## Environment
- OS: Windows 11
- Python: 3.14.2
- FRIDAY versiyon: 0.1.0
```

### Feature Request Template

```markdown
## Özet
Kısa açıklama

## Motivasyon
Neden bu özellik gerekli?

## Öneri
Nasıl çalışması gerektiği

## Alternatifler
Düşündüğünüz diğer yaklaşımlar
```

---

## Lisans

Katkıda bulunarak, kodunuzun Apache 2.0 lisansı altında yayınlanacağını kabul etmiş olursunuz.

---

## Sorular?

- GitHub Issues
- Tartışmalar bölümü
- Discord sunucusu *(yakında)*

---

<p align="center">
  <em>FRIDAY'i birlikte daha iyi hale getirelim!</em>
</p>
