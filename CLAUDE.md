# HousingScope

Konut alıcısı, satıcısı ve yatırımcısı için aylık güncellenen makroekonomik dashboard.

## Proje Yapısı

```
pipeline/       ← EVDS → Snowflake RAW (Python)
sql/staging/    ← RAW → STAGING (normalize + agrega)
sql/mart/       ← STAGING → MART (birleşik tablo)
setup/          ← Snowflake ilk kurulum SQL'leri
agents/         ← Insight agent (aylık otomatik yorum)
knowledge/      ← Statik piyasa bilgisi — agent okur, yazmaz
outputs/        ← Agent çıktıları (aylık markdown yorumlar)
data/           ← Klasörler korunur; ham veri artık Snowflake RAW'da
                   data/raw/       → Snowflake RAW schema
                   data/processed/ → Snowflake MART.konut_indicators
                   data/snapshots/ → Snowflake Time Travel
```

## Komutlar

```bash
python pipeline/run.py --mode backfill      # İlk kurulum (2020'den bugüne)
python pipeline/run.py --mode incremental   # Aylık güncelleme
```

## Ortam Değişkenleri

`.env` dosyasına ekle (bkz. `.env.example`):
```
EVDS_API_KEY=...
SNOWFLAKE_ACCOUNT=...
SNOWFLAKE_USER=...
SNOWFLAKE_WAREHOUSE=...
SNOWFLAKE_DATABASE=HOUSINGSCOPE_DB
SNOWFLAKE_ROLE=ACCOUNTADMIN
SNOWFLAKE_PASSWORD=...   # boşsa externalbrowser auth kullanılır
```

## EVDS Seri Kodları (20 Seri)

| Key | EVDS Kodu | Frekans | Gösterge |
|-----|-----------|---------|----------|
| `kfe` | `TP.KFE.TR` | aylık | Konut Fiyat Endeksi (güncel) |
| `kfe_yeni` | `TP.YKFE.TR` | aylık | Yeni Konutlar Fiyat Endeksi |
| `kfe_ikinciel` | `TP.YOKFEND.TR` | aylık | İkinci El Konutlar Fiyat Endeksi |
| `konut_faiz` | `TP.KTF12` | haftalık→aylık | Konut Kredisi Faizi (akım) |
| `tufe` | `TP.TUKFIY2025.GENEL` | aylık | TÜFE Genel (güncel) |
| `usd_try` | `TP.DK.USD.A` | günlük→aylık | USD/TRY |
| `insaat_maliyet` | `TP.TUFE1YI.T1` | aylık | Yurt İçi ÜFE (inşaat maliyet proxy) |
| `konut_satis_toplam` | `TP.AKONUTSAT1.KTRTOPLAM` | aylık | Toplam Satış Adedi |
| `konut_satis_ipotekli` | `TP.AKONUTSAT2.KTRTOPLAM` | aylık | İpotekli Satışlar |
| `konut_satis_ilkel` | `TP.AKONUTSAT3.KTRTOPLAM` | aylık | İlk El Satışlar |
| `konut_satis_ikinciel` | `TP.AKONUTSAT4.KTRTOPLAM` | aylık | İkinci El Satışlar |
| `mevduat_faiz` | `TP.TRY.MT01` | haftalık→aylık | TL Mevduat Faizi 1 Ay (%) |
| `altin` | `TP.MK.KUL.YTL` | aylık | Külçe Altın Satış Fiyatı (TL/Gr) |
| `politika_faiz` | `TP.BISPOLFAIZ.TUR` | aylık | TCMB 1 Haftalık Repo Faizi |
| `kira_endeksi` | `TP.YKKE.TR` | aylık | Yeni Kiracı Kira Endeksi |
| `birimfiyat_ist` | `TP.BIRIMFIYAT.IST` | çeyreklik→aylık | İstanbul Konut Birim Fiyatı (TL/m²) |
| `birimfiyat_ank` | `TP.BIRIMFIYAT.ANK` | çeyreklik→aylık | Ankara Konut Birim Fiyatı (TL/m²) |
| `birimfiyat_izm` | `TP.BIRIMFIYAT.IZM` | çeyreklik→aylık | İzmir Konut Birim Fiyatı (TL/m²) |
| `kfe_istanbul` | `TP.BK.ISTANBUL` | aylık | İstanbul Konut Fiyat Endeksi |
| `kfe_ankara` | `TP.BK.ANKARA` | aylık | Ankara Konut Fiyat Endeksi |
| `kfe_izmir` | `TP.BK.IZMIR` | aylık | İzmir Konut Fiyat Endeksi |

## Veri Akışı

```
EVDS API → Snowflake RAW (20 tablo)
         → SQL staging → Snowflake STAGING (normalize + agrega)
         → SQL mart    → Snowflake MART.konut_indicators
                       → Vercel Blob (public JSON)
                       → dashboard (datamesa.com/housingscope)
                       → insight-agent
```

## Snowflake Yapısı

```
HOUSINGSCOPE_DB
├── RAW      — Ham EVDS verisi (20 tablo, varchar raw_date/raw_value)
├── STAGING  — Normalize + agrega (month VARCHAR YYYY-MM, value FLOAT)
└── MART     — konut_indicators (month, series_key, series_label, value)
```

İlk kurulum: `setup/init_snowflake.sql` → Snowflake Worksheets'te "Run All"

## Agent

`agents/insight-agent/` — Aylık kalkar, MART tablosunu sorgular, `outputs/` altına yorum yazar.
Heartbeat: Her ayın 3'ü (EVDS yayınından ~2 gün sonra).

## Kurallar

### Genel (tüm projelerde geçerli)
- Repo private. Branch: `main` (stable) + `develop` (aktif). Her zaman `develop`'ta çalış.
- Her iş bir GitHub issue'dan başlar. Issue = to-do + karar logu.
- Kararlar `decisions.md`'ye değil, issue yorumlarına gider.
- SOLID prensiplerine uy. Basit, sade, pratik mimari.
- Varsayım yapma — sor.

### Bu Projeye Özel
- `data/` klasörleri korunur ama içerik Snowflake'te — elle dokunulmaz
- `knowledge/` agent tarafından düzenlenmez — değişiklik önerisi insana iletilir
- `.env` asla commit'lenmez
- Snowflake Time Travel snapshot rolünü üstleniyor (data/snapshots/ artık kullanılmıyor)

## Dashboard

Dashboard bu repoda **yaşamıyor** — `tmy-datamesa/datamesa` (personal_ws) reposunda.

- **Route:** `datamesa.com/housingscope`
- **Veri akışı:** Bu repo → Vercel Blob → `GET /api/housingscope/data` → dashboard
- `dashboard/` klasörü placeholder olarak korunuyor

## Current Status

2026-04-15 — Pipeline 20 seriye tamamlandı (Issue #12). Dashboard `personal_ws`'de canlı.
Aylık otomasyon: her ayın 3'ü GitHub Actions cron.
