-- İzmir Konut Birim Fiyatı (TL/m²) — çeyreklik seri
-- Ham tarih formatı: "2020-Q1" → son ay: "2020-03", "2020-06", "2020-09", "2020-12"

CREATE OR REPLACE TABLE STAGING.stg_birimfiyat_izm AS
SELECT
    SPLIT_PART(raw_date, '-', 1)
        || '-' ||
    CASE SPLIT_PART(raw_date, '-', 2)
        WHEN 'Q1' THEN '03'
        WHEN 'Q2' THEN '06'
        WHEN 'Q3' THEN '09'
        WHEN 'Q4' THEN '12'
    END                                            AS month,
    raw_value::FLOAT                               AS value,
    CURRENT_TIMESTAMP                              AS updated_at
FROM RAW.birimfiyat_izm
WHERE raw_value IS NOT NULL
  AND raw_value != ''
ORDER BY month;
