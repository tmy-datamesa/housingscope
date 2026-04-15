-- TCMB Politika Faizi (1 Haftalık Repo) — aylık seri
-- Ham tarih formatı: "2020-1" → normalize: "2020-01"

CREATE OR REPLACE TABLE STAGING.stg_politika_faiz AS
SELECT
    SPLIT_PART(raw_date, '-', 1)
        || '-' ||
    LPAD(SPLIT_PART(raw_date, '-', 2), 2, '0')   AS month,
    raw_value::FLOAT                               AS value,
    CURRENT_TIMESTAMP                              AS updated_at
FROM RAW.politika_faiz
WHERE raw_value IS NOT NULL
  AND raw_value != ''
ORDER BY month;
