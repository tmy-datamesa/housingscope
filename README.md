# HousingScope

Konut alıcısı, satıcısı ve yatırımcısı için aylık güncellenen makroekonomik dashboard.

EVDS API ile 20 gösterge · Snowflake ELT · Vercel Blob · AI destekli yorum

## Kurulum

```bash
pip install -r requirements.txt
cp .env.example .env
# .env dosyasına EVDS_API_KEY ve Snowflake credentials ekle
```

## Kullanım

```bash
# İlk kurulum — 2020'den bugüne tam yükleme
python pipeline/run.py --mode backfill

# Aylık güncelleme (son 2 ay, merge-based)
python pipeline/run.py --mode incremental

# MART → Vercel Blob export (pipeline sonrası otomatik çalışır)
python pipeline/export_to_blob.py
```

GitHub Actions her ayın 3'ünde `incremental` + `export_to_blob` çalıştırır.

## Göstergeler (20 Seri)

| Key | EVDS Kodu | Frekans | Gösterge |
|-----|-----------|---------|----------|
| `kfe` | `TP.KFE.TR` | aylık | Konut Fiyat Endeksi (Genel) |
| `kfe_yeni` | `TP.YKFE.TR` | aylık | Yeni Konutlar Fiyat Endeksi |
| `kfe_ikinciel` | `TP.YOKFEND.TR` | aylık | İkinci El Konutlar Fiyat Endeksi |
| `kfe_istanbul` | `TP.BK.ISTANBUL` | aylık | İstanbul Konut Fiyat Endeksi |
| `kfe_ankara` | `TP.BK.ANKARA` | aylık | Ankara Konut Fiyat Endeksi |
| `kfe_izmir` | `TP.BK.IZMIR` | aylık | İzmir Konut Fiyat Endeksi |
| `tufe` | `TP.TUKFIY2025.GENEL` | aylık | TÜFE Genel |
| `insaat_maliyet` | `TP.TUFE1YI.T1` | aylık | Yurt İçi ÜFE (inşaat maliyet proxy) |
| `konut_faiz` | `TP.KTF12` | haftalık→aylık | Konut Kredisi Faizi |
| `mevduat_faiz` | `TP.TRY.MT01` | haftalık→aylık | TL Mevduat Faizi 1 Ay (%) |
| `politika_faiz` | `TP.BISPOLFAIZ.TUR` | aylık | TCMB Politika Faizi |
| `usd_try` | `TP.DK.USD.A` | günlük→aylık | USD/TRY |
| `altin` | `TP.MK.KUL.YTL` | aylık | Külçe Altın Satış Fiyatı (TL/Gr) |
| `kira_endeksi` | `TP.YKKE.TR` | aylık | Yeni Kiracı Kira Endeksi |
| `konut_satis_toplam` | `TP.AKONUTSAT1.KTRTOPLAM` | aylık | Toplam Konut Satışı (Adet) |
| `konut_satis_ipotekli` | `TP.AKONUTSAT2.KTRTOPLAM` | aylık | İpotekli Satışlar |
| `konut_satis_ilkel` | `TP.AKONUTSAT3.KTRTOPLAM` | aylık | İlk El Satışlar |
| `konut_satis_ikinciel` | `TP.AKONUTSAT4.KTRTOPLAM` | aylık | İkinci El Satışlar |
| `birimfiyat_ist` | `TP.BIRIMFIYAT.IST` | çeyreklik→aylık | İstanbul Konut Birim Fiyatı (TL/m²) |
| `birimfiyat_ank` | `TP.BIRIMFIYAT.ANK` | çeyreklik→aylık | Ankara Konut Birim Fiyatı (TL/m²) |
| `birimfiyat_izm` | `TP.BIRIMFIYAT.IZM` | çeyreklik→aylık | İzmir Konut Birim Fiyatı (TL/m²) |

## Yapı

```
pipeline/       → EVDS → Snowflake RAW (fetch.py, run.py, export_to_blob.py)
sql/staging/    → RAW → STAGING: 20 normalize SQL dosyası
sql/mart/       → STAGING → MART.konut_indicators (tek birleşik tablo)
setup/          → Snowflake ilk kurulum (tek seferlik)
agents/         → Insight agent (aylık AI yorum, outputs/ altına yazar)
knowledge/      → Statik piyasa bilgisi — agent okur, yazmaz
outputs/        → Aylık insight markdown dosyaları
data/           → Klasörler korunur; içerik Snowflake'te
```

## Veri Akışı

```
EVDS API → Snowflake RAW → STAGING → MART.konut_indicators
                                    → Vercel Blob (public JSON)
                                    → datamesa.com/housingscope
                                    → insight-agent → outputs/
```

## Ortam Değişkenleri

`.env` (bkz. `.env.example`):

```
EVDS_API_KEY=...
SNOWFLAKE_ACCOUNT=...
SNOWFLAKE_USER=...
SNOWFLAKE_PASSWORD=...   # boşsa externalbrowser auth
SNOWFLAKE_WAREHOUSE=...
SNOWFLAKE_DATABASE=HOUSINGSCOPE_DB
SNOWFLAKE_ROLE=ACCOUNTADMIN
BLOB_READ_WRITE_TOKEN=...  # export_to_blob.py için
```
