# Insight Agent Heartbeat

## Zamanlama

**Her ayın 3'ü** — EVDS genellikle ayın 1-2'sinde günceller, 3'ü güvenli tampon.

Ön koşul: `data/processed/dashboard.json` bu ayın tarihiyle güncellenmiş olmalı.

## Her Döngü

### 1. Context Oku
- `data/processed/dashboard.json` → güncel seri verileri
- `knowledge/MARKET_CONTEXT.md` → piyasa bağlamı
- `knowledge/INDICATORS.md` → gösterge anlamları
- `journal/` → önceki ay bulguları
- `MEMORY.md` → kanıtlanmış pattern'lar

### 2. Durum Değerlendir
- `dashboard.json` bu ay güncellendi mi? → `updated_at` kontrol et
- Güncellenmemişse: pipeline çalışmamış, önce `python pipeline/run.py` çalıştır, insana bildir
- Güncellendiyse: analiz başla

### 3. MONTHLY_ANALYSIS Skill'ini Çalıştır

`skills/MONTHLY_ANALYSIS.md` adımlarını izle.

### 4. Logla
- `outputs/YYYY-MM_insight.md` yaz
- `journal/YYYY-MM-DD_HHMM.md` giriş yaz
- `MEMORY.md` güncelle (yeni pattern varsa)

## Haftalık Review Yok

Bu agent aylık çalışır. Aylık review = döngünün kendisi.

## Escalation

İnsana bildir:
- `dashboard.json` ayın 5'ine kadar güncellenmemişse (EVDS yayın gecikmesi)
- Herhangi bir seride veri kesintisi varsa (null / boş değerler)
- Göstergeler birbiriyle çelişkili sinyal veriyorsa (örn: fiyat artıyor ama satış düşüyor)
