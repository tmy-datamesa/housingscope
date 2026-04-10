# HousingScope

Konut alıcısı, satıcısı ve yatırımcısı için aylık güncellenen makroekonomik dashboard.

EVDS API ile 5 gösterge · Aylık otomatik güncelleme · AI destekli yorum

## Kurulum

```bash
pip install -r requirements.txt
cp .env.example .env
# .env dosyasına EVDS_API_KEY ekle
```

## Kullanım

```bash
# Tam pipeline (veri çek + dönüştür)
python pipeline/run.py

# Ayrı adımlar
python pipeline/fetch.py      # Sadece EVDS'den çek
python pipeline/transform.py  # Sadece dönüştür
```

## Göstergeler

| Gösterge | Seri Kodu |
|----------|-----------|
| Konut Fiyat Endeksi | TP.HKFE01 |
| Konut Kredisi Faizi | TP.TK.TG.AY |
| TÜFE Genel | TP.FE.OKTG01 |
| USD/TRY | TP.DK.USD.A |
| İnşaat Maliyet Endeksi | TP.YIEX |

## Yapı

```
pipeline/   → Veri çekme ve dönüştürme
dashboard/  → Frontend (TBD)
agents/     → Insight agent (aylık yorum)
data/       → Ham ve işlenmiş veriler
knowledge/  → Piyasa bilgisi
outputs/    → Aylık yorumlar
```
