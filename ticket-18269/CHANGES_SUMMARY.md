# Ticket 18269 - Changes Summary

## 📋 **File Modified:**
`original_getAssetOnboarding.kql`

---

## ✅ **Changes Made:**

### **Change 1: Added Type 1 OEM Keys to Step 12 (Lines 121-123)**

**Before:**
```kql
and Key in ('oemInfo.0.oemName', 'oemInfo.0.oemSiteId','assetRegistrationInfo.accountNumber')
```

**After:**
```kql
and Key in ('oemInfo.0.oemName', 'oemInfo.0.oemSiteId', 
           'oemInfo.1.oemName', 'oemInfo.1.oemSiteId',
           'assetRegistrationInfo.accountNumber')
```

---

### **Change 2: Added Type 1 OEM Columns to Extract (Lines 126-127)**

**Added:**
```kql
type1_oem_name = case(Key == 'oemInfo.1.oemName', valueMax, ""),
type1_oem_siteId = case(Key == 'oemInfo.1.oemSiteId', valueMax, ""),
```

---

### **Change 3: Added Type 1 OEM to Summarize (Lines 131-132)**

**Added:**
```kql
type1_oem_name = any(type1_oem_name),
type1_oem_siteId = any(type1_oem_siteId),
```

---

### **Change 4: Added Type 1 OEM to Project (Line 134)**

**Before:**
```kql
| project siteId = Id, oem_name, oem_siteId, account_number
```

**After:**
```kql
| project siteId = Id, oem_name, oem_siteId, type1_oem_name, type1_oem_siteId, account_number
```

---

### **Change 5: Added Type 1 OEM Columns to Result (Lines 150-151)**

**Added to distinct clause:**
```kql
type1_oem_siteId,
type1_oem_name,
```

---

### **Change 6: Added Battery Flag (Lines 170-175)**

**Added extend clause:**
```kql
// Add battery flag based on product subtype
| extend has_battery = case(
    productInfo_prodSubType in ('HybridInverter', 'BatteryInverter'), 'Yes',
    isnotempty(productInfo_prodSubType), 'No',
    ''  // Empty if product info not available
)
```

---

## 🎯 **New Columns Added to Report:**

1. **`type1_oem_name`** - OEM name for Type 1 asset (e.g., second OEM for battery)
2. **`type1_oem_siteId`** - OEM site ID for Type 1 asset
3. **`has_battery`** - Battery flag ('Yes', 'No', or empty if unknown)

---

## 🧪 **How to Test:**

Run the modified function and check site `100003907`:

```kql
getAssetOnboarding()
| where site_ids == "100003907"
```

**Expected Output:**

| Field | Expected Value |
|-------|---------------|
| site_ids | 100003907 |
| oem_name | Qcells |
| oem_siteId | 100003907 |
| **type1_oem_name** | **Qcells** ✅ |
| **type1_oem_siteId** | **SSMAK9HTBP** ✅ |
| **has_battery** | **Yes** ✅ |

---

## 📝 **Next Steps:**

1. ✅ Deploy the modified function to Fabric
2. ✅ Test with site `100003907`
3. ✅ Refresh the Power BI report
4. ✅ Verify new columns appear in the report

---

## 🔄 **Rollback (if needed):**

If there are any issues, the original file is saved as `original_getAssetOnboarding.kql.backup` (if you created a backup).

To rollback, simply replace with the original version that didn't have Type 1 OEM fields.

---

**Status:** ✅ READY TO DEPLOY
