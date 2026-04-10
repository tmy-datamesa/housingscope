"""
Tam ELT pipeline: EVDS → Snowflake RAW → STAGING → MART

Kullanım:
    python pipeline/run.py --mode backfill      # İlk kurulum (bir kez)
    python pipeline/run.py --mode incremental   # Aylık güncelleme (Actions)
"""

import argparse
import os
from glob import glob
from pathlib import Path

import snowflake.connector
from dotenv import load_dotenv

from fetch import fetch_all

load_dotenv()

SQL_STAGING_DIR = Path(__file__).parent.parent / "sql" / "staging"
SQL_MART_FILE   = Path(__file__).parent.parent / "sql" / "mart" / "fct_konut_indicators.sql"


def snowflake_connect() -> snowflake.connector.SnowflakeConnection:
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
        **auth_params,
    )


def run_sql_file(conn, path: Path):
    sql = path.read_text(encoding="utf-8")
    conn.cursor().execute(sql)
    print(f"    ✓ {path.name}")


def run(mode: str):
    print(f"=== HousingScope ELT Pipeline [{mode}] ===\n")

    # 1. Extract + Load → Snowflake RAW
    print("1/3  Extract + Load (EVDS → Snowflake RAW)...")
    fetch_results = fetch_all(mode)
    errors = [k for k, v in fetch_results.items() if v["status"] == "error"]
    if errors:
        print(f"\n  ⚠ Hatalı seriler: {errors}")
        print("  Transform yine de devam ediyor (mevcut RAW verisiyle)...\n")

    # 2. Transform → STAGING
    print("\n2/3  Transform (RAW → STAGING)...")
    conn = snowflake_connect()
    for sql_file in sorted(SQL_STAGING_DIR.glob("*.sql")):
        run_sql_file(conn, sql_file)

    # 3. Transform → MART
    print("\n3/3  Transform (STAGING → MART)...")
    run_sql_file(conn, SQL_MART_FILE)

    conn.close()
    print("\n✓ Pipeline tamamlandı.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["backfill", "incremental"],
        default="incremental",
    )
    args = parser.parse_args()
    run(args.mode)
