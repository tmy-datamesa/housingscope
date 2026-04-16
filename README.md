# HousingScope

Monthly-updated macroeconomic dashboard for Turkey's housing market — built for buyers, sellers, and investors.

**Live:** [datamesa.dev/housingscope](https://datamesa.dev/housingscope)

<img width="1117" height="962" alt="image" src="https://github.com/user-attachments/assets/b58abe24-57d5-4a2f-b4ee-cbb860d09967" />

---

## What It Does

HousingScope tracks 20 macroeconomic indicators from Turkey's Central Bank (EVDS) and delivers a monthly-refreshed dashboard with price indices, interest rates, sales volumes, rental trends, and city-level comparisons — automatically, without manual intervention.

---

## Architecture

```
EVDS API (TCMB)
    │
    ▼
Python pipeline (fetch + normalize)
    │
    ├── Snowflake RAW       ← raw time-series per indicator
    ├── Snowflake STAGING   ← normalized: YYYY-MM dates, FLOAT values
    └── Snowflake MART      ← single unified table (month, series_key, value)
                │
                ▼
        Vercel Blob         ← public JSON endpoint
                │
                ▼
        Dashboard           ← FastAPI + Chart.js, datamesa.dev/housingscope
```

**Design decisions:**
- **Three-layer ELT** (RAW → STAGING → MART) separates concerns: raw ingestion, normalization, and presentation are independently maintainable
- **Snowflake Time Travel** replaces manual snapshots — historical states are queryable without extra storage
- **Vercel Blob as public cache** decouples the pipeline from the dashboard; the site reads a static JSON endpoint, not a live database connection
- **GitHub Actions cron** runs on the 3rd of each month — two days after EVDS publishes — making the pipeline fully automated

---

## Data Pipeline

**20 EVDS indicators** across five categories:

| Category | Indicators |
|---|---|
| Housing prices | KFE (general, new, resale), city-level KFE (Istanbul, Ankara, Izmir) |
| Inflation | CPI (TÜFE), construction cost (PPI proxy) |
| Interest rates | Mortgage rate, 1-month deposit rate, TCMB policy rate |
| Market activity | Total sales, mortgage sales, new vs. resale sales |
| Benchmarks | USD/TRY, gold price (TRY/g), rental index, city unit prices (TRY/m²) |

Frequencies handled: monthly, weekly (averaged to monthly), daily (averaged to monthly), quarterly (mapped to period end month).

**SQL staging layer** normalizes each series independently — adding a new indicator means one new `.sql` file and one line in `fetch.py`.

---

## Insight Agent

A Claude-powered agent runs after each pipeline update. It reads the MART table, computes month-over-month and year-over-year changes across all 20 indicators, and produces a structured markdown report with:
- Real vs. nominal price spread (KFE − CPI)
- Buyer / seller / investor signal for the month
- Key risks and inflection points

Output: `outputs/YYYY-MM_insight.md`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Data source | EVDS (TCMB Open Data API) |
| Pipeline | Python (`requests`, `snowflake-connector`, `python-dotenv`) |
| Storage | Snowflake (RAW / STAGING / MART schemas) |
| Public cache | Vercel Blob |
| Dashboard | FastAPI + Jinja2 + Chart.js (vanilla, no framework) |
| Hosting | Vercel (Python Fluid Compute) |
| Automation | GitHub Actions (monthly cron) |
| Insight agent | Claude (Anthropic) |

---

## Portfolio Note

Snowflake is used intentionally here to demonstrate ELT pipeline design — RAW/STAGING/MART separation, `MERGE`-based incremental loading, and `ensure_raw_tables()` for schema management. At this data volume (20 series, ~1,500 rows) it is deliberate over-engineering for learning and demonstration purposes.

<img width="2550" height="1351" alt="image" src="https://github.com/user-attachments/assets/3ede4258-f1a1-4f0b-9418-d40384e2fc5b" />

<img width="567" height="1200" alt="image" src="https://github.com/user-attachments/assets/d7ae056e-5f51-4beb-a0be-61a79f38baa4" />

