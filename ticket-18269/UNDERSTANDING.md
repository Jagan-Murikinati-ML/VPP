# Ticket 18269 - Understanding & Implementation Plan

## 🎯 **Ticket Requirements**

The Asset Onboarding Fabric report needs two additions:

1. **Add Type 1 Asset OEM Information**
   - Current: Report shows `oem_name` and `oem_siteId` for **Type 0** asset only
   - Required: Add `oem_name` and `oem_siteId` for **Type 1** asset

2. **Add Battery Flag**
   - Show whether the site has batteries or not

---

## 📊 **Understanding Type 0 vs Type 1 Assets**

### **Definition:**
- **Type 0 = `oemInfo.0`** (First OEM - typically solar/inverter OEM)
- **Type 1 = `oemInfo.1`** (Second OEM - typically battery OEM, if different)

### **Why Multiple OEMs?**

Some sites have **different manufacturers** for different components:

**Scenario 1: Single OEM (Tesla)**
- Solar inverter: Tesla
- Battery: Tesla
- Result: Only `oemInfo.0` populated (both are same)

**Scenario 2: Multiple OEMs (Enphase + Qcells)**
- Solar inverter: Enphase → `oemInfo.0.oemName = "Enphase"`, `oemInfo.0.oemSiteId = "12345"`
- Battery: Qcells → `oemInfo.1.oemName = "Qcells"`, `oemInfo.1.oemSiteId = "67890"`

**Scenario 3: Multiple OEMs (SolarEdge + Tesla)**
- Solar inverter: SolarEdge → `oemInfo.0.oemName = "SolarEdge"`
- Battery: Tesla → `oemInfo.1.oemName = "Tesla"`

---

## 🔍 **Asset Registry Tables (per Juan Pablo)**

The Asset Registry uses these 3 core gold tables:

1. **`goldAdtPropertyMinMaxLatestViewV2`** ← Properties of twins
   - Columns: `Id`, `Key`, `ModelId`, `valueMax`, `actionMax`, etc.
   - Keys include:
     - `oemInfo.0.oemName`, `oemInfo.0.oemSiteId`
     - `oemInfo.1.oemName`, `oemInfo.1.oemSiteId`
     - `oemInfo.2.oemName`, `oemInfo.2.oemSiteId`
     - etc.

2. **`goldAdtAllRelationshipsLatestView`** ← Relationships between twins
   - Shows which devices are connected to which sites
   - Columns: `Source`, `Target`, `Name`, `Action`

3. **`goldAdtTwinEventsLatestV2`** ← Twin existence
   - Shows if a twin is created or deleted
   - Columns: `TwinId`, `ModelId`, `Action`

---

## 📋 **Current Report Structure (data.csv)**

Current fields include:
- `site_ids` (internal site ID)
- `oem_siteId` (currently showing only oemInfo.0.oemSiteId)
- `oem_name` (currently showing only oemInfo.0.oemName)
- Customer info, address, state
- Product info: `productInfo_prodType`, `productInfo_prodSubType`
- `wMaxRtg` (battery capacity in Watts)
- `system_size_kw`
- Status: `system_status_1h_online`, `last_data_timestamp`

---

## ✅ **What We Need to Add**

### **1. Type 1 Asset OEM Information**

Add these columns:
- `type1_oem_name` (from `oemInfo.1.oemName`)
- `type1_oem_siteId` (from `oemInfo.1.oemSiteId`)

### **2. Battery Flag**

Add column:
- `has_battery` (boolean or "Yes"/"No")

**Battery Detection Logic Options:**

**Option A:** Check `productInfo_prodSubType`
```kql
has_battery = prodSubType in ('HybridInverter', 'BatteryInverter')
```

**Option B:** Check `wMaxRtg` (battery capacity)
```kql
has_battery = wMaxRtg > 0
```

**Option C:** Check for battery device in relationships (most accurate)
```kql
// Check if site has a battery device connected
has_battery = exists battery device with ModelId startswith 'dtmi:qcells:device:batt'
```

**Recommendation:** Use **Option C** (check for actual battery device) as it's most accurate based on Asset Registry data.

---

## 🧪 **Testing Plan**

### **Step 1: Find Test Sites**

We need to find:
1. Site with **only Type 0** (e.g., Qcells solar only)
2. Site with **Type 0 AND Type 1** (e.g., Enphase solar + Tesla battery)
3. Site with **battery** (e.g., Tesla Powerwall)
4. Site **without battery** (e.g., Qcells solar only)

### **Step 2: Query for Test Sites**

```kql
// Find sites with both oemInfo.0 and oemInfo.1
goldAdtPropertyMinMaxLatestViewV2
| where Key in ('oemInfo.0.oemName', 'oemInfo.1.oemName')
| where actionMax != 'Delete'
| summarize 
    type0_oem = take_anyif(valueMax, Key == 'oemInfo.0.oemName'),
    type1_oem = take_anyif(valueMax, Key == 'oemInfo.1.oemName')
by Id
| where isnotnull(type1_oem)  // Only sites with Type 1
| take 10
```

### **Step 3: Compare Current vs Expected**

For each test site:
1. Check current report output (data.csv)
2. Query Asset Registry for oemInfo.0 and oemInfo.1
3. Verify battery flag logic
4. Document expected output

---

## 📝 **Next Steps**

1. ✅ Understand the ticket requirements
2. ✅ Understand Asset Registry structure
3. 🔄 Find test sites with Type 1 OEM data
4. 🔄 Query test sites and compare with current report
5. 🔄 Ask Shuai for clarification on expected output (if needed)
6. 🔄 Write KQL query to add Type 1 OEM fields
7. 🔄 Implement battery flag logic
8. 🔄 Test and validate

---

**Status:** Ready to find test sites and validate understanding 🚀
