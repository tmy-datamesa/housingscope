-- Konut göstergeleri mart tablosu
-- Tüm staging serileri tek tabloda birleştirilir
-- Dashboard ve Insight Agent bu tabloyu sorgular
--
-- Örnek sorgu:
--   SELECT month, value FROM MART.konut_indicators
--   WHERE series_key = 'kfe_yeni' ORDER BY month;

CREATE OR REPLACE TABLE MART.konut_indicators AS

-- KFE serileri (tarihi + güncel)
SELECT month, 'kfe'            AS series_key, 'Konut Fiyat Endeksi (Genel)'      AS series_label, value FROM STAGING.stg_kfe
UNION ALL
SELECT month, 'kfe_yeni'       AS series_key, 'Yeni Konutlar Fiyat Endeksi'       AS series_label, value FROM STAGING.stg_kfe_yeni
UNION ALL
SELECT month, 'kfe_ikinciel'   AS series_key, 'İkinci El Konutlar Fiyat Endeksi'  AS series_label, value FROM STAGING.stg_kfe_ikinciel
UNION ALL

-- Diğer göstergeler
SELECT month, 'tufe'           AS series_key, 'TÜFE Genel'                        AS series_label, value FROM STAGING.stg_tufe
UNION ALL
SELECT month, 'konut_faiz'     AS series_key, 'Konut Kredisi Faizi (%)'           AS series_label, value FROM STAGING.stg_konut_faiz
UNION ALL
SELECT month, 'usd_try'        AS series_key, 'USD/TRY'                           AS series_label, value FROM STAGING.stg_usd_try
UNION ALL
SELECT month, 'insaat_maliyet'       AS series_key, 'İnşaat Maliyet Endeksi'      AS series_label, value FROM STAGING.stg_insaat_maliyet
UNION ALL

-- Konut satış adetleri
SELECT month, 'konut_satis_toplam'   AS series_key, 'Toplam Konut Satışı (Adet)'  AS series_label, value FROM STAGING.stg_konut_satis_toplam
UNION ALL
SELECT month, 'konut_satis_ipotekli' AS series_key, 'İpotekli Satışlar (Adet)'    AS series_label, value FROM STAGING.stg_konut_satis_ipotekli
UNION ALL
SELECT month, 'konut_satis_ilkel'    AS series_key, 'İlk El Satışlar (Adet)'      AS series_label, value FROM STAGING.stg_konut_satis_ilkel
UNION ALL
SELECT month, 'konut_satis_ikinciel' AS series_key, 'İkinci El Satışlar (Adet)'        AS series_label, value FROM STAGING.stg_konut_satis_ikinciel
UNION ALL

-- Karşılaştırmalı getiri göstergeleri
SELECT month, 'mevduat_faiz'         AS series_key, 'TL Mevduat Faizi -1 Ay (%)'       AS series_label, value FROM STAGING.stg_mevduat_faiz
UNION ALL
SELECT month, 'altin'                AS series_key, 'Külçe Altın Satış Fiyatı (TL/Gr)' AS series_label, value FROM STAGING.stg_altin
UNION ALL

-- Politika faizi ve kira
SELECT month, 'politika_faiz'        AS series_key, 'TCMB Politika Faizi (%)'           AS series_label, value FROM STAGING.stg_politika_faiz
UNION ALL
SELECT month, 'kira_endeksi'         AS series_key, 'Yeni Kiracı Kira Endeksi'          AS series_label, value FROM STAGING.stg_kira_endeksi
UNION ALL

-- Şehir bazlı birim fiyat (TL/m²)
SELECT month, 'birimfiyat_ist'       AS series_key, 'İstanbul Konut Birim Fiyatı (TL/m²)' AS series_label, value FROM STAGING.stg_birimfiyat_ist
UNION ALL
SELECT month, 'birimfiyat_ank'       AS series_key, 'Ankara Konut Birim Fiyatı (TL/m²)'  AS series_label, value FROM STAGING.stg_birimfiyat_ank
UNION ALL
SELECT month, 'birimfiyat_izm'       AS series_key, 'İzmir Konut Birim Fiyatı (TL/m²)'   AS series_label, value FROM STAGING.stg_birimfiyat_izm
UNION ALL

-- Şehir bazlı KFE endeksi
SELECT month, 'kfe_istanbul'         AS series_key, 'İstanbul Konut Fiyat Endeksi'      AS series_label, value FROM STAGING.stg_kfe_istanbul
UNION ALL
SELECT month, 'kfe_ankara'           AS series_key, 'Ankara Konut Fiyat Endeksi'        AS series_label, value FROM STAGING.stg_kfe_ankara
UNION ALL
SELECT month, 'kfe_izmir'            AS series_key, 'İzmir Konut Fiyat Endeksi'         AS series_label, value FROM STAGING.stg_kfe_izmir

ORDER BY series_key, month;
