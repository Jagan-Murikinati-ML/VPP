-- ============================================
-- Migration Script: assetdb Schema Updates
-- Description: Add new columns and status
-- ============================================

BEGIN;

-- 1. Add customer_opt_out column to tb_bas_site
ALTER TABLE asset.tb_bas_site
ADD COLUMN IF NOT EXISTS customer_opt_out BOOLEAN;

-- 2. Add target_removal_date column to tb_program_site_enrollment_status
ALTER TABLE asset.tb_program_site_enrollment_status
ADD COLUMN IF NOT EXISTS target_removal_date TIMESTAMP WITH TIME ZONE;

-- 3. Insert new statuses into tb_vpp_enrollment_status
INSERT INTO asset.tb_vpp_enrollment_status (
    status_code,
    status_name,
    description,
    display_order,
    is_active
)
VALUES (
    'WITHDRAWAL_FAILED',
    'Withdrawal Failed',
    'Indicates withdrawal process failed',
    8,
    true
),
(
    'WITHDRAWN',
    'Withdrawn',
    'Indicates withdrawn',
    9,
    true
)
ON CONFLICT (status_code) DO NOTHING;

COMMIT;

-- ============================================
-- End of Script
-- ============================================