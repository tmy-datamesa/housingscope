-- Konut Kredisi Faiz Oranı — haftalık seri → aylık ortalama
-- Ham tarih formatı: "03-01-2020" (DD-MM-YYYY)

CREATE OR REPLACE TABLE STAGING.stg_konut_faiz AS
SELECT
    -- "03-01-2020" → "2020-01"
    SPLIT_PART(raw_date, '-', 3)
        || '-' ||
    SPLIT_PART(raw_date, '-', 2)               AS month,
    AVG(raw_value::FLOAT)                       AS value,   -- haftalık → aylık ortalama
    CURRENT_TIMESTAMP                           AS updated_at
FROM RAW.konut_faiz
WHERE raw_value IS NOT NULL
  AND raw_value != ''
GROUP BY month
ORDER BY month;
