-- ============================================================================
-- Migration Script: Add VPP Site Metadata Columns
-- Ticket: ADO #12121
-- Author: Jagan Murikinati
-- Date: 2026-03-18
-- Database: assetdb
-- Schema: asset
-- ============================================================================

-- STEP 1: Add auto_enrollment to tb_bas_program_info
ALTER TABLE asset.tb_bas_program_info 
ADD COLUMN IF NOT EXISTS auto_enrollment BOOLEAN DEFAULT FALSE;

COMMENT ON COLUMN asset.tb_bas_program_info.auto_enrollment IS 
'Indicates whether the program automatically enrolls sites. Default: FALSE';

-- STEP 2: Add utility meter columns to tb_bas_site
ALTER TABLE asset.tb_bas_site 
ADD COLUMN IF NOT EXISTS utility_meter_id CHARACTER VARYING(255);

COMMENT ON COLUMN asset.tb_bas_site.utility_meter_id IS 
'Utility meter identifier for the site';

ALTER TABLE asset.tb_bas_site 
ADD COLUMN IF NOT EXISTS utility_meter_serial_number CHARACTER VARYING(255);

COMMENT ON COLUMN asset.tb_bas_site.utility_meter_serial_number IS 
'Serial number of the utility meter at the site';

-- STEP 3: Create ENUM type for site_owner_authorization
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'site_authorization_status') THEN
        CREATE TYPE asset.site_authorization_status AS ENUM ('PENDING', 'AUTHORIZED', 'DECLINED');
    END IF;
END $$;

COMMENT ON TYPE asset.site_authorization_status IS 
'Authorization status for site owner participation in VPP programs';

-- STEP 4: Add site_owner_authorization to tb_opr_program_site_info
ALTER TABLE asset.tb_opr_program_site_info 
ADD COLUMN IF NOT EXISTS site_owner_authorization asset.site_authorization_status DEFAULT 'PENDING';

COMMENT ON COLUMN asset.tb_opr_program_site_info.site_owner_authorization IS 
'Site owner authorization status for program participation. Values: PENDING, AUTHORIZED, DECLINED. Default: PENDING';

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

SELECT 'Migration completed successfully!' as status;

SELECT table_name, column_name, data_type, column_default 
FROM information_schema.columns 
WHERE table_schema = 'asset' 
  AND table_name IN ('tb_bas_program_info', 'tb_bas_site', 'tb_opr_program_site_info')
  AND column_name IN ('auto_enrollment', 'utility_meter_id', 'utility_meter_serial_number', 'site_owner_authorization')
ORDER BY table_name, column_name;
