# Skill: Monthly Analysis

## Amaç

Aylık EVDS verisinden konut profesyonelleri için net, veri destekli yorum üret.

## Hedefler

- Aylık yorum üretimi
- Net alıcı/satıcı/yatırımcı sinyali

## Girdiler

- Snowflake `MART.konut_indicators` — 13 seri, (month, series_key, value) formatı
- `knowledge/MARKET_CONTEXT.md` — piyasa bağlamı
- `knowledge/INDICATORS.md` — gösterge anlamları
- `MEMORY.md` — önceki kanıtlanmış pattern'lar

## Süreç

### Adım 1: Sayıları Oku

Son iki ayı karşılaştır (her seri için):

**Fiyat grubu:**
- kfe: ay/ay değişim (%), yıl/yıl değişim (%)
- kfe_yeni vs kfe_ikinciel: fark var mı? (yeni > eski = arz baskısı)

**Enflasyon bağlamı:**
- tufe: son değer, ay/ay değişim
- KFE – TÜFE farkı: pozitif mi (reel artış) negatif mi (reel düşüş)?
- insaat_maliyet (ÜFE): KFE ile karşılaştır (maliyet > fiyat = arz sıkışması)

**Erişilebilirlik:**
- konut_faiz: değişim yönü (kredi maliyeti)
- mevduat_faiz: konut faizine yakın mı? (park etmek mi almak mı?)
- usd_try: dolar bazında konut değeri nereye gidiyor?

**Piyasa aktivitesi:**
- konut_satis_toplam: hacim artıyor mu azalıyor mu?
- konut_satis_ipotekli / konut_satis_toplam: ipotekli oran (faize duyarlılık proxy)
- konut_satis_ilkel vs konut_satis_ikinciel: piyasa sağlığı

**Getiri karşılaştırması:**
- altin: aynı dönemde altın ne yaptı? (konut rakibi)

### Adım 2: Sinyal Üret

Her gösterge için yön belirle: ↑ ↓ →

Sinyal matrisi:
| Durum | Alıcı için | Satıcı için | Yatırımcı için |
|-------|-----------|------------|---------------|
| KFE > TÜFE (reel artış) | Acele et | İyi zaman | Pozitif |
| KFE < TÜFE (reel düşüş) | Bekle | Fırsat penceresi kapanıyor | Dikkatli |
| Faiz düşüyor | Kredi avantajı artıyor | Talep artacak | Uyarı: fiyat artabilir |
| Faiz yükseliyor | Maliyetli | Talep zayıflıyor | Negatif |
| Satış hacmi artıyor | Talep güçlü | Güçlü piyasa | Likidite var |
| İpotekli oran düşüyor | Faiz yük ağır | Peşin talep var | Dikkatli |

### Adım 3: Yorum Yaz

Format (`outputs/YYYY-MM_insight.md`):

```markdown
# [AY YIL] Konut Piyasası Görünümü

## Bu Ay Ne Değişti?
[2-3 cümle. Sayı ver. Jargon kullanma.]

## Göstergeler

| Gösterge | Değer | Ay/Ay | Yıl/Yıl | Sinyal |
|----------|-------|-------|---------|--------|
| KFE (Genel) | ... | ...% | ...% | ↑/↓/→ |
| KFE (Yeni) | ... | ...% | - | ↑/↓/→ |
| KFE (İkinci El) | ... | ...% | - | ↑/↓/→ |
| TÜFE | ... | ...% | - | ↑/↓/→ |
| Reel KFE (KFE-TÜFE) | ... | - | - | ↑/↓/→ |
| Konut Faizi | ...% | ↑/↓/→ | - | - |
| Mevduat Faizi | ...% | ↑/↓/→ | - | - |
| USD/TRY | ... | ...% | - | ↑/↓/→ |
| İnşaat Maliyeti (ÜFE) | ... | ...% | - | ↑/↓/→ |
| Toplam Satış | ... adet | ...% | - | ↑/↓/→ |
| İpotekli Satış Oranı | ...% | - | - | ↑/↓/→ |
| Altın (TL/Gr) | ... | ...% | - | ↑/↓/→ |

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
- [ ] Yeni vs ikinci el fiyat farkı yorumlandı mı?
- [ ] Satış hacmi ve ipotekli oran yorumlandı mı?
- [ ] Her üç profil için (alıcı/satıcı/yatırımcı) net sinyal var mı?
- [ ] Jargon yok, sayı var

## Çıktı

`outputs/YYYY-MM_insight.md`

## Kalite Çıtası

- Sayısız "artıyor/azalıyor" ifadesi yasak — her değişim yüzde veya puan olarak verilmeli
- "Piyasa karmaşık" gibi muğlak ifadeler yasak
- Her yorum en fazla 500 kelime
