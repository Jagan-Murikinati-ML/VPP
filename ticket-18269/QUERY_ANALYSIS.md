# getAssetOnboarding Query - Analysis & Required Changes

## 📊 **Current OEM Data Section**

**Lines ~102-110 (the `oem_data` block):**

```kql
let oem_data = goldAdtPropertyMinMaxLatestViewV2
    | where actionMax != 'Delete'
    and ModelId == "dtmi:qcells:site:site;1" 
    and Key in ('oemInfo.0.oemName', 'oemInfo.0.oemSiteId','assetRegistrationInfo.accountNumber')
    | extend oem_name = case(Key == 'oemInfo.0.oemName', valueMax, ""),
             oem_siteId = case(Key == 'oemInfo.0.oemSiteId', valueMax, ""),
             account_number = case(Key == 'assetRegistrationInfo.accountNumber', valueMax, "")
    | summarize oem_name = any(oem_name), oem_siteId = any(oem_siteId), account_number = any(account_number) by Id
    | project siteId = Id, oem_name, oem_siteId, account_number
; //oem_data
```

**Current Output:**
- `oem_name` ← Type 0 (oemInfo.0.oemName)
- `oem_siteId` ← Type 0 (oemInfo.0.oemSiteId)
- `account_number`

---

## ✅ **Required Changes**

### **Change 1: Add Type 1 OEM Keys**

Modify the `where Key in (...)` clause to include Type 1:

```kql
and Key in ('oemInfo.0.oemName', 'oemInfo.0.oemSiteId',
           'oemInfo.1.oemName', 'oemInfo.1.oemSiteId',    // ← ADD THESE
           'assetRegistrationInfo.accountNumber')
```

### **Change 2: Add Type 1 Columns to extend**

Add two new case statements:

```kql
| extend oem_name = case(Key == 'oemInfo.0.oemName', valueMax, ""),
         oem_siteId = case(Key == 'oemInfo.0.oemSiteId', valueMax, ""),
         type1_oem_name = case(Key == 'oemInfo.1.oemName', valueMax, ""),      // ← ADD THIS
         type1_oem_siteId = case(Key == 'oemInfo.1.oemSiteId', valueMax, ""),  // ← ADD THIS
         account_number = case(Key == 'assetRegistrationInfo.accountNumber', valueMax, "")
```

### **Change 3: Add Type 1 Columns to summarize**

```kql
| summarize oem_name = any(oem_name), 
           oem_siteId = any(oem_siteId), 
           type1_oem_name = any(type1_oem_name),        // ← ADD THIS
           type1_oem_siteId = any(type1_oem_siteId),    // ← ADD THIS
           account_number = any(account_number) by Id
```

### **Change 4: Add Type 1 Columns to project**

```kql
| project siteId = Id, 
         oem_name, 
         oem_siteId, 
         type1_oem_name,      // ← ADD THIS
         type1_oem_siteId,    // ← ADD THIS
         account_number
```

### **Change 5: Add Type 1 Columns to final distinct**

In the `result_data` section (around line 120), add the new columns:

```kql
| distinct site_ids,
          oem_siteId,
          oem_name,
          type1_oem_name,      // ← ADD THIS
          type1_oem_siteId,    // ← ADD THIS
          customer_name,
          customer_email,
          ...
```

---

## 🔋 **Add Battery Flag**

### **Option A: Simple Method (Using Product Info)**

The query already has `productInfo_prodSubType` from the `rated_capacity` section!

Just add this in the final `distinct` section:

```kql
| distinct site_ids,
          oem_siteId,
          oem_name,
          type1_oem_name,
          type1_oem_siteId,
          customer_name,
          ...
          tostring(productInfo_prodSubType),
          has_battery = case(                                    // ← ADD THIS
              productInfo_prodSubType in ('HybridInverter', 'BatteryInverter'), 'Yes',
              isnotempty(productInfo_prodSubType), 'No',
              ''
          ),
          account_number,
          ...
```

---

## 📋 **Complete Modified `oem_data` Section**

```kql
//Step 12: Fetch Oem data
let oem_data = goldAdtPropertyMinMaxLatestViewV2
    | where actionMax != 'Delete'
    and ModelId == "dtmi:qcells:site:site;1" 
    and Key in ('oemInfo.0.oemName', 
               'oemInfo.0.oemSiteId',
               'oemInfo.1.oemName',           // ← ADDED
               'oemInfo.1.oemSiteId',         // ← ADDED
               'assetRegistrationInfo.accountNumber')
    | extend oem_name = case(Key == 'oemInfo.0.oemName', valueMax, ""),
             oem_siteId = case(Key == 'oemInfo.0.oemSiteId', valueMax, ""),
             type1_oem_name = case(Key == 'oemInfo.1.oemName', valueMax, ""),      // ← ADDED
             type1_oem_siteId = case(Key == 'oemInfo.1.oemSiteId', valueMax, ""),  // ← ADDED
             account_number = case(Key == 'assetRegistrationInfo.accountNumber', valueMax, "")
    | summarize oem_name = any(oem_name), 
               oem_siteId = any(oem_siteId),
               type1_oem_name = any(type1_oem_name),        // ← ADDED
               type1_oem_siteId = any(type1_oem_siteId),    // ← ADDED
               account_number = any(account_number) by Id
    | project siteId = Id, 
             oem_name, 
             oem_siteId,
             type1_oem_name,      // ← ADDED
             type1_oem_siteId,    // ← ADDED
             account_number
; //oem_data
```

---

## ❓ **Questions for Shuai**

Before implementing, confirm with Shuai:

```
Hi Shuai,

I got the getAssetOnboarding query from Zahm. 

For ticket 18269, I need to add Type 1 OEM columns. 

Current column names for Type 0:
- oem_name
- oem_siteId

What should I name the Type 1 columns?
Option A: type1_oem_name, type1_oem_siteId
Option B: oem_name_type1, oem_siteId_type1
Option C: secondary_oem_name, secondary_oem_siteId
Option D: Something else?

Also:
- Battery flag column name: has_battery or battery_flag?
- Battery detection: Use productInfo_prodSubType (already in query) or check device relationships?

Thanks!
```

---

## 🧪 **Test Query**

After making changes, test with:

```kql
getAssetOnboarding()
| where site_ids == "100003907"
```

**Expected Output:**
| site_ids | oem_name | oem_siteId | type1_oem_name | type1_oem_siteId | has_battery |
|----------|----------|------------|----------------|------------------|-------------|
| 100003907 | Qcells | 100003907 | Qcells | SSMAK9HTBP | Yes |

---

## ✅ **Summary of Changes**

**Total Lines to Modify:** ~3 sections

1. **`oem_data` section** (~10 lines modified)
2. **`result_data` distinct** (~2 lines added)
3. **Battery flag logic** (~5 lines added)

**Total: ~17 lines of changes**

Very manageable! 🚀
