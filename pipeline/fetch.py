"""
EVDS API'den ham veri çeker ve data/raw/ altına JSON olarak kaydeder.

Kullanım:
    python pipeline/fetch.py
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EVDS_API_KEY")
BASE_URL = "https://evds2.tcmb.gov.tr/service/evds"

# İzlenecek seriler: {dosya_adı: seri_kodu}
SERIES = {
    "kfe": "TP.HKFE01",          # Konut Fiyat Endeksi
    "konut_faiz": "TP.TK.TG.AY", # Konut kredisi faiz oranı
    "tufe": "TP.FE.OKTG01",      # TÜFE genel
    "usd_try": "TP.DK.USD.A",    # USD/TRY
    "insaat_maliyet": "TP.YIEX", # İnşaat maliyet endeksi
}

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


def fetch_series(series_code: str, start_date: str = "01-01-2020") -> dict:
    """Tek bir seriyi EVDS'den çeker."""
    params = {
        "series": series_code,
        "startDate": start_date,
        "endDate": datetime.now().strftime("%d-%m-%Y"),
        "type": "json",
        "key": API_KEY,
    }
    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_all():
    """Tüm serileri çeker ve data/raw/ altına kaydeder."""
    if not API_KEY:
        raise ValueError("EVDS_API_KEY bulunamadı. .env dosyasını kontrol et.")

    results = {}
    for name, code in SERIES.items():
        print(f"Çekiliyor: {name} ({code})...")
        try:
            data = fetch_series(code)
            output_path = RAW_DIR / f"{name}.json"
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  ✓ {output_path}")
            results[name] = {"status": "ok", "code": code}
        except Exception as e:
            print(f"  ✗ Hata: {e}")
            results[name] = {"status": "error", "error": str(e)}

    return results


if __name__ == "__main__":
    results = fetch_all()
    print("\nSonuç:", results)
