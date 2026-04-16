# HousingScope

Monthly macroeconomic dashboard for Turkey's housing market.

## Project Structure

```
pipeline/       ← EVDS → Snowflake RAW  (fetch.py, run.py, export_to_blob.py)
sql/staging/    ← RAW → STAGING: 20 normalized SQL files
sql/mart/       ← STAGING → MART.konut_indicators (single unified table)
setup/          ← One-time Snowflake initialization (run manually)
agents/         ← Insight agent — monthly AI commentary, writes to outputs/
knowledge/      ← Static market reference — agent reads, never writes
outputs/        ← Monthly insight markdown files (YYYY-MM_insight.md)
data/           ← Folder structure preserved; data lives in Snowflake
```

## Commands

```bash
python pipeline/run.py --mode backfill      # Full load from 2020
python pipeline/run.py --mode incremental   # Last 2 months (merge-based)
python pipeline/export_to_blob.py           # MART → Vercel Blob (public JSON)
```

GitHub Actions runs `incremental` + `export_to_blob` on the 3rd of each month.

## Environment Variables

Copy `.env.example` to `.env`:

```
EVDS_API_KEY=...
SNOWFLAKE_ACCOUNT=...
SNOWFLAKE_USER=...
SNOWFLAKE_PASSWORD=...        # leave empty for externalbrowser auth (local)
SNOWFLAKE_WAREHOUSE=...
SNOWFLAKE_DATABASE=HOUSINGSCOPE_DB
SNOWFLAKE_ROLE=ACCOUNTADMIN
BLOB_READ_WRITE_TOKEN=...     # required for export_to_blob.py
```

## EVDS Series (20)

| Key | EVDS Code | Frequency | Indicator |
|-----|-----------|-----------|-----------|
| `kfe` | `TP.KFE.TR` | monthly | Housing Price Index (general) |
| `kfe_yeni` | `TP.YKFE.TR` | monthly | New Housing Price Index |
| `kfe_ikinciel` | `TP.YOKFEND.TR` | monthly | Resale Housing Price Index |
| `kfe_istanbul` | `TP.BK.ISTANBUL` | monthly | Istanbul Housing Price Index |
| `kfe_ankara` | `TP.BK.ANKARA` | monthly | Ankara Housing Price Index |
| `kfe_izmir` | `TP.BK.IZMIR` | monthly | Izmir Housing Price Index |
| `tufe` | `TP.TUKFIY2025.GENEL` | monthly | CPI (general) |
| `insaat_maliyet` | `TP.TUFE1YI.T1` | monthly | Domestic PPI (construction cost proxy) |
| `konut_faiz` | `TP.KTF12` | weekly → monthly | Mortgage Rate |
| `mevduat_faiz` | `TP.TRY.MT01` | weekly → monthly | 1-month TRY Deposit Rate |
| `politika_faiz` | `TP.BISPOLFAIZ.TUR` | monthly | TCMB Policy Rate |
| `usd_try` | `TP.DK.USD.A` | daily → monthly | USD/TRY |
| `altin` | `TP.MK.KUL.YTL` | monthly | Gold Price (TRY/g) |
| `kira_endeksi` | `TP.YKKE.TR` | monthly | New Tenant Rental Index |
| `konut_satis_toplam` | `TP.AKONUTSAT1.KTRTOPLAM` | monthly | Total Housing Sales (units) |
| `konut_satis_ipotekli` | `TP.AKONUTSAT2.KTRTOPLAM` | monthly | Mortgage Sales |
| `konut_satis_ilkel` | `TP.AKONUTSAT3.KTRTOPLAM` | monthly | New Housing Sales |
| `konut_satis_ikinciel` | `TP.AKONUTSAT4.KTRTOPLAM` | monthly | Resale Sales |
| `birimfiyat_ist` | `TP.BIRIMFIYAT.IST` | quarterly → monthly | Istanbul Unit Price (TRY/m²) |
| `birimfiyat_ank` | `TP.BIRIMFIYAT.ANK` | quarterly → monthly | Ankara Unit Price (TRY/m²) |
| `birimfiyat_izm` | `TP.BIRIMFIYAT.IZM` | quarterly → monthly | Izmir Unit Price (TRY/m²) |

## Data Flow

```
EVDS API → Snowflake RAW (20 tables)
         → SQL staging → Snowflake STAGING (normalized)
         → SQL mart    → Snowflake MART.konut_indicators
                       → Vercel Blob (public JSON)
                       → datamesa.dev/housingscope
                       → insight agent → outputs/
```

## Snowflake Schema

```
HOUSINGSCOPE_DB
├── RAW      — Raw EVDS data (20 tables, varchar raw_date / raw_value)
├── STAGING  — Normalized (month VARCHAR YYYY-MM, value FLOAT)
└── MART     — konut_indicators (month, series_key, series_label, value)
```

Initial setup: run `setup/init_snowflake.sql` in Snowflake Worksheets once.

## Dashboard

Dashboard lives in `tmy-datamesa/datamesa` (personal_ws repo), not here.

- Route: `datamesa.dev/housingscope`
- Data flow: this repo → Vercel Blob → `GET /api/housingscope/data` → dashboard
- `dashboard/` folder is kept as a placeholder

## Insight Agent

`agents/insight-agent/` — runs after each pipeline update, queries MART, writes monthly commentary to `outputs/`.
Heartbeat: 3rd of each month (∼2 days after EVDS publishes).

## Rules

### General

- Repo is private. Branches: `main` (stable) + `develop` (active). Always work on `develop`.
- Every task starts with a GitHub issue. Issue = to-do + decision log.
- Decisions go in issue comments, not in a decisions file.
- Follow SOLID. Keep it simple and practical.
- Never assume — ask.

### Project-specific

- `data/` folders are preserved but content lives in Snowflake — do not touch manually
- `knowledge/` is read-only for the agent — propose changes to a human
- Never commit `.env`
- Snowflake Time Travel owns the snapshot role (`data/snapshots/` is unused)

## Portfolio Note

Snowflake is used intentionally to demonstrate ELT pipeline design (RAW → STAGING → MART separation, `MERGE`-based incremental loading). At this data volume it is deliberate over-engineering for learning and portfolio purposes. New dashboards in `tmy-datamesa/datamesa` use a database-free pattern (EVDS → Python → Vercel Blob directly).
