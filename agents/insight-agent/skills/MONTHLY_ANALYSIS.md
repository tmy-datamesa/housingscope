# Skill: Monthly Analysis

## Amaç

Aylık EVDS verisinden konut profesyonelleri için net, veri destekli yorum üret.

## Hedefler

- Aylık yorum üretimi
- Net alıcı/satıcı/yatırımcı sinyali

## Girdiler

- `data/processed/dashboard.json` — tüm seriler
- `knowledge/MARKET_CONTEXT.md` — piyasa bağlamı
- `knowledge/INDICATORS.md` — gösterge anlamları
- `MEMORY.md` — önceki kanıtlanmış pattern'lar

## Süreç

### Adım 1: Sayıları Oku
Her seri için son iki ayı karşılaştır:
- KFE: ay/ay değişim (%), yıl/yıl değişim (%)
- TÜFE: son değer, ay/ay değişim
- KFE – TÜFE farkı: pozitif mi (reel artış) negatif mi (reel düşüş)?
- Konut faizi: değişim yönü
- USD/TRY: değişim yönü
- İnşaat maliyeti: değişim yönü

### Adım 2: Sinyal Üret
Her gösterge için yön belirle: ↑ ↓ →

Sinyal matrisi:
| Durum | Alıcı için | Satıcı için | Yatırımcı için |
|-------|-----------|------------|---------------|
| KFE > TÜFE (reel artış) | Acele et | İyi zaman | Pozitif |
| KFE < TÜFE (reel düşüş) | Bekle | Fırsat penceresi kapanıyor | Dikkatli |
| Faiz düşüyor | Kredi avantajı artıyor | Talep artacak | Uyarı: fiyat artabilir |
| Faiz yükseliyor | Maliyetli | Talep zayıflıyor | Negatif |

### Adım 3: Yorum Yaz

Format (`outputs/YYYY-MM_insight.md`):

```markdown
# [AY YIL] Konut Piyasası Görünümü

## Bu Ay Ne Değişti?
[2-3 cümle. Sayı ver. Jargon kullanma.]

## Göstergeler

| Gösterge | Değer | Ay/Ay | Yıl/Yıl | Sinyal |
|----------|-------|-------|---------|--------|
| KFE | ... | ...% | ...% | ↑/↓/→ |
| TÜFE | ... | ...% | - | ↑/↓/→ |
| Reel KFE (KFE-TÜFE) | ... | - | - | ↑/↓/→ |
| Konut Faizi | ...% | ↑/↓/→ | - | - |
| USD/TRY | ... | ...% | - | ↑/↓/→ |
| İnşaat Maliyeti | ... | ...% | - | ↑/↓/→ |

## Alıcı / Satıcı / Yatırımcı Sinyali

**Alıcı:** [1 cümle net sinyal]
**Satıcı:** [1 cümle net sinyal]
**Yatırımcı:** [1 cümle net sinyal]

## Dikkat Edilmesi Gereken

[Bu ay öne çıkan 1-2 risk veya fırsat]
```

### Adım 4: Kalite Kontrolü

Yayınlamadan önce kontrol et:
- [ ] Her claim için bir sayı var mı?
- [ ] "Reel KFE" (KFE–TÜFE) hesaplandı mı?
- [ ] Her üç profil için (alıcı/satıcı/yatırımcı) net sinyal var mı?
- [ ] Jargon yok, sayı var

## Çıktı

`outputs/YYYY-MM_insight.md`

## Kalite Çıtası

- Sayısız "artıyor/azalıyor" ifadesi yasak — her değişim yüzde veya puan olarak verilmeli
- "Piyasa karmaşık" gibi muğlak ifadeler yasak
- Her yorum en fazla 400 kelime
