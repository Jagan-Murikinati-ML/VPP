# Testing Guide - Postgres Migration

**Ticket:** ADO #12121  
**Database:** assetregistry (DEV)  
**Script:** postgres_migration.sql  

---

## 🎯 WHAT YOU'RE TESTING

Verify that 4 new columns are added correctly to 3 tables:

1. ✅ `asset.tb_bas_program_info.auto_enrollment` (BOOLEAN)
2. ✅ `asset.tb_bas_site.utility_meter_id` (VARCHAR)
3. ✅ `asset.tb_bas_site.utility_meter_serial_number` (VARCHAR)
4. ✅ `asset.tb_opr_program_site_info.site_owner_authorization` (ENUM)

---

## 🔧 PREREQUISITES

### 1. Get Database Password from Jim
- [ ] DM Jim for password
- [ ] Save it securely

### 2. Install Database Tool
- [ ] DBeaver (recommended): https://dbeaver.io/download/
- [ ] OR Azure Data Studio: https://aka.ms/azuredatastudio

### 3. Connection Details
```
Host: assetregistry-us-es-dev-postgre.postgres.database.azure.com
Port: 5432
Database: assetregistry (or postgres - confirm with Jim)
User: esadmin
Password: <from Jim>
SSL Mode: Require
```

---

## 📋 TESTING STEPS

### Step 1: Connect to Database (5 minutes)

**Using DBeaver:**
1. Open DBeaver
2. Click "New Database Connection"
3. Select "PostgreSQL"
4. Enter connection details above
5. Click "Test Connection"
6. If successful, click "Finish"

**Verify Connection:**
```sql
SELECT current_database(), current_user, version();
```

Expected: Should show database name, user, and Postgres version

---

### Step 2: Verify Tables Exist (5 minutes)

**Check if the 3 tables exist:**

```sql
-- List all tables in asset schema
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'asset'
ORDER BY table_name;
```

**Expected tables:**
- ✅ `tb_bas_program_info`
- ✅ `tb_bas_site`
- ✅ `tb_opr_program_site_info`

**If tables don't exist:** Contact Jim/Shaun - wrong database or schema

---

### Step 3: Check Current Table Structure (10 minutes)

**Before running migration, document current columns:**

```sql
-- Check tb_bas_program_info columns
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_schema = 'asset' AND table_name = 'tb_bas_program_info'
ORDER BY ordinal_position;

-- Check tb_bas_site columns
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_schema = 'asset' AND table_name = 'tb_bas_site'
ORDER BY ordinal_position;

-- Check tb_opr_program_site_info columns
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_schema = 'asset' AND table_name = 'tb_opr_program_site_info'
ORDER BY ordinal_position;
```

**Save the output** - you'll compare after migration

---

### Step 4: Run the Migration Script (5 minutes)

1. Open `postgres_migration.sql` in DBeaver
2. Review the script
3. Execute the script (F5 or Execute button)
4. Check for errors

**Expected Output:**
```
ALTER TABLE
ALTER TABLE
ALTER TABLE
CREATE TYPE
ALTER TABLE
```

**If errors occur:**
- Read the error message carefully
- Check if columns already exist
- Verify table names are correct
- Contact me for help

---

### Step 5: Verify Columns Were Added (10 minutes)

**Run the verification queries from the script:**

```sql
-- Verify auto_enrollment
SELECT 
    'tb_bas_program_info' as table_name,
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'asset' 
  AND table_name = 'tb_bas_program_info'
  AND column_name = 'auto_enrollment';
```

**Expected:**
- column_name: `auto_enrollment`
- data_type: `boolean`
- column_default: `false`

```sql
-- Verify utility meter columns
SELECT 
    'tb_bas_site' as table_name,
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'asset' 
  AND table_name = 'tb_bas_site'
  AND column_name IN ('utility_meter_id', 'utility_meter_serial_number');
```

**Expected:** 2 rows
- `utility_meter_id` - character varying
- `utility_meter_serial_number` - character varying

```sql
-- Verify site_owner_authorization
SELECT 
    'tb_opr_program_site_info' as table_name,
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'asset' 
  AND table_name = 'tb_opr_program_site_info'
  AND column_name = 'site_owner_authorization';
```

