# Indicators

Her göstergenin ne anlama geldiği ve nasıl yorumlanacağı.
Snowflake MART.konut_indicators'da `series_key` değerleri ile eşleşir.

---

## Fiyat Grubu

### kfe — Konut Fiyat Endeksi (Genel)
- **EVDS Kodu:** `TP.KFE.TR`
- **Sıklık:** Aylık (~6-8 hafta gecikmeyle)
- **Ne ölçer:** Türkiye geneli konut satış fiyatları endeksi (2017=100 baz)
- **Nasıl yorumlanır:**
  - KFE > TÜFE → reel fiyat artışı (konut enflasyona karşı koruyor)
  - KFE < TÜFE → reel fiyat düşüşü (konut enflasyonun gerisinde kalıyor)

### kfe_yeni — Yeni Konutlar Fiyat Endeksi
- **EVDS Kodu:** `TP.YKFE.TR`
- **Sıklık:** Aylık
- **Ne ölçer:** Sadece yeni konutlar (ilk el) fiyat endeksi
- **Nasıl yorumlanır:**
  - kfe_yeni > kfe_ikinciel → yeni konut arzı pahalılaşıyor (inşaat maliyeti baskısı)
  - kfe_yeni < kfe_ikinciel → ikinci el piyasası daha sıcak

### kfe_ikinciel — İkinci El Konutlar Fiyat Endeksi
- **EVDS Kodu:** `TP.YOKFEND.TR`
- **Sıklık:** Aylık
- **Ne ölçer:** Sadece ikinci el konutlar fiyat endeksi
- **Nasıl yorumlanır:**
  - Genel KFE'den ayrışma var mı? → piyasa segmentasyonu sinyali

---

## Enflasyon Bağlamı

### tufe — TÜFE Genel
- **EVDS Kodu:** `TP.TUKFIY2025.GENEL`
- **Sıklık:** Aylık
- **Ne ölçer:** Tüketici fiyat enflasyonu, genel endeks
- **Nasıl yorumlanır:**
  - KFE ile karşılaştırılarak reel konut getirisi hesaplanır
  - reel KFE = KFE ay/ay % − TÜFE ay/ay %

### insaat_maliyet — İnşaat Maliyet Endeksi (ÜFE Proxy)
- **EVDS Kodu:** `TP.TUFE1YI.T1`
- **Sıklık:** Aylık
- **Ne ölçer:** Yurt İçi Üretici Fiyat Endeksi (genel) — inşaat girdi maliyeti proxy
- **Not:** EVDS'de ayrı bir İnşaat Maliyet Endeksi yok. YİÜFE en iyi proxy.
- **Nasıl yorumlanır:**
  - insaat_maliyet > KFE → müteahhit marjı sıkışıyor → yeni arz azalabilir → uzun vadede fiyat baskısı
  - insaat_maliyet < KFE → arz tarafı sağlıklı

---

## Erişilebilirlik

### konut_faiz — Konut Kredisi Faizi
- **EVDS Kodu:** `TP.KTF12` (haftalık akım, aylık ortalamaya çevrilir)
- **Sıklık:** Haftalık → aylık ortalama
- **Ne ölçer:** Bankacılık sektörü yeni konut kredisi faiz oranı (%)
- **Nasıl yorumlanır:**
  - Faiz ↓ → kredi erişilebilirliği artar → talep artar → fiyat baskısı
  - Faiz ↑ → aylık taksit yükselir → talep zayıflar
  - mevduat_faiz ile karşılaştır: konut faizi > mevduat faizi → kredi yükü ağır

### mevduat_faiz — TL Mevduat Faizi (1 Ay)
- **EVDS Kodu:** `TP.TRY.MT01` (haftalık, aylık ortalamaya çevrilir)
- **Sıklık:** Haftalık → aylık ortalama
- **Ne ölçer:** 1 aya kadar vadeli TL mevduat faizi (%)
- **Nasıl yorumlanır:**
  - mevduat_faiz ↑ → "bankada tutmak" alternatifi güçleniyor → konut talebi azalabilir
  - Yatırımcı için: konut reel getirisi vs mevduat karşılaştırması

### usd_try — USD/TRY
- **EVDS Kodu:** `TP.DK.USD.A` (günlük, aylık ortalamaya çevrilir)
- **Sıklık:** Günlük → aylık ortalama
- **Ne ölçer:** TL/USD kuru
- **Nasıl yorumlanır:**
  - Dolar bazında konut getirisi: KFE % / USD % − 1
  - TRY değer kaybı → dolar bazında getiri erir
  - Yabancı yatırımcı ve diaspora talebi için proxy

---

## Piyasa Aktivitesi

### konut_satis_toplam — Toplam Konut Satış Adedi
- **EVDS Kodu:** `TP.AKONUTSAT1.KTRTOPLAM`
- **Sıklık:** Aylık
- **Ne ölçer:** Türkiye geneli aylık toplam konut satış adedi
- **Nasıl yorumlanır:**
  - Hacim ↑ + fiyat ↑ → güçlü talep
  - Hacim ↓ + fiyat ↑ → likidite azalıyor, fiyat tutunuyor

### konut_satis_ipotekli — İpotekli Konut Satışları
- **EVDS Kodu:** `TP.AKONUTSAT2.KTRTOPLAM`
- **Sıklık:** Aylık
- **Ne ölçer:** Banka kredisiyle yapılan konut satışları
- **Nasıl yorumlanır:**
  - ipotekli / toplam oranı → piyasanın faize duyarlılığı
  - Oran düşüyorsa → alıcılar peşin alıyor (faiz yükü çok ağır veya sermaye bol)

### konut_satis_ilkel — İlk El Konut Satışları
- **EVDS Kodu:** `TP.AKONUTSAT3.KTRTOPLAM`
- **Sıklık:** Aylık
- **Ne ölçer:** Müteahhitten / projeden satışlar
- **Nasıl yorumlanır:**
  - ilk el ↑ → yeni arz piyasaya giriyor, inşaat sektörü aktif

### konut_satis_ikinciel — İkinci El Konut Satışları
- **EVDS Kodu:** `TP.AKONUTSAT4.KTRTOPLAM`
- **Sıklık:** Aylık
- **Ne ölçer:** Mevcut konutların el değiştirmesi
- **Nasıl yorumlanır:**
  - ikinci el ↑ → mevcut sahipler satıyor (talep var) veya fiyat realizasyonu

---

## Getiri Karşılaştırması

### altin — Külçe Altın Satış Fiyatı
- **EVDS Kodu:** `TP.MK.KUL.YTL`
- **Sıklık:** Aylık
- **Ne ölçer:** TCMB külçe altın satış fiyatı (TL/gram)
- **Nasıl yorumlanır:**
  - Konut ile rakip enflasyon koruması
  - KFE % vs altın % karşılaştırması → hangi varlık daha iyi korudu?
