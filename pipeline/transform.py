"""
data/raw/ altındaki ham EVDS JSON'larını dashboard formatına dönüştürür.
Çıktı: data/processed/dashboard.json

Kullanım:
    python pipeline/transform.py
"""

import json
from datetime import datetime
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
SNAPSHOTS_DIR = Path("data/snapshots")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)


def parse_evds_series(raw: dict) -> list[dict]:
    """EVDS JSON yanıtından [{date, value}] listesi çıkarır."""
    items = raw.get("items", [])
    result = []
    for item in items:
        date = item.get("Tarih") or item.get("date")
        # EVDS seriye göre farklı alan adları kullanabiliyor — ilk dolu değeri al
        value = None
        for k, v in item.items():
            if k not in ("Tarih", "date", "UNIXTIME") and v not in (None, ""):
                try:
                    value = float(v)
                    break
                except (ValueError, TypeError):
                    continue
        if date and value is not None:
            result.append({"date": date, "value": value})
    return result


def transform_all() -> dict:
    """Tüm raw serileri işler ve tek dashboard JSON'ı üretir."""
    series_names = {
        "kfe": "Konut Fiyat Endeksi",
        "konut_faiz": "Konut Kredisi Faizi (%)",
        "tufe": "TÜFE Genel",
        "usd_try": "USD/TRY",
        "insaat_maliyet": "İnşaat Maliyet Endeksi",
    }

    dashboard = {
        "updated_at": datetime.now().strftime("%Y-%m-%d"),
        "series": {},
    }

    for key, label in series_names.items():
        raw_path = RAW_DIR / f"{key}.json"
        if not raw_path.exists():
            print(f"  ⚠ Atlandı (raw yok): {key}")
            continue
        with open(raw_path, encoding="utf-8") as f:
            raw = json.load(f)
        points = parse_evds_series(raw)
        dashboard["series"][key] = {"label": label, "data": points}
        print(f"  ✓ {key}: {len(points)} nokta")

    # Processed
    processed_path = PROCESSED_DIR / "dashboard.json"
    with open(processed_path, "w", encoding="utf-8") as f:
        json.dump(dashboard, f, ensure_ascii=False, indent=2)
    print(f"\nProcessed: {processed_path}")

    # Snapshot
    month = datetime.now().strftime("%Y-%m")
    snapshot_path = SNAPSHOTS_DIR / f"{month}.json"
    with open(snapshot_path, "w", encoding="utf-8") as f:
        json.dump(dashboard, f, ensure_ascii=False, indent=2)
    print(f"Snapshot: {snapshot_path}")

    return dashboard


if __name__ == "__main__":
    transform_all()
