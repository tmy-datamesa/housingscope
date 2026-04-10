"""
EVDS API'den ham veri çeker ve Snowflake RAW schema'ya yükler.

Kullanım:
    python pipeline/fetch.py --mode backfill      # 2020'den bugüne, bir kez
    python pipeline/fetch.py --mode incremental   # Son 2 ay (GitHub Actions)
"""

import argparse
import os
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

import requests
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

# EVDS API
EVDS_API_KEY = os.getenv("EVDS_API_KEY")
EVDS_BASE_URL = "https://evds3.tcmb.gov.tr/igmevdsms-dis"
BACKFILL_START_YEAR = 2020

# Seriler: {dosya_key: (evds_kodu, frekans)}
# frekans: "monthly" | "weekly" | "daily"
SERIES = {
    "kfe":             ("TP.KFE.TR",      "monthly"),  # Konut Fiyat Endeksi (güncel — TP.HKFE01'in yerini aldı)
    "kfe_yeni":        ("TP.YKFE.TR",     "monthly"),  # Yeni konutlar fiyat endeksi
    "kfe_ikinciel":    ("TP.YOKFEND.TR",  "monthly"),  # İkinci el konutlar fiyat endeksi
    "konut_faiz":      ("TP.KTF12",       "weekly"),
    "tufe":            ("TP.TUKFIY2025.GENEL", "monthly"),  # TÜFE Genel (güncel — TP.FE.OKTG01'in yerini aldı)
    "usd_try":         ("TP.DK.USD.A",    "daily"),
    "insaat_maliyet":        ("TP.TUFE1YI.T1",       "monthly"),
    "konut_satis_toplam":    ("TP.AKONUTSAT1.KTRTOPLAM", "monthly"),  # Toplam satış adedi
    "konut_satis_ipotekli":  ("TP.AKONUTSAT2.KTRTOPLAM", "monthly"),  # İpotekli satışlar
    "konut_satis_ilkel":     ("TP.AKONUTSAT3.KTRTOPLAM", "monthly"),  # İlk el satışlar
    "konut_satis_ikinciel":  ("TP.AKONUTSAT4.KTRTOPLAM", "monthly"),  # İkinci el satışlar
    "mevduat_faiz":          ("TP.TRY.MT01",           "weekly"),   # 1 Aya Kadar Vadeli TL Mevduat Faizi (%)
    "altin":                 ("TP.MK.KUL.YTL",         "monthly"),  # Külçe Altın Satış Fiyatı (TL/Gr)
}


# ---------------------------------------------------------------------------
# EVDS
# ---------------------------------------------------------------------------

def evds_fetch(series_code: str, start_date: str, end_date: str) -> list[dict]:
    """Tek bir EVDS isteği atar, items listesini döner."""
    uri = f"series={series_code}&startDate={start_date}&endDate={end_date}&type=json"
    url = f"{EVDS_BASE_URL}/{uri}"
    response = requests.get(url, headers={"key": EVDS_API_KEY}, timeout=30)
    response.raise_for_status()
    return response.json().get("items", [])


def extract_value(item: dict) -> str | None:
    """EVDS item'ından değer alanını bulur (alan adı seriden seriye değişiyor)."""
    skip = {"Tarih", "date", "UNIXTIME", "YEARWEEK"}
    for key, val in item.items():
        if key not in skip:
            return val if val not in (None, "") else None
    return None


def fetch_series(name: str, code: str, frequency: str, mode: str) -> list[tuple]:
    """
    Bir seriyi EVDS'den çeker.
    Dönen değer: [(raw_date, raw_value, series_code, source_year), ...]
    """
    today = date.today()
    rows = []

    if mode == "backfill":
        if frequency in ("daily", "weekly"):
            # Yıllık dilimler — EVDS 1000 kayıt limitini aşmamak için
            for year in range(BACKFILL_START_YEAR, today.year + 1):
                start = f"01-01-{year}"
                end = f"31-12-{year}"
                items = evds_fetch(code, start, end)
                for item in items:
                    val = extract_value(item)
                    rows.append((item.get("Tarih"), val, code, year))
        else:
            # Aylık seri — tek istekte tüm geçmiş
            start = f"01-01-{BACKFILL_START_YEAR}"
            end = today.strftime("%d-%m-%Y")
            items = evds_fetch(code, start, end)
            for item in items:
                val = extract_value(item)
                rows.append((item.get("Tarih"), val, code, None))

    elif mode == "incremental":
        # Son 2 ay — MERGE ile upsert yapılır
        start_dt = today - relativedelta(months=2)
        start = start_dt.strftime("01-%m-%Y")
        end = today.strftime("%d-%m-%Y")
        items = evds_fetch(code, start, end)
        for item in items:
            val = extract_value(item)
            rows.append((item.get("Tarih"), val, code, None))

    return rows


