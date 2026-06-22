# Deployment Guide - Ticket 20086
## Add Utility Information to Asset Onboarding Report

---

## 📋 **Pre-Deployment Checklist**

- [x] Code reviewed and tested locally
- [x] Confirmed data source with Juan Pablo Culebro
- [x] Test queries prepared
- [ ] Tested in DEV environment
- [ ] Validated in Asset Onboarding Dashboard
- [ ] Approved for QA deployment
- [ ] Approved for PROD deployment

---

## 🚀 **Deployment Steps**

### **Step 1: Access Fabric Workspace**

1. Navigate to: [Fabric Workspace](https://app.fabric.microsoft.com/groups/09c5e73c-a820-4100-aef5-d774ac0395f6/)
2. Go to **Functions** section
3. Locate function: `getAssetOnboarding()`

---

### **Step 2: Backup Current Function**

**IMPORTANT:** Before making changes, save the current version!

```kql
// Copy the entire current function code to a file
// Name it: getAssetOnboarding_backup_YYYYMMDD.kql
```

---

### **Step 3: Deploy Modified Function**

1. Open the function `getAssetOnboarding()` for editing
2. Copy the contents from `original_code.kql` (in ticket-20086 folder)
3. Paste and replace the entire function
4. **Save** the function

---

### **Step 4: Run Test Queries**

Execute the test queries from `test_utility_fields.kql`:

#### **Test 1: Verify utility keys exist**
```kql
goldAdtPropertyMinMaxLatestViewV2
| where Key in ('utilityName', 'utilityAccountNumber')
| where actionMax != 'Delete'
| summarize 
    total_sites_with_utility_name = countif(Key == 'utilityName'),
    total_sites_with_utility_account = countif(Key == 'utilityAccountNumber')
```

**Expected:** Should return counts > 0 for both fields

---

#### **Test 2: Run modified function**
```kql
getAssetOnboarding()
| take 100
| project site_ids, customer_name, utility_company, utility_service_account_number
```

**Expected:** 
- Function executes without errors
- New columns `utility_company` and `utility_service_account_number` are visible
- Some rows have populated utility data

---

#### **Test 3: Coverage statistics**
```kql
getAssetOnboarding()
| summarize 
    total_sites = count(),
    sites_with_utility_company = countif(isnotempty(utility_company)),
    sites_with_utility_account = countif(isnotempty(utility_service_account_number))
| extend 
    pct_with_utility_company = round(100.0 * sites_with_utility_company / total_sites, 2),
    pct_with_utility_account = round(100.0 * sites_with_utility_account / total_sites, 2)
```

**Expected:** Get coverage percentages to understand data availability

---

### **Step 5: Validate in Dashboard**

1. Navigate to: [Asset Onboarding Dashboard](https://app.fabric.microsoft.com/groups/09c5e73c-a820-4100-aef5-d774ac0395f6/reports/b140bc27-f819-4b74-8ce6-d60b49cc583b/7c30b3e609720e59d7be?experience=fabric-developer)
2. **Refresh** the data source
3. **Verify** the two new columns appear:
   - Utility Company
   - Utility Service Account Number
4. **Check** sample data to ensure values are populated correctly

---

## 🔍 **What Changed?**

### **1. Added Step 12A - Utility Data Extraction**
- **Location:** Lines 155-165 in `original_code.kql`
- **Purpose:** Extract `utilityName` and `utilityAccountNumber` from Asset Registry
- **Pattern:** Follows same pattern as Step 12 (OEM data)

### **2. Added Join in Step 13**
- **Location:** Line 176 in `original_code.kql`
- **Change:** Added `| join kind = leftouter utility_data on $left.site_ids == $right.siteId`

### **3. Added Fields to Output**
- **Location:** Lines 201-202 in `original_code.kql`
- **Fields Added:**
  - `utility_company`
  - `utility_service_account_number`

---

## ⚠️ **Rollback Plan**

If any issues occur:

1. **Stop** immediately
2. **Restore** from backup:
   ```kql
   // Paste the backup function code saved in Step 2
   ```
3. **Save** and verify dashboard works again
4. **Investigate** the issue before attempting re-deployment

---

## 📊 **Expected Results**

After deployment, the Asset Onboarding report will show:

| Field Name | Source | Example Value |
|-----------|--------|---------------|
| `utility_company` | `goldAdtPropertyMinMaxLatestViewV2.utilityName` | "PG&E", "Southern California Edison", etc. |
| `utility_service_account_number` | `goldAdtPropertyMinMaxLatestViewV2.utilityAccountNumber` | "12345678", "ACC-9876543", etc. |

**Note:** Some sites may have empty values if utility info is not populated in Asset Registry.

---

## 📞 **Contacts for Issues**

- **Juan Pablo Culebro** - Data source/Kusto expert
- **Sanjeev Lakkaraju** - Team lead
- **Naveen Siddalingaswamy** - Business validation

---

## ✅ **Post-Deployment Validation**

- [ ] Function executes without errors
- [ ] New columns visible in dashboard
- [ ] Sample data matches expectations
- [ ] No performance degradation
- [ ] Existing columns unaffected
- [ ] Stakeholders notified of completion
- [ ] Ticket 20086 updated with deployment notes