**Expected:**
- column_name: `site_owner_authorization`
- data_type: `USER-DEFINED` or `site_authorization_status`
- column_default: `'PENDING'::site_authorization_status`

---

### Step 6: Test Data Insertion (10 minutes)

**Test that you can insert data with new columns:**

```sql
-- Test 1: Insert into tb_bas_program_info with auto_enrollment
-- (Adjust column names based on actual table structure)
-- This is just to verify the column works - don't commit if not needed

BEGIN;

-- Example insert (modify based on actual required columns)
-- INSERT INTO asset.tb_bas_program_info (program_id, program_name, auto_enrollment)
-- VALUES ('TEST-001', 'Test Program', TRUE);

-- Verify
-- SELECT * FROM asset.tb_bas_program_info WHERE program_id = 'TEST-001';

ROLLBACK; -- Don't commit test data
```

```sql
-- Test 2: Test ENUM values for site_owner_authorization
BEGIN;

-- Example insert (modify based on actual required columns)
-- INSERT INTO asset.tb_opr_program_site_info (program_id, site_id, site_owner_authorization)
-- VALUES ('TEST-001', 'SITE-001', 'AUTHORIZED');

-- Verify
-- SELECT * FROM asset.tb_opr_program_site_info WHERE program_id = 'TEST-001';

-- Test invalid ENUM value (should fail)
-- INSERT INTO asset.tb_opr_program_site_info (program_id, site_id, site_owner_authorization)
-- VALUES ('TEST-002', 'SITE-002', 'INVALID'); -- Should error

ROLLBACK; -- Don't commit test data
```

---

## ✅ SUCCESS CRITERIA

After testing, you should confirm:

- [ ] All 4 columns exist in their respective tables
- [ ] Data types are correct (BOOLEAN, VARCHAR, ENUM)
- [ ] Default values are set correctly
- [ ] ENUM type accepts valid values (PENDING, AUTHORIZED, DECLINED)
- [ ] ENUM type rejects invalid values
- [ ] No errors during migration
- [ ] Existing data in tables is not affected

---

## 📸 DOCUMENTATION

**Take screenshots of:**
1. Successful migration execution
2. Verification query results showing new columns
3. ENUM type definition

**Save to attach to ADO ticket**

---

## 🆘 TROUBLESHOOTING

### Error: "relation does not exist"
→ Wrong schema or table name. Verify with Jim.

### Error: "column already exists"
→ Migration already run. Check if columns exist. If yes, you're done!

### Error: "type already exists"
→ ENUM type already created. Safe to ignore or use IF NOT EXISTS.

### Error: "permission denied"
→ User doesn't have ALTER TABLE permission. Contact Jim.

---

## 🚀 AFTER SUCCESSFUL TESTING

1. **Document results** in ADO ticket:
   ```
   ✅ Migration tested successfully in DEV
   ✅ All 4 columns added correctly
   ✅ Data types verified
   ✅ ENUM type working as expected
   ✅ Ready for QA/Prod deployment
   
   Attached: postgres_migration.sql
   ```

2. **Attach the SQL script** to ADO ticket

3. **Ask about QA/Prod deployment:**
   ```
   Who handles deployment to QA and Production?
   Should I coordinate with DevOps team?
   ```

---

## 📝 TEST RESULTS TEMPLATE

```
# Test Results - DEV Environment

Date: _______________
Tester: Jagan Murikinati
Database: assetregistry-us-es-dev-postgre

## Results:

✅ tb_bas_program_info.auto_enrollment
   - Type: boolean
   - Default: false
   - Status: SUCCESS

✅ tb_bas_site.utility_meter_id
   - Type: character varying
   - Status: SUCCESS

✅ tb_bas_site.utility_meter_serial_number
   - Type: character varying
   - Status: SUCCESS

✅ tb_opr_program_site_info.site_owner_authorization
   - Type: site_authorization_status (ENUM)
   - Values: PENDING, AUTHORIZED, DECLINED
   - Default: PENDING
   - Status: SUCCESS

## Issues Found:
None

## Ready for QA/Prod:
YES
```

---

**Good luck with testing! Let me know if you encounter any issues!** 🚀

