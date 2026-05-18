# V1 vs Juan's Test Function - Detailed Comparison

**Purpose:** Understand Juan's optimizations and identify why it's still slow (5-7s in PROD)

---

## 🔍 **KEY OPTIMIZATIONS JUAN MADE**

### **Optimization 1: User Mapping - Nested Subqueries**

**V1 Approach (4 separate joins):**
```kusto
let site_ids_from_user = materialize(
    silverUserEvents 
    | where user_id == inputUserId
    | join kind=inner (goldUserGroupToUserMapping | ...) on ...
    | join kind=inner (goldUserGroupToResourceGroupMapping | ...) on ...
    | join kind=inner (goldResourceGroupToSiteMapping | ...) on ...
    | join kind=inner (ValidPropertyViewV2 | ...) on ...
    | distinct site_ids
);
```

**Juan's Approach (Nested subqueries):**
```kusto
let site_ids_from_user = 
    goldAdtTwinEventsLatestV2
    | where TwinId in (
        goldResourceGroupToSiteMapping 
        | where resource_group_id in (
            goldUserGroupToResourceGroupMapping 
            | where user_group_id in (
                goldUserGroupToUserMapping 
                | where user_ids == inputUserId ...
                | project user_group_id
            ) ...
            | project resource_group_ids
        ) ...
        | project site_ids
    ) and Action != 'Delete'
    | summarize make_set(TwinId)
```

**Differences:**
- ✅ Eliminates `silverUserEvents` table (not needed)
- ✅ Uses nested `in` operators instead of explicit joins
- ✅ Uses `goldAdtTwinEventsLatestV2` instead of `ValidPropertyViewV2`
- ⚠️ **Potential Issue:** Nested `in` operators can be slow with large datasets

**Estimated Impact:** Unclear - could be faster or slower depending on data volume

---

### **Optimization 2: Eliminated GetSiteProperties() Helper**

**V1 Approach:**
```kusto
let goldAdtPropertySites = GetSiteProperties(paginatedSiteIdsList);
```
**Time:** ~800ms (fetches 50+ properties via complex helper function)

**Juan's Approach:**
```kusto
let goldAdtPropertySites_new = 
    materialize(
        goldAdtPropertyMinMaxLatestViewV2
        | where Id in (paginatedSiteIdsList)
            and (Key startswith "oemInfo" and Key endswith "oemName"
                or Key in (dynamic(['address.stateProvince','address.zipPostalCode',
                                   'address.location.timeZone','siteName'])))
        | summarize
            state = take_anyif(valueMax, Key == 'address.stateProvince'),
            zipCode = take_anyif(valueMax, Key == 'address.zipPostalCode'),
            timezone = take_anyif(valueMax, Key == 'address.location.timeZone'),
            siteName = take_anyif(valueMax, Key == 'siteName'),
            (_, oem) = arg_max(...)
        by siteId = Id
    )
```

**Differences:**
- ✅ Fetches ONLY needed properties (5 fields instead of 50+)
- ✅ Single direct query instead of helper function
- ✅ Uses `take_anyif()` for efficient extraction
- ✅ Smart OEM selection with `arg_max()`

**Estimated Impact:** **-400 to -500ms** ✅ Major improvement!

---

### **Optimization 3: Eliminated GetRealtionshipConnectedIds() Helper**

**V1 Approach:**
```kusto
let connectedIds = materialize(GetRealtionshipConnectedIds(paginatedSiteIdsList));
```
**Time:** ~100-200ms

**Juan's Approach:**
```kusto
let relatedDevices = 
    materialize(
        goldAdtAllRelationshipsLatestView
        | where Action != 'Delete' 
            and Source in (paginatedSiteIdsList) 
            and Name in ("hasDevice","hasSystemInfo")
        | project siteId = Source, deviceId = Target, Name
    )
```

**Differences:**
- ✅ Direct query instead of helper function
- ✅ Fetches ONLY needed relationship types
- ✅ More explicit and readable

**Estimated Impact:** **-50 to -100ms** ✅ Minor improvement

---

### **Optimization 4: Consolidated Device Data Queries**

**V1 Approach (Battery Capacity):**
```kusto
let rated_capacity = goldAdtPropertyDevices
    | join kind=inner (connectedIds) on ...
    | join kind=inner goldAdtPropertyMinMaxLatestViewV2 on ...
    | where Key == 'productInfo.prodSubType' and valueMax in (...)
    | extend rated_capacity = case(...)
    | summarize arg_max(timeMax, *) by SiteId
```

**Juan's Approach:**
```kusto
let rated_capacity_newtry =
    goldAdtPropertyMinMaxLatestViewV2  // Start here, not goldAdtPropertyDevices
    | where Key in ('nameplateInfo.wMaxRtg','productInfo.prodSubType')
    | join kind = inner (goldAdtTwinEventsLatestV2 | ...) on ...
    | lookup kind = inner (relatedDevices | ...) on ...
    | summarize
        rated_capacity = anyif(valueMax, Key == 'nameplateInfo.wMaxRtg'),
        prodSubType = anyif(valueMax, Key == 'productInfo.prodSubType'),
        max_timeMax = max(timeMax)
    by siteId, deviceId = Id
    | where prodSubType in ("HybridInverter","BatteryInverter")
    | summarize arg_max(max_timeMax,*) by siteId
```

