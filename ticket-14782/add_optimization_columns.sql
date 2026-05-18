-- ============================================================================
-- Migration Script: Add Optimization Columns
-- Ticket: ADO #14782
-- Database: assetdb
-- Schema: asset
-- ============================================================================

-- Add optimization_enabled to tb_bas_program_info
ALTER TABLE asset.tb_bas_program_info
ADD COLUMN IF NOT EXISTS optimization_enabled BOOLEAN DEFAULT FALSE;

COMMENT ON COLUMN asset.tb_bas_program_info.optimization_enabled IS
'Boolean flag for optimization';

-- Add optimization_schedule to tb_bas_program_info
ALTER TABLE asset.tb_bas_program_info
ADD COLUMN IF NOT EXISTS optimization_schedule JSONB;

COMMENT ON COLUMN asset.tb_bas_program_info.optimization_schedule IS
'JSONB field for optimization schedule configuration';

-- ============================================================================
-- VERIFICATION
-- ============================================================================

SELECT 'Migration completed successfully!' as status;

SELECT column_name, data_type, column_default
FROM information_schema.columns
WHERE table_schema = 'asset'
  AND table_name = 'tb_bas_program_info'
  AND column_name IN ('optimization_enabled', 'optimization_schedule')
ORDER BY column_name;