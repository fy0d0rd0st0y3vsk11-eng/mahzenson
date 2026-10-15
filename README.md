# Mahzen Discord Bot

Python 3.11/3.12, discord.py ve OpenRouter ile hazırlanmış başlangıç sürümü.

## Komutlar
- `/ping` — bağlantı gecikmesi
- `/yardim` — komut listesi
- `/sunucu` — sunucu bilgileri
- `/ask soru:` — OpenRouter yapay zekâsı
- `/anket soru: secenek1: secenek2:` — iki seçenekli tepki anketi
- `/duyuru mesaj:` — yönetici duyurusu
- `/temizle adet:` — Mesajları Yönet izniyle 1-50 mesaj temizleme

## Hosting ayarları
Başlatma komutu: `python -m app.main`
Kurulum komutu: `pip install -r requirements.txt`

Environment Variables:
- `DISCORD_TOKEN` — Discord Developer Portal bot tokenı
- `OPENROUTER_API_KEY` — OpenRouter API anahtarı (AI komutu için)
- `OPENROUTER_MODEL` — varsayılan `openai/gpt-4o-mini`
- `DATABASE_PATH` — kalıcı depolamadaki SQLite yolu
- `LOG_LEVEL` — varsayılan `INFO`

Gerçek tokenları koda yazma, ZIP'e koyma veya başkalarıyla paylaşma. OpenRouter kullanımının ücret doğurabileceğini unutma; model fiyatını kontrol et ve harcama sınırı belirle. Ücretsiz hosting ve 7/24 çalışma bu proje tarafından garanti edilemez. SQLite verilerinin korunması için veritabanı kalıcı depolamada tutulmalıdır.

## Discord kurulumu
Discord Developer Portal'da uygulama ve bot oluştur. OAuth2 URL Generator'da `bot` ve `applications.commands` kapsamlarını seç; gerekli izinleri ver. `/temizle` için botta `Manage Messages` izni gerekir. Token sızarsa yenile.
