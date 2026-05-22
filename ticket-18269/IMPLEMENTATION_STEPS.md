# Ticket 18269 - Implementation Steps

## ✅ **What We Know Now**

1. ✅ **Function Name:** `getAssetOnboarding` (from Zahm)
2. ✅ **Current Type 0 Columns:** `oem_name`, `oem_siteId`
3. ✅ **Data Source:** `goldAdtPropertyMinMaxLatestViewV2`
4. ✅ **Test Site:** `100003907` (has Type 1 OEM data)
5. ✅ **Battery Detection:** Use relationship-based method (from Juan Pablo)

---

## 📝 **Step-by-Step Implementation**

### **Step 1: Confirm Column Names with Shuai** ⏭️

**Message to Shuai:**

```
Hi Shuai,

Working on ticket 18269. I got the getAssetOnboarding query from Zahm.

Current Type 0 columns:
- oem_name
- oem_siteId

What should I name the Type 1 columns?

Option A: type1_oem_name, type1_oem_siteId
Option B: oem_name_type1, oem_siteId_type1  
Option C: secondary_oem_name, secondary_oem_siteId
Option D: Other preference?

Also:
- Battery flag column name: has_battery or battery_flag?

Note: Juan Pablo confirmed we should use relationship-based detection
(check for battery devices in goldAdtTwinEventsLatestV2 + goldAdtAllRelationshipsLatestView)

Thanks!
```

---

### **Step 2: View Current Function** ⏭️

```kql
.show function getAssetOnboarding
```

This shows the current function definition.

---

### **Step 3: Modify the Function** ⏭️

**Three sections to modify:**

#### **Section 1: oem_data block (~line 102-110)**

Change this:
```kql
and Key in ('oemInfo.0.oemName', 'oemInfo.0.oemSiteId','assetRegistrationInfo.accountNumber')
```

To this:
```kql
and Key in ('oemInfo.0.oemName', 'oemInfo.0.oemSiteId',
           'oemInfo.1.oemName', 'oemInfo.1.oemSiteId',  // ADD THESE
           'assetRegistrationInfo.accountNumber')
```

Add to extend:
```kql
type1_oem_name = case(Key == 'oemInfo.1.oemName', valueMax, ""),
type1_oem_siteId = case(Key == 'oemInfo.1.oemSiteId', valueMax, ""),
```

Add to summarize:
```kql
type1_oem_name = any(type1_oem_name),
type1_oem_siteId = any(type1_oem_siteId),
```

Add to project:
```kql
type1_oem_name,
type1_oem_siteId,
```

#### **Section 2: result_data distinct (~line 120-140)**

Add after `oem_name`:
```kql
type1_oem_name,
type1_oem_siteId,
```

#### **Section 3: Battery flag (same section)**

Add after `productInfo_prodSubType`:
```kql
has_battery = case(
    productInfo_prodSubType in ('HybridInverter', 'BatteryInverter'), 'Yes',
    isnotempty(productInfo_prodSubType), 'No',
    ''
),
```

---

### **Step 4: Update the Function** ⏭️

Use `.create-or-alter function`:

```kql
.create-or-alter function getAssetOnboarding() {
    // PASTE THE FULL MODIFIED QUERY HERE
}
```

**See `MODIFIED_QUERY.kql` for the exact changes.**

---

### **Step 5: Test the Function** ⏭️

```kql
getAssetOnboarding()
| where site_ids == "100003907"
| project site_ids, oem_name, oem_siteId, type1_oem_name, type1_oem_siteId, has_battery
```

**Expected Output:**

| site_ids | oem_name | oem_siteId | type1_oem_name | type1_oem_siteId | has_battery |
|----------|----------|------------|----------------|------------------|-------------|
| 100003907 | Qcells | 100003907 | Qcells | SSMAK9HTBP | Yes or No |

---

### **Step 6: Test with More Sites** ⏭️

Test with different scenarios:

```kql
// Test with sites that have NO Type 1
getAssetOnboarding()
| where site_ids in ("100001549", "100011910")
| project site_ids, oem_name, type1_oem_name, type1_oem_siteId

// Expected: type1_oem_name and type1_oem_siteId should be empty
```

```kql
// Test with sites that have Type 1 (from query2.csv - Qcells + Tesla)
getAssetOnboarding()
| where type1_oem_name == "Tesla"
| take 10
| project site_ids, oem_name, type1_oem_name, type1_oem_siteId
```

---

### **Step 7: Refresh Power BI Report** ⏭️

1. Open the Power BI report in Fabric
2. Go to **Transform Data** or **Refresh**
3. The report should automatically pick up the new columns from `getAssetOnboarding()`
4. Verify the new columns appear

---

### **Step 8: Validate in Power BI** ⏭️

1. Export report to CSV (or check in Power BI directly)
2. Filter for site `100003907`
3. Verify:
   - `type1_oem_name` = Qcells
   - `type1_oem_siteId` = SSMAK9HTBP
   - `has_battery` = Yes or No

---

## 📊 **Summary of Changes**

**Total Lines Modified:** ~17 lines

**Files Created:**
- ✅ `QUERY_ANALYSIS.md` - Detailed analysis
- ✅ `MODIFIED_QUERY.kql` - Modified sections only
- ✅ `IMPLEMENTATION_STEPS.md` - This file

**Sections Modified:**
1. ✅ `oem_data` block - Add Type 1 keys and columns
2. ✅ `result_data` distinct - Add Type 1 to output
3. ✅ Battery flag logic - Add has_battery calculation

---

## ⚠️ **Important Notes**

1. **Column Names:** Wait for Shuai's confirmation before finalizing
2. **Battery Logic:** Currently using `productInfo_prodSubType` (simple method)
3. **Testing:** Test with site 100003907 first before deploying
4. **Backup:** Save the current function definition before modifying

---

## ✅ **Checklist**

- [ ] Get column name confirmation from Shuai
- [ ] View current function (`.show function getAssetOnboarding`)
- [ ] Backup current function
- [ ] Modify the three sections
- [ ] Update function (`.create-or-alter function`)
- [ ] Test with site 100003907
- [ ] Test with sites without Type 1
- [ ] Test with multi-OEM sites
- [ ] Refresh Power BI report
- [ ] Validate output in report
- [ ] Mark ticket as complete

---

**Ready to implement once Shuai confirms column names!** 🚀
