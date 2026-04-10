-- USD/TRY — günlük seri → aylık ortalama
-- Ham tarih formatı: "17-07-2023" (DD-MM-YYYY)
-- Hafta sonu / tatil günleri null olarak gelir — filtrelenir

CREATE OR REPLACE TABLE STAGING.stg_usd_try AS
SELECT
    -- "17-07-2023" → "2023-07"
    SPLIT_PART(raw_date, '-', 3)
        || '-' ||
    SPLIT_PART(raw_date, '-', 2)               AS month,
    AVG(raw_value::FLOAT)                       AS value,   -- günlük → aylık ortalama
    CURRENT_TIMESTAMP                           AS updated_at
FROM RAW.usd_try
WHERE raw_value IS NOT NULL
  AND raw_value != ''
GROUP BY month
ORDER BY month;
