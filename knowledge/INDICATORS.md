# Indicators

Her göstergenin ne anlama geldiği ve nasıl yorumlanacağı.

## KFE — Konut Fiyat Endeksi

- **Kaynak:** TÜİK, EVDS seri kodu: `TP.HKFE01`
- **Sıklık:** Aylık (yaklaşık 6-8 hafta gecikmeyle)
- **Ne ölçer:** Türkiye geneli konut satış fiyatları endeksi (2017=100 baz)
- **Nasıl yorumlanır:**
  - KFE > TÜFE → reel fiyat artışı (konut enflasyona karşı koruyor)
  - KFE < TÜFE → reel fiyat düşüşü (konut enflasyonun gerisinde kalıyor)
  - Ay/ay değişim: kısa vadeli ivme
  - Yıl/yıl değişim: trend

## Konut Kredisi Faiz Oranı

- **Kaynak:** TCMB, EVDS seri kodu: `TP.TK.TG.AY`
- **Sıklık:** Aylık
- **Ne ölçer:** Bankacılık sektörü ortalama konut kredisi faiz oranı (%)
- **Nasıl yorumlanır:**
  - Faiz ↓ → kredi erişilebilirliği artar → talep artar → fiyat baskısı (ters korelasyon)
  - Faiz ↑ → aylık taksit yükselir → talep zayıflar → fiyat baskısı azalır
  - Kırılım noktası: %20-25 bandı — bu altında kredi talebi belirgin artıyor

## TÜFE Genel

- **Kaynak:** TÜİK, EVDS seri kodu: `TP.FE.OKTG01`
- **Sıklık:** Aylık
- **Ne ölçer:** Tüketici fiyat enflasyonu, genel endeks
- **Nasıl yorumlanır:**
  - KFE ile karşılaştırılarak reel konut getirisi hesaplanır
  - Düşen enflasyon → kira ve konut reel değerini yükseltir (nominal artış olmadan)

## USD/TRY

- **Kaynak:** TCMB, EVDS seri kodu: `TP.DK.USD.A`
- **Sıklık:** Günlük (aylık ortalama alınır)
- **Ne ölçer:** Türk lirası / Amerikan doları kuru
- **Nasıl yorumlanır:**
  - Dolar bazında konut getirisi hesaplamak için kullanılır
  - TRY değer kaybı → dolar bazında getiri erir
  - Yabancı yatırımcı ve diaspora talebi için proxy

## İnşaat Maliyet Endeksi

- **Kaynak:** TÜİK/TCMB, EVDS seri kodu: `TP.YIEX` (doğrulanacak)
- **Sıklık:** Aylık
- **Ne ölçer:** İnşaat sektörü girdi maliyetleri endeksi
- **Nasıl yorumlanır:**
  - Maliyet > KFE → müteahhit marjı sıkışıyor → yeni arz azalabilir → uzun vadede fiyat baskısı
  - Maliyet < KFE → arz tarafı sağlıklı