# ---------------------------------------------------------------------------
# Snowflake
# ---------------------------------------------------------------------------

def snowflake_connect() -> snowflake.connector.SnowflakeConnection:
    """
    Snowflake bağlantısı kurar.
    - SNOWFLAKE_PASSWORD boşsa: externalbrowser (lokal geliştirme)
    - SNOWFLAKE_PASSWORD doluysa: username+password (GitHub Actions)
    """
    password = os.getenv("SNOWFLAKE_PASSWORD", "")
    auth_params = (
        {"authenticator": "externalbrowser"}
        if not password
        else {"password": password}
    )

    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        role=os.getenv("SNOWFLAKE_ROLE"),
        schema="RAW",
        **auth_params,
    )


def load_backfill(conn, table: str, rows: list[tuple]) -> int:
    """
    Backfill: tabloyu truncate edip tüm geçmişi yükler.
    Dönen değer: yüklenen satır sayısı.
    """
    cur = conn.cursor()
    cur.execute(f"TRUNCATE TABLE RAW.{table}")
    cur.executemany(
        f"""
        INSERT INTO RAW.{table} (raw_date, raw_value, series_code, source_year)
        VALUES (%s, %s, %s, %s)
        """,
        rows,
    )
    return len(rows)


def load_incremental(conn, table: str, rows: list[tuple]) -> int:
    """
    Incremental: aynı (raw_date, series_code) çifti varsa atla, yoksa ekle (upsert).
    Dönen değer: eklenen satır sayısı.
    """
    cur = conn.cursor()
    inserted = 0

    for raw_date, raw_value, series_code, source_year in rows:
        cur.execute(
            f"""
            MERGE INTO RAW.{table} AS target
            USING (
                SELECT %s AS raw_date, %s AS raw_value, %s AS series_code
            ) AS source
            ON target.raw_date = source.raw_date
            AND target.series_code = source.series_code
            WHEN NOT MATCHED THEN
                INSERT (raw_date, raw_value, series_code, loaded_at)
                VALUES (source.raw_date, source.raw_value, source.series_code, CURRENT_TIMESTAMP)
            """,
            (raw_date, raw_value, series_code),
        )
        inserted += cur.rowcount

    return inserted


# ---------------------------------------------------------------------------
# Ana fonksiyon
# ---------------------------------------------------------------------------

def ensure_raw_tables(conn):
    """SERIES'teki her seri için RAW tablo yoksa oluşturur."""
    cur = conn.cursor()
    for name in SERIES:
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS RAW.{name}
            LIKE RAW.kfe
        """)


def fetch_all(mode: str) -> dict:
    if not EVDS_API_KEY:
        raise ValueError("EVDS_API_KEY bulunamadı. .env dosyasını kontrol et.")

    print(f"Snowflake bağlanılıyor...")
    conn = snowflake_connect()
    ensure_raw_tables(conn)
    results = {}

    for name, (code, frequency) in SERIES.items():
        print(f"\n  {name} ({code}) çekiliyor [{frequency}]...")
        try:
            rows = fetch_series(name, code, frequency, mode)
            print(f"    EVDS: {len(rows)} satır alındı")

            if mode == "backfill":
                count = load_backfill(conn, name, rows)
                print(f"    Snowflake RAW.{name}: {count} satır yüklendi (truncate+insert)")
            else:
                count = load_incremental(conn, name, rows)
                print(f"    Snowflake RAW.{name}: {count} yeni satır eklendi (merge)")

            results[name] = {"status": "ok", "rows": count}

        except Exception as e:
            print(f"    HATA: {e}")
            results[name] = {"status": "error", "error": str(e)}

    conn.close()
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["backfill", "incremental"],
        default="incremental",
        help="backfill: 2020'den bugüne (bir kez). incremental: son 2 ay (Actions).",
    )
    args = parser.parse_args()

    print(f"=== Fetch [{args.mode}] — {datetime.now().strftime('%Y-%m-%d %H:%M')} ===\n")
    results = fetch_all(args.mode)
    print(f"\nSonuç: {results}")
