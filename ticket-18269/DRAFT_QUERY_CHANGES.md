# Draft Query Changes - Ticket 18269

## 🎯 **What to Add to the Existing Query**

Once you find the current query, you'll need to make these specific changes:

---

## 📝 **Change 1: Add Type 1 OEM Keys to Filter**

### **Find this line in the current query:**

```kql
| where Key in ('siteId', 'oemInfo.0.oemName', 'oemInfo.0.oemSiteId', ...)
```

### **Modify to:**

```kql
| where Key in ('siteId', 
               'oemInfo.0.oemName', 
               'oemInfo.0.oemSiteId',
               'oemInfo.1.oemName',      // ← ADD THIS LINE
               'oemInfo.1.oemSiteId',    // ← ADD THIS LINE
               'siteName',
               'address.stateProvince',
               // ... rest of the keys
```

---

## 📝 **Change 2: Add Type 1 Columns to Summarize**

### **Find the summarize block:**

```kql
| summarize 
    siteId = take_anyif(valueMax, Key == 'siteId'),
    oem_name = take_anyif(valueMax, Key == 'oemInfo.0.oemName'),
    oem_siteId = take_anyif(valueMax, Key == 'oemInfo.0.oemSiteId'),
    customer_name = ...,
    ...
by Id
```

### **Modify to:**

```kql
| summarize 
    siteId = take_anyif(valueMax, Key == 'siteId'),
    oem_name = take_anyif(valueMax, Key == 'oemInfo.0.oemName'),
    oem_siteId = take_anyif(valueMax, Key == 'oemInfo.0.oemSiteId'),
    type1_oem_name = take_anyif(valueMax, Key == 'oemInfo.1.oemName'),      // ← ADD THIS LINE
    type1_oem_siteId = take_anyif(valueMax, Key == 'oemInfo.1.oemSiteId'),  // ← ADD THIS LINE
    customer_name = ...,
    ...
by Id
```

---

## 📝 **Change 3A: Add Battery Flag (Simple Method)**

### **Step 1: Add productInfo key to filter**

In the `where Key in (...)` clause, add:

```kql
'productInfo.prodSubType',
```

### **Step 2: Add to summarize**

```kql
prodSubType = take_anyif(valueMax, Key == 'productInfo.prodSubType'),
```

### **Step 3: Add extend after summarize**

After the `| summarize ... by Id` block, add:

```kql
| extend has_battery = case(
    prodSubType in ('HybridInverter', 'BatteryInverter'), 'Yes',
    isnotempty(prodSubType), 'No',
    ''  // Empty if no product info
)
```

---

## 📝 **Change 3B: Add Battery Flag (Accurate Method)** - ADVANCED

This requires checking for actual battery devices in relationships.

### **Add this as a separate `let` statement BEFORE the main query:**

```kql
// Get sites with battery devices
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
        goldAdtPropertyMinMaxLatestViewV2
        | where Key == 'siteId'
        | where actionMax != 'Delete'
        | where ModelId startswith 'dtmi:qcells:site'
        | project siteTwinId = Id, siteId = valueMax
    ) on $left.siteId == $right.siteTwinId
    | distinct siteId
    | extend has_battery = 'Yes';

// Then in your main query, at the end:
| join kind=leftouter (sitesWithBattery) on siteId
| extend has_battery = coalesce(has_battery, 'No')
```

**Recommendation:** Start with **Change 3A (Simple Method)** for now.

---

## 🧪 **Test Query for Site 100003907**

After making changes, test with:

```kql
// YOUR MODIFIED QUERY HERE
| where siteId == "100003907"
```

**Expected Output:**

| siteId | oem_name | oem_siteId | type1_oem_name | type1_oem_siteId | has_battery |
|--------|----------|------------|----------------|------------------|-------------|
| 100003907 | Qcells | 100003907 | Qcells | SSMAK9HTBP | Yes |

---

## 📋 **Complete Example (Minimal)**

Here's a minimal example of what the modified query might look like:

```kql
goldAdtPropertyMinMaxLatestViewV2
| where Key in (
    'siteId',
    'oemInfo.0.oemName',
    'oemInfo.0.oemSiteId',
    'oemInfo.1.oemName',           // ← ADDED
    'oemInfo.1.oemSiteId',         // ← ADDED
    'productInfo.prodSubType',     // ← ADDED for battery flag
    'siteName',
    'address.stateProvince',
    // ... other keys
)
| where actionMax != 'Delete'
| where ModelId startswith 'dtmi:qcells:site'
| summarize 
    siteId = take_anyif(valueMax, Key == 'siteId'),
    oem_name = take_anyif(valueMax, Key == 'oemInfo.0.oemName'),
    oem_siteId = take_anyif(valueMax, Key == 'oemInfo.0.oemSiteId'),
    type1_oem_name = take_anyif(valueMax, Key == 'oemInfo.1.oemName'),        // ← ADDED
    type1_oem_siteId = take_anyif(valueMax, Key == 'oemInfo.1.oemSiteId'),    // ← ADDED
    prodSubType = take_anyif(valueMax, Key == 'productInfo.prodSubType'),     // ← ADDED
    siteName = take_anyif(valueMax, Key == 'siteName'),
    state = take_anyif(valueMax, Key == 'address.stateProvince'),
    // ... other fields
by Id
| extend has_battery = case(
    prodSubType in ('HybridInverter', 'BatteryInverter'), 'Yes',
    isnotempty(prodSubType), 'No',
    ''
)
| project siteId, oem_name, oem_siteId, 
         type1_oem_name, type1_oem_siteId,  // ← ADDED
         has_battery,                        // ← ADDED
         siteName, state
         // ... other fields
```

---

## ✅ **Checklist Before Implementing**

- [ ] Found the current query source
- [ ] Confirmed with Shuai on battery flag logic
- [ ] Tested modified query with site 100003907
- [ ] Verified output matches expected format
- [ ] Updated Power BI report
- [ ] Refreshed dataset
- [ ] Validated in Power BI

---

**Ready to use once you find the current query!** 🚀
