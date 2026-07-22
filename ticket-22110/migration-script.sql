-- =============================================================================
-- Migration: Add program eligibility JSON field to site table
-- Work Item: 22110
-- =============================================================================
ALTER TABLE asset.tb_bas_site
ADD COLUMN IF NOT EXISTS is_program_eligible jsonb;
