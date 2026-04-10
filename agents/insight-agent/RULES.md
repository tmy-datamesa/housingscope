# Insight Agent Rules

## Yapabilir

- Snowflake MART.konut_indicators sorgulamak (read-only)
- `knowledge/` okumak
- `MEMORY.md` güncellemek
- `outputs/` altına yorum yazmak

## Yapamaz

- Snowflake'teki herhangi bir tabloyu düzenlemek
- `knowledge/` dosyalarını doğrudan düzenlemek (değişiklik önerisi yazar)
- İnsan onayı olmadan dışarı yayınlamak
- Pipeline çalıştırmak (insana devreder)

## Handoff Kuralları

- MART'ta bu ayın verisi yoksa → insana "pipeline'ı çalıştır" ilet, bekle
- Veri eksikse → mevcut verilerle çalış, eksiği yorumda belirt
- Göstergeler çelişkili sinyal veriyorsa → insana escalate et, yorum üretme
