-- ============================================
-- Migration Script: assetdb Schema Updates
-- Work Item: 23041
-- Description: Create device_info table and load validated
--              battery/PV sizing data
-- ============================================

BEGIN;

CREATE TABLE IF NOT EXISTS asset.device_info (
    site_id integer NOT NULL,
    battery_power_rating numeric,
    battery_energy_rating numeric,
    pv_system_size numeric
);

COMMIT;

-- ============================================
-- Data load
-- Run this script with psql from the directory containing
-- "Validated battery and PV size_as of_0728.csv", e.g.:
--   psql "host=... port=5432 dbname=assetdb user=esadmin sslmode=require" -f device_info_migration.sql
-- \copy is a psql client-side command and cannot run inside BEGIN/COMMIT
-- via -f in the same transaction as DDL above, so it is issued separately below.
-- ============================================

\copy asset.device_info (site_id, battery_power_rating, battery_energy_rating, pv_system_size) FROM 'Validated battery and PV size_as of_0728.csv' WITH (FORMAT csv, HEADER true)

-- ============================================
-- End of Script
-- ============================================


so you must run psql from inside the folder containing the CSV (or edit the path in the script to an absolute one for that environment).

