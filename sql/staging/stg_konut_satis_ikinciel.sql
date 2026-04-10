-- İkinci El Konut Satışları — aylık seri (TP.AKONUTSAT4.TOPLAM)
-- Ham tarih formatı: "2020-1" → normalize: "2020-01"

CREATE OR REPLACE TABLE STAGING.stg_konut_satis_ikinciel AS
SELECT
    SPLIT_PART(raw_date, '-', 1)
        || '-' ||
    LPAD(SPLIT_PART(raw_date, '-', 2), 2, '0')   AS month,
    raw_value::FLOAT                               AS value,
    CURRENT_TIMESTAMP                              AS updated_at
FROM RAW.konut_satis_ikinciel
WHERE raw_value IS NOT NULL
  AND raw_value != ''
ORDER BY month;
