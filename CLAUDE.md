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

### Genel (tüm projelerde geçerli)
- Repo private. Branch: `main` (stable) + `develop` (aktif). Her zaman `develop`'ta çalış.
- Her iş bir GitHub issue'dan başlar. Issue = to-do + karar logu.
- Kararlar `decisions.md`'ye değil, issue yorumlarına gider.
- SOLID prensiplerine uy. Basit, sade, pratik mimari.
- Varsayım yapma — sor.

### Bu Projeye Özel
- `data/raw/` hiçbir zaman elle düzenlenmez
- `knowledge/` agent tarafından düzenlenmez — değişiklik önerisi insana iletilir
- Her pipeline çalışmasında `data/snapshots/YYYY-MM.json` arşivi oluşturulur
- `.env` asla commit'lenmez

## Current Status

2026-04-10 — Proje kuruldu. Pipeline iskelet hazır (fetch, transform, run). Insight agent dokümante edildi. Sıradaki: EVDS API key ile seri kodlarını doğrula, ilk fetch'i çalıştır.
