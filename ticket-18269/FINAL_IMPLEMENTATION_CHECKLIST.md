# Final Implementation Checklist - Ticket 18269

## ✅ **All Requirements Confirmed**

1. ✅ **Function:** `getAssetOnboarding` (from Zahm)
2. ✅ **Column Names:** type0_oem_name, type0_oem_siteId, type1_oem_name, type1_oem_siteId, has_battery (from Shuai)
3. ✅ **Battery Detection:** Relationship-based using goldAdtTwinEventsLatestV2 + goldAdtAllRelationshipsLatestView (from Juan Pablo)
4. ✅ **Test Site:** 100003907 (has Type 1: Qcells/SSMAK9HTBP, has battery)

---

## 📋 **Implementation Steps**

### ☐ **Step 1: Backup Current Function** (5 min)

```kql
.show function getAssetOnboarding
```

Copy the output and save to a file (in case you need to rollback).

---

### ☐ **Step 2: Update the Function** (30 min)

The complete modified query is in `MODIFIED_QUERY.kql`. You need to make **3 changes**:

#### **Change 1: Update oem_data section (~line 102-110)**

**BEFORE:**
```kql
| extend oem_name = case(Key == 'oemInfo.0.oemName', valueMax, ""),
         oem_siteId = case(Key == 'oemInfo.0.oemSiteId', valueMax, ""),
```

**AFTER:**
```kql
| extend type0_oem_name = case(Key == 'oemInfo.0.oemName', valueMax, ""),
         type0_oem_siteId = case(Key == 'oemInfo.0.oemSiteId', valueMax, ""),
         type1_oem_name = case(Key == 'oemInfo.1.oemName', valueMax, ""),
         type1_oem_siteId = case(Key == 'oemInfo.1.oemSiteId', valueMax, ""),
```

**Also update** the `summarize` and `project` to use the new names.

---

#### **Change 2: Add Battery Detection (~before oem_data, around line 100)**

Add this NEW section:

```kql
// Step 11.5: Detect sites with batteries (Juan Pablo's method)
let sitesWithBattery = 
    goldAdtTwinEventsLatestV2
    | where Action != 'Delete'
    | where ModelId startswith 'dtmi:qcells:device:batt'
    | project batteryTwinId = TwinId
    | join kind=inner (
        goldAdtAllRelationshipsLatestView
        | where Action != 'Delete'
        | project siteId = Source, batteryTwinId = Target
    ) on batteryTwinId
    | join kind=inner (
        goldAdtTwinEventsLatestV2
        | where Action != 'Delete'
        | where ModelId startswith 'dtmi:qcells:site'
        | project siteTwinId = TwinId
    ) on $left.siteId == $right.siteTwinId
    | distinct siteId
    | extend has_battery = 'Yes'
; // sitesWithBattery
```

---

#### **Change 3: Update result_data section (~line 120-145)**

**BEFORE:**
```kql
| distinct site_ids,
          oem_siteId,
          oem_name,
```

**AFTER:**
```kql
| join kind = leftouter sitesWithBattery on $left.site_ids == $right.siteId
| distinct site_ids,
          type0_oem_siteId,    // RENAMED
          type0_oem_name,      // RENAMED
          type1_oem_name,      // ADDED
          type1_oem_siteId,    // ADDED
```

**And add near the end (before account_number):**
```kql
has_battery = coalesce(has_battery, 'No'),  // ADDED
```

---

### ☐ **Step 3: Test with Site 100003907** (10 min)

```kql
getAssetOnboarding()
| where site_ids == "100003907"
| project site_ids, type0_oem_name, type0_oem_siteId, 
         type1_oem_name, type1_oem_siteId, has_battery
```

**Expected Output:**
```
site_ids: 100003907
type0_oem_name: Qcells
type0_oem_siteId: 100003907
type1_oem_name: Qcells
type1_oem_siteId: SSMAK9HTBP
has_battery: Yes
```

---

### ☐ **Step 4: Test with Multiple Scenarios** (10 min)

```kql
// Test sites WITHOUT Type 1
getAssetOnboarding()
| where site_ids in ("100001549", "100011910")
| project site_ids, type0_oem_name, type1_oem_name, type1_oem_siteId, has_battery

// Expected: type1_oem_name and type1_oem_siteId should be empty
```

```kql
// Test sites WITH battery
getAssetOnboarding()
| where has_battery == 'Yes'
| take 10
| project site_ids, type0_oem_name, type1_oem_name, has_battery
```

---

### ☐ **Step 5: Refresh Power BI Report** (15 min)

1. Open Power BI report in Fabric
2. Go to **Settings** → **Refresh** or **Transform Data**
3. Verify new columns appear:
   - type0_oem_name
   - type0_oem_siteId
   - type1_oem_name
   - type1_oem_siteId
   - has_battery

---

### ☐ **Step 6: Validate in Report** (10 min)

1. Export report to CSV or check in Power BI
2. Filter for site `100003907`
3. Verify all 5 new/renamed columns are correct
4. Check a few other sites

---

### ☐ **Step 7: Reply to Shuai** (2 min)

Use the message from `SHUAI_RESPONSE.md`:

```
Hi Shuai,

Confirmed! I've updated the report with the requested columns:
- type0_oem_name, type0_oem_siteId (renamed from oem_name, oem_siteId)
- type1_oem_name, type1_oem_siteId (new)
- has_battery (new)

Tested with site 100003907 - all working correctly!

The report has been refreshed.

Thanks!
```

---

## 🧪 **Testing Summary**

| Test Case | Expected Result | Status |
|-----------|----------------|--------|
| Site 100003907 | Type 1 = Qcells/SSMAK9HTBP, battery = Yes | ☐ |
| Sites without Type 1 | Type 1 columns empty | ☐ |
| Sites with battery | has_battery = Yes | ☐ |
| Sites without battery | has_battery = No | ☐ |
| Report refresh | New columns appear | ☐ |

---

## 📁 **Reference Files**

- `MODIFIED_QUERY.kql` - Complete code with all changes
- `BATTERY_FLAG_TEST.kql` - Battery detection test queries
- `SHUAI_RESPONSE.md` - Message to send to Shuai
- `JUAN_PABLO_SOLUTION.md` - Battery detection explanation

---

## ⚠️ **Important Notes**

1. **Backup first!** Save current function before modifying
2. **Column rename impact:** Power BI visuals using old column names (oem_name, oem_siteId) will need updating
3. **Testing is critical:** Verify with multiple sites before considering complete

---

## ✅ **Completion Checklist**

- [ ] Function backed up
- [ ] Code changes applied
- [ ] Site 100003907 tested
- [ ] Multiple scenarios tested
- [ ] Power BI report refreshed
- [ ] Report validated
- [ ] Shuai notified
- [ ] Ticket marked complete

---

**Total Estimated Time: ~90 minutes**

**Ready to implement!** 🚀
