"""
Snowflake MART.konut_indicators → Vercel Blob (public JSON)

Kullanım:
    python pipeline/export_to_blob.py
"""

import json
import os
import urllib.request
from datetime import datetime, timezone

import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

BLOB_PATHNAME = "housingscope/konut_indicators.json"
BLOB_UPLOAD_URL = f"https://blob.vercel-storage.com/{BLOB_PATHNAME}"


def snowflake_connect():
    password = os.getenv("SNOWFLAKE_PASSWORD", "")
    auth_params = (
        {"authenticator": "externalbrowser"} if not password else {"password": password}
    )
    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        role=os.getenv("SNOWFLAKE_ROLE"),
        schema="MART",
        **auth_params,
    )


def export():
    print("Exporting MART.konut_indicators → Vercel Blob...")

    conn = snowflake_connect()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT month, series_key, series_label, value "
            "FROM konut_indicators "
            "ORDER BY series_key, month"
        )
        records = [
            {"month": row[0], "series_key": row[1], "series_label": row[2], "value": row[3]}
            for row in cur.fetchall()
        ]
        cur.execute("SELECT MAX(month) FROM konut_indicators")
        latest = cur.fetchone()[0] or datetime.now(timezone.utc).strftime("%Y-%m")
    finally:
        conn.close()

    payload = json.dumps(
        {"meta": {"report_updated": latest}, "records": records},
        ensure_ascii=False,
    ).encode("utf-8")

    token = os.environ["BLOB_READ_WRITE_TOKEN"]
    req = urllib.request.Request(
        BLOB_UPLOAD_URL,
        data=payload,
        method="PUT",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "x-content-type": "application/json",
            "x-access": "public",
        },
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())

    print(f"✓ Uploaded {len(records)} records → {result.get('url', BLOB_UPLOAD_URL)}")
    print(f"  report_updated: {latest}")


if __name__ == "__main__":
    export()
