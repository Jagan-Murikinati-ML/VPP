-- ============================================================================
-- Migration Script: Add Baseline Optimization Columns
-- Author: Jagan Murikinati
-- Ticket: ADO #14782
-- Database: assetdb
-- Schema: asset
-- ============================================================================

-- Add baseline_opt_enabled to tb_bas_program_info
ALTER TABLE asset.tb_bas_program_info
ADD COLUMN IF NOT EXISTS baseline_opt_enabled BOOLEAN DEFAULT FALSE;

COMMENT ON COLUMN asset.tb_bas_program_info.baseline_opt_enabled IS
'Boolean flag for baseline optimization';

-- Add baseline_opt_schedule to tb_bas_program_info
ALTER TABLE asset.tb_bas_program_info
ADD COLUMN IF NOT EXISTS baseline_opt_schedule JSONB;

COMMENT ON COLUMN asset.tb_bas_program_info.baseline_opt_schedule IS
'JSONB field for baseline optimization schedule configuration';

-- ============================================================================
-- VERIFICATION
-- ============================================================================

SELECT 'Migration completed successfully!' as status;

SELECT column_name, data_type, column_default
FROM information_schema.columns
WHERE table_schema = 'asset'
  AND table_name = 'tb_bas_program_info'
  AND column_name IN ('baseline_opt_enabled', 'baseline_opt_schedule')
ORDER BY column_name;
