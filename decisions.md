# Decisions

Mimari kararlar ve gerekçeleri.

---

## [2026-04-10] Veri katmanı: JSON flat file

**Karar:** Veritabanı yok, `data/processed/dashboard.json` düz dosya.
**Neden:** 5-6 seri, aylık güncelleme — SQLite bile fazla karmaşık. JSON okunabilir, versiyonlanabilir, dashboard'a direkt servis edilebilir.
**Değiştirilir mi:** Seri sayısı 20+'ya çıkarsa veya gerçek zamanlı veri eklenirse.

---

## [2026-04-10] Agent framework: agents-egitim (markdown)

**Karar:** Insight agent için kod değil, markdown tabanlı agents-egitim framework.
**Neden:** Agent'ın işi deterministik değil (yorum üretimi) — Claude Code + HEARTBEAT.md yeterli. Kod altyapısı gereksiz karmaşıklık.
**Değiştirilir mi:** Hayır.

---

## [2026-04-10] Dashboard tech: TBD

**Karar:** Next.js veya FastAPI + HTML — henüz kararlaştırılmadı.
**Seçenekler:**
- Next.js + Recharts: Daha güçlü, öğretici, portfolio değeri yüksek
- FastAPI + HTML: LearnMate gibi hızlı prototip, Python ile tutarlı
**Karar noktası:** Pipeline çalışınca, veri formatı netleşince seç.

---

## [2026-04-10] Aylık güncelleme: cron script

**Karar:** `pipeline/run.py` manuel veya cron ile çalışır. Otomatik deploy yok (MVP'de).
**Neden:** EVDS yayın tarihleri düzensiz, manuel tetikleme daha güvenilir başlangıç.
**Değiştirilir mi:** Dashboard Vercel'e taşınırsa GitHub Actions cron eklenebilir.
