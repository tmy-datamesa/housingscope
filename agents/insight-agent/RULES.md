# Insight Agent Rules

## Yapabilir

- `data/processed/dashboard.json` okumak
- `knowledge/` okumak
- `journal/` okumak ve yazmak
- `MEMORY.md` güncellemek
- `outputs/` altına yorum yazmak

## Yapamaz

- `data/raw/` veya `data/processed/` düzenlemek
- `knowledge/` dosyalarını doğrudan düzenlemek
- İnsan onayı olmadan dışarı yayınlamak
- Pipeline çalıştırmak (insana devreder)

## Handoff Kuralları

- `dashboard.json` güncel değilse → insana "pipeline'ı çalıştır" ilet, bekle
- Veri eksikse → mevcut verilerle çalış, eksiği yorumda belirt
- Göstergeler çelişkili sinyal veriyorsa → insana escalate et, yorum üretme
