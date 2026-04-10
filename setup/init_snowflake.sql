-- HousingScope Snowflake Kurulum
-- Bu dosya ilk kurulumda bir kez çalıştırılır.
-- Snowflake Worksheets'te açıp "Run All" ile çalıştır.

-- Database ve schema'lar
CREATE DATABASE IF NOT EXISTS HOUSINGSCOPE_DB;
USE DATABASE HOUSINGSCOPE_DB;

CREATE SCHEMA IF NOT EXISTS RAW;
CREATE SCHEMA IF NOT EXISTS STAGING;
CREATE SCHEMA IF NOT EXISTS MART;

-- RAW tabloları (tüm seriler aynı yapı)
USE SCHEMA RAW;

CREATE TABLE IF NOT EXISTS kfe (
    raw_date      VARCHAR,
    raw_value     VARCHAR,
    series_code   VARCHAR,
    loaded_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_year   INTEGER
);

CREATE TABLE IF NOT EXISTS usd_try          LIKE kfe;
CREATE TABLE IF NOT EXISTS konut_faiz       LIKE kfe;
CREATE TABLE IF NOT EXISTS tufe             LIKE kfe;
CREATE TABLE IF NOT EXISTS insaat_maliyet   LIKE kfe;

-- Doğrulama: 5 tablo görünmeli
SHOW TABLES IN SCHEMA RAW;
