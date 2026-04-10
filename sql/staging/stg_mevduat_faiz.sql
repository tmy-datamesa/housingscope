-- 1 Aya Kadar Vadeli TL Mevduat Faizi — haftalık seri → aylık ortalama (TP.TRY.MT01)
-- Ham tarih formatı: "DD-MM-YYYY"

CREATE OR REPLACE TABLE STAGING.stg_mevduat_faiz AS
SELECT
    SPLIT_PART(raw_date, '-', 3)
        || '-' ||
    SPLIT_PART(raw_date, '-', 2)               AS month,
    AVG(raw_value::FLOAT)                       AS value,
    CURRENT_TIMESTAMP                           AS updated_at
FROM RAW.mevduat_faiz
WHERE raw_value IS NOT NULL
  AND raw_value != ''
GROUP BY month
ORDER BY month;
