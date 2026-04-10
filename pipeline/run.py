"""
Tam pipeline: EVDS'den çek → dönüştür → dashboard.json güncelle.

Kullanım:
    python pipeline/run.py
"""

from fetch import fetch_all
from transform import transform_all


def run():
    print("=== HousingScope Pipeline ===\n")

    print("1/2 Veri çekiliyor...")
    fetch_results = fetch_all()

    errors = [k for k, v in fetch_results.items() if v["status"] == "error"]
    if errors:
        print(f"\n⚠ Hatalı seriler: {errors}")
        print("Transform yine de çalışıyor (mevcut raw dosyalarıyla)...\n")

    print("\n2/2 Dönüştürülüyor...")
    transform_all()

    print("\n✓ Pipeline tamamlandı.")


if __name__ == "__main__":
    run()