**Differences:**
- ✅ Eliminates `goldAdtPropertyDevices` table
- ✅ Uses `lookup` instead of `join` (faster for small lookups)
- ✅ Fetches multiple properties in one query

**Estimated Impact:** **-100 to -150ms** ✅ Moderate improvement

---

### **Optimization 5: System Size Query**

**V1 Approach:**
```kusto
let system_size = connectedIds
    | join kind=leftouter (goldAdtPropertyLatestViewV2 | ...) on ...
    | extend PriorityModel = case(...)
    | summarize arg_min(PriorityModel, Value) by SiteId
```

**Juan's Approach:**
```kusto
let system_size_newtry = 
    goldAdtPropertyMinMaxLatestViewV2  // Uses Min/Max view instead
    | where Key in ('systemSizeKw')
    | lookup kind = inner (relatedDevices | ...) on ...
    | summarize 
        (priorityModel, system_size_kw) = arg_min(...)
    by siteId
```

**Differences:**
- ✅ Uses `goldAdtPropertyMinMaxLatestViewV2` instead of `goldAdtPropertyLatestViewV2`
- ✅ Uses `lookup` instead of `join`
- ✅ More efficient aggregation

**Estimated Impact:** **-50 to -100ms** ✅ Minor improvement

---

## ⚠️ **WHAT JUAN DIDN'T CHANGE (Still Slow)**

### **1. Telemetry Data Fetch (Still ~500ms)**
```kusto
let commData = silverCommDataSite  // BILLIONS of rows!
    | where siteId in (paginatedSiteIdsList) 
    | summarize arg_max(sourceTimestamp, *) by siteId
    ...
```

**Issue:** Still scans `silverCommDataSite` (huge table)

**Potential Optimization:** Could be made optional or use indexed lookup

---

### **2. Program Data Fetch (Still ~400ms)**
```kusto
let program_data = GetLatestProgramSiteInfo
    | where site_id in (paginatedSiteIdsList)
    | join kind=inner (GetLatestProgramInfo | ...) on program_id
    | summarize program_name = make_set(program_name) by site_id
```

**Issue:** Still uses helper functions, still joins two tables

**Potential Optimization:** Could be made optional or materialized

---

### **3. User Mapping Might Still Be Slow**

Juan's nested `in` approach might actually be SLOWER than joins for large datasets because:
- Each `in` operator creates a subquery
- Nested `in` operators don't benefit from join optimization
- Kusto might not optimize this pattern well

**Potential Optimization:** Use `getCurrentUserSiteMapping()` helper (like V3 does)

---

## 📊 **ESTIMATED PERFORMANCE BREAKDOWN**

| Section | V1 Time | Juan's Test (Estimate) | Improvement |
|---------|---------|------------------------|-------------|
| User mapping | ~1,000ms | ~800-1,000ms? | ⚠️ 0-200ms |
| VPP filter | ~400ms | ~400ms | ➖ Same |
| Pagination | ~5ms | ~5ms | ➖ Same |
| Site properties | ~800ms | **~300ms** | ✅ **-500ms** |
| Telemetry | ~500ms | ~500ms | ➖ Same |
| Programs | ~400ms | ~400ms | ➖ Same |
| Device data | ~300ms | **~150ms** | ✅ **-150ms** |
| **TOTAL** | **~3,405ms** | **~2,555ms** | ✅ **~850ms saved** |

**Expected Juan's Test Performance in DEV:** **~2.5 seconds**

**Actual Performance in PROD:** **5-7 seconds** ❌

**Discrepancy:** **+2.5 to +4.5 seconds** 🚨

---

## 🚨 **WHY IS IT STILL 5-7 SECONDS IN PROD?**

### **Hypothesis 1: PROD Has More Data**
- PROD might have 10x more sites than DEV
- Nested `in` operators scale poorly with data volume
- `silverCommDataSite` much larger in PROD

### **Hypothesis 2: User Mapping is Bottleneck**
- Nested `in` approach might be slower than expected
- Should test with `getCurrentUserSiteMapping()` helper instead

### **Hypothesis 3: Missing Indexes**
- Tables might not be optimized in PROD
- Query cache might not be warm

---

## 🎯 **RECOMMENDED NEXT STEPS**

### **Step 1: Deploy to DEV and Measure**
Test Juan's function in DEV to get accurate baseline

### **Step 2: Profile Each Section**
Measure each section individually to find the actual bottleneck

### **Step 3: Apply Additional Optimizations**

**Priority 1: User Mapping**
```kusto
// Replace nested in operators with helper function
let site_ids_from_user = toscalar(
    getCurrentUserSiteMapping(inputUserId) 
    | project list_site_ids
);
```
**Expected savings:** -600 to -800ms

**Priority 2: Make Telemetry Optional**
```kusto
.create-or-alter function getAllVppSitesByUserId_optimized(
    inputUserId: string,
    includeTelemetry: bool = true,  // NEW parameter
    ...
)
```
**Expected savings:** -500ms when not needed

**Priority 3: Make Programs Optional**
```kusto
includePrograms: bool = true  // NEW parameter
```
**Expected savings:** -400ms when not needed

---

**Total Potential Additional Savings:** **~1,500-1,700ms**

**Target Performance:** **2.5s - 1.5s = ~1 second** 🎯✅

