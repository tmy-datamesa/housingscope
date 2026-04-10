# HousingScope

Konut alıcısı, satıcısı ve yatırımcısı için aylık güncellenen makroekonomik dashboard.

## Proje Yapısı

```
pipeline/       ← EVDS veri çekme ve dönüştürme (Python)
dashboard/      ← Frontend (TBD: Next.js veya FastAPI+HTML)
agents/         ← Insight agent (aylık otomatik yorum)
data/raw/       ← EVDS ham JSON — değiştirme
data/processed/ ← Grafik formatı JSON — pipeline yazar
data/snapshots/ ← Aylık arşiv
knowledge/      ← Statik piyasa bilgisi — agent okur, yazmaz
journal/        ← Paylaşılan hafıza — agent yazar
outputs/        ← Agent çıktıları (aylık markdown yorumlar)
```

## Komutlar

```bash
python pipeline/run.py          # Veri çek + dönüştür (tam pipeline)
python pipeline/fetch.py        # Sadece EVDS API çekimi
python pipeline/transform.py    # Sadece dönüştürme
```

## Ortam Değişkenleri

`.env` dosyasına ekle:
```
EVDS_API_KEY=...
```

## EVDS Seri Kodları

| Kod | Gösterge |
|-----|----------|
| `TP.HKFE01` | Konut Fiyat Endeksi (KFE) |
| `TP.TK.TG.AY` | Konut kredisi faiz oranı |
| `TP.FE.OKTG01` | TÜFE genel |
| `TP.DK.USD.A` | USD/TRY |
| `TP.YIEX` | İnşaat maliyet endeksi |

## Veri Akışı

```
EVDS API → data/raw/{seri}.json → data/processed/dashboard.json → dashboard
                                                                 → insight-agent
```

## Agent

`agents/insight-agent/` — Aylık kalkar, işlenmiş veriyi okur, `outputs/` altına yorum yazar.
Heartbeat: Her ayın 3'ü (EVDS yayınından ~2 gün sonra).

## Kurallar

- `data/raw/` hiçbir zaman elle düzenlenmez
- `knowledge/` agent tarafından düzenlenmez — değişiklik önerisi insan'a iletilir
- Her pipeline çalışmasında `data/snapshots/YYYY-MM.json` arşivi oluşturulur
- `.env` asla commit'lenmez
