# Insight Agent Heartbeat

## Zamanlama

**Her ayın 3'ü** — EVDS genellikle ayın 1-2'sinde günceller, 3'ü güvenli tampon.

Ön koşul: Snowflake MART.konut_indicators bu ayın verisiyle güncellenmiş olmalı.

## Her Döngü

### 1. Context Oku
- `SELECT MAX(month) FROM MART.konut_indicators` → son veri tarihi nedir?
- `knowledge/MARKET_CONTEXT.md` → piyasa bağlamı
- `knowledge/INDICATORS.md` → gösterge anlamları
- `MEMORY.md` → kanıtlanmış pattern'lar

### 2. Durum Değerlendir
- MART'taki son ay bu ay mı? → pipeline çalışmış
- Güncellenmemişse: pipeline çalışmamış, insana bildir, bekle
- Güncellendiyse: analiz başla

### 3. MONTHLY_ANALYSIS Skill'ini Çalıştır

`skills/MONTHLY_ANALYSIS.md` adımlarını izle.

### 4. Logla
- `outputs/YYYY-MM_insight.md` yaz
- `MEMORY.md` güncelle (yeni pattern varsa)

## Haftalık Review Yok

Bu agent aylık çalışır. Aylık review = döngünün kendisi.

## Escalation

İnsana bildir:
- MART tablosundaki son veri ayın 5'ine kadar bu ayı göstermiyorsa (pipeline çalışmamış)
- Herhangi bir seride veri kesintisi varsa (null / boş değerler)
- Göstergeler birbiriyle çelişkili sinyal veriyorsa (örn: fiyat artıyor ama satış düşüyor)
