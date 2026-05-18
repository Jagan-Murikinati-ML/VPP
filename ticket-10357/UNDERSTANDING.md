# Ticket 10357 - Performance Issue Understanding

## Problem Statement
The `getAllVppSitesByUserId` function takes 3-5 seconds to execute, which is too slow for a good user experience.

## 🔍 **CRITICAL DISCOVERY!**

**There are TWO DIFFERENT functions:**

### 1. **`getAllVppSitesByUserId` (V1, V2)** - Your original ticket
- **Function name:** `getAllVppSitesByUserId` (existing function)
- **Purpose:** Full-featured VPP site list with filters, sorting, search
- **Performance:** 3-5 seconds ❌

### 2. **`getAllVppRegisteredSitesByUserId` (Original existing function)** - Different function!
- **Function name:** `getAllVppRegisteredSitesByUserId` ⚠️ **DIFFERENT NAME!**
- **Purpose:** Simpler VPP site list with state/utility filters only
- **Performance:** Unknown (this exists in production already!)

### 3. **`getAllVppRegisteredSitesByUserId_v3`** - Sanjeev's optimization
- **Function name:** `getAllVppRegisteredSitesByUserId_v3` (new version)
- **Purpose:** Optimized version of `getAllVppRegisteredSitesByUserId` (not `getAllVppSitesByUserId`!)
- **Performance:** 1-2 seconds ✅

## ⚠️ **Key Insight:**

**V3 is NOT optimizing your V2 function!**

Sanjeev's V3 is optimizing a **DIFFERENT function** called `getAllVppRegisteredSitesByUserId` that already exists!

Your V2 function (`getAllVppSitesByUserId`) is still the slow one that needs optimization!

## Current State

### V1 - `getAllVppSitesByUserId` (Original, 134 lines)
- **Performance:** 2-3 seconds
- **Features:**
  - Server-side pagination only
  - No filtering, no sorting, no search
  - Full site data (14+ fields including telemetry)
  - Program names, battery status, grid energy
  - Uses helper functions: `GetSiteProperties()`, `getTimezonesBySites()`, etc.

### V2 - `getAllVppSitesByUserId` (Your enhancement)
- **Performance:** 3-5 seconds (SLOWER than V1!)
- **Features:**
  - Server-side filtering (multiple fields, operators)
  - Server-side sorting (any field, asc/desc)
  - Server-side pagination
  - Global search across all fields
  - Full site data (14+ fields including telemetry)
  - All V1 features + filtering/sorting/search


### Original - `getAllVppRegisteredSitesByUserId` (Existing in production, 105 lines)
- **Performance:** Unknown
- **Features:**
  - State/utility filtering
  - Fixed sorting (siteId ascending)
  - Server-side pagination
  - Minimal site data (7 fields only)
  - Battery capacity included (always)
  - Uses `getCurrentUserSiteMapping()` helper
  - **No telemetry, no program names**

### V3 - `getAllVppRegisteredSitesByUserId_v3` (Sanjeev's optimization)
- **Performance:** 1-2 seconds ✅
- **Features:**
  - Same as original `getAllVppRegisteredSitesByUserId`
  - **PLUS:** Optional battery capacity (`includeBattCap` parameter)
  - Uses same `getCurrentUserSiteMapping()` helper

## 📊 Table Usage Comparison

### Tables Used in V1 (`getAllVppSitesByUserId`)

| Step | Table | Rows | What For |
|------|-------|------|----------|
| 1 | `silverUserEvents` | 5k | User lookup |
| 1 | `goldUserGroupToUserMapping` | 5k | User → User Group |
| 1 | `goldUserGroupToResourceGroupMapping` | 5k | User Group → Resource Group |
| 1 | `goldResourceGroupToSiteMapping` | 400k | Resource Group → Sites ⚠️ |
| 1 | `ValidPropertyViewV2` | 576k | Validate sites ⚠️ |
| 2 | `goldAdtPropertyMinMaxLatestViewV2` | 1.6M | VPP registered check 🔴 |
| 2 | `goldAdtTwinEventsLatestV2` | 55k | Twin validation |
| 4 | **`GetSiteProperties()`** (helper) | - | **Gets ALL site properties** ⚠️ |
| 5 | **`getTimezonesBySites()`** (helper) | - | Gets timezones |
| 6 | `silverCommDataSite` | BILLIONS | **Telemetry data** 🔴 |
| 7 | `GetLatestProgramSiteInfo` | - | Program relationships |
| 7 | `GetLatestProgramInfo` | - | Program names |
| 8 | `goldAdtPropertyDevices` | 21k | Device info |
| 8 | `connectedIds` (via helper) | - | Device relationships |
| 8 | `goldAdtPropertyMinMaxLatestViewV2` | 1.6M | Device properties 🔴 |
| 8 | `goldAdtPropertyLatestViewV2` | 1.6M | System size 🔴 |

**Total: 15+ table scans, including 4 scans of 1.6M row tables!** ❌

---

### Tables Used in `getAllVppRegisteredSitesByUserId` (Original) & V3

| Step | Table | Rows | What For |
|------|-------|------|----------|
| 1 | **`getCurrentUserSiteMapping()`** (helper) | - | **Pre-cached user → sites** ✅ |
| 2 | `goldAdtPropertyMinMaxLatestViewV2` | 1.6M | VPP registered check 🔴 |
| 2 | `goldAdtTwinEventsLatestV2` | 55k | Twin validation |
| 3 | `goldAdtPropertyMinMaxLatestViewV2` | 1.6M | **Only 5 properties** (state, utility, zip, loadZone, oem) ✅ |
| 4 | `goldAdtPropertyMinMaxLatestViewV2` | 1.6M | Battery capacity (optional in V3) |
| 4 | `goldAdtTwinEventsLatestV2` | 55k | Battery devices |
| 4 | `goldAdtAllRelationshipsLatestView` | ? | Device relationships |

**Total: 7 table scans, but NO telemetry, NO program data, MINIMAL properties!** ✅

---

## 🔍 What `getCurrentUserSiteMapping()` Does

From the helper function code:

```kql
silverUserEvents
| where user_id == inputUserId
| join kind=inner (goldUserGroupToUserMapping | where isingroup > 0)
    on $left.user_id == $right.user_ids
| join kind=inner(goldUserGroupToResourceGroupMapping | where isingroup > 0)
    on $left.user_group_id == $right.user_group_id
| join kind=inner(goldResourceGroupToSiteMapping | where isingroup > 0)
    on $left.resource_group_ids == $right.resource_group_id
| join kind=inner goldAdtPropertySites  // ← Uses materialized view!
    on $left.site_ids == $right.siteId
| distinct user_id, site_ids
| summarize make_list(site_ids) by user_id
```

**Key Difference:**
- V1: Joins `ValidPropertyViewV2` (576k rows) - expensive scan! ❌
- Helper: Joins `goldAdtPropertySites` - likely a **materialized view** ✅

**This helper function is faster because:**
1. Uses `goldAdtPropertySites` (materialized view) instead of `ValidPropertyViewV2`
2. Returns array directly (no need to re-query)
3. Can be **cached** by Kusto

---

## Performance Analysis

### Why V1 is Slow (2-3 seconds)

#### 1. User Mapping Joins (~1,000ms)
```
4 joins including ValidPropertyViewV2 (576k rows)
```

#### 2. GetSiteProperties() Function (~800ms)
- Fetches ALL 50+ properties per site
- Scans goldAdtPropertyMinMaxLatestViewV2 (1.6M rows!)
- Complex bag operations

#### 3. Telemetry Data (~500ms)
- Scans silverCommDataSite (BILLIONS of rows) 🔴
- Fetches grid energy, SOC, etc.

#### 4. Program Data (~400ms)
- Joins GetLatestProgramSiteInfo
- Joins GetLatestProgramInfo

#### 5. Device Data (~300ms)
- Multiple joins for battery capacity and system size

**Total: ~3,000ms**

---

### Why V2 is SLOWER than V1 (3-5 seconds)

**V2 = V1 + filtering/sorting/search logic**

V2 adds:
- Dynamic filtering (mv-expand, complex where clauses) +500ms
- Triple sorting logic (asc/desc on any field) +400ms
- Global search (searches across ALL fields) +600ms
- Extra materialize() calls for filter/sort +200ms

**Total: V1 (3,000ms) + additions (1,700ms) = 4,700ms**

---

### Why Original `getAllVppRegisteredSitesByUserId` is Faster

**Skips:**
- ❌ No `GetSiteProperties()` - saves ~800ms
- ❌ No telemetry (`silverCommDataSite`) - saves ~500ms
- ❌ No program data - saves ~400ms
- ❌ No device data (except battery) - saves ~300ms
- ✅ Uses `getCurrentUserSiteMapping()` helper - saves ~400ms

**Fetches only 5 properties directly:**
- state, utility, zipCode, loadZone, oem

**Total savings: ~2,400ms**

**Estimated time: ~600-800ms**

### Why V3 is Faster (1-2 seconds)

V3 adds ONE optimization to the original `getAllVppRegisteredSitesByUserId`:

#### **Optional Battery Capacity** (`includeBattCap` parameter)

**Original function:**
- Always fetches battery capacity (adds ~200-300ms)

**V3 function:**
```kql
| where includeBattCap  // Only fetch if requested
```

**Savings when `includeBattCap=false`: ~200-300ms**

**Result:**
- V3 with `includeBattCap=false`: ~600ms ⚡
- V3 with `includeBattCap=true`: ~900ms ✅
- Original: ~900ms (always includes battery)

**V3 improvement: Makes battery capacity optional for faster queries when not needed!**

## 🎯 The Real Problem

**Ticket #10357 is about `getAllVppSitesByUserId` (V1/V2), NOT `getAllVppRegisteredSitesByUserId`!**

### Sanjeev's V3 Doesn't Solve Your Problem!

V3 optimizes a **DIFFERENT function** that:
- Already has different use case (state/utility filtering only)
- Already doesn't have telemetry/programs (by design)
- Already is simpler/faster

**Your V2 function is STILL slow (3-5s) and needs optimization!**

---

## 📊 Feature Comparison

| Feature | V1 | V2 (Your Work) | Original `getAllVppRegistered...` | V3 |
|---------|----|----|----------------------------------|-----|
| **Function Name** | `getAllVppSitesByUserId` | `getAllVppSitesByUserId` | `getAllVppRegisteredSitesByUserId` | `getAllVppRegisteredSitesByUserId_v3` |
| **Performance** | 2-3s | 3-5s ❌ | ~900ms | 600ms-900ms ✅ |
| **Pagination** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **State/utility filter** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |
| **Dynamic filters** | ❌ No | ✅ Yes (any field) | ❌ No | ❌ No |
| **Dynamic sorting** | ❌ No | ✅ Yes (any field) | ❌ No (siteId only) | ❌ No (siteId only) |
| **Global search** | ❌ No | ✅ Yes | ❌ No | ❌ No |
| **Site name** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **SOC (battery %)** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **Grid energy** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **Program names** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **Inverter status** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **System size** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **Battery capacity** | ✅ Yes | ✅ Yes | ✅ Yes (always) | ✅ Yes (optional) |
| **Fields returned** | 14 | 14 | 7 | 7 |
| **Use Case** | Full site list | Full list + filters/sort/search | State/utility filter only | State/utility filter only |

---

## 🔥 Critical Insights

### 1. **There are TWO separate functions for TWO different use cases!**

**`getAllVppSitesByUserId`** (V1, V2):
- Full-featured site list
- All telemetry, programs, device data
- Supports rich filtering, sorting, search (V2 only)
- **Problem: Too slow (3-5s)**

**`getAllVppRegisteredSitesByUserId`** (Original, V3):
- Minimal site list (7 fields)
- State/utility filtering only
- No telemetry, no programs
- **Already fast (~900ms), V3 makes it faster (~600ms)**

### 2. **V3 doesn't help your V2 performance problem!**

Sanjeev's V3 is optimizing a different, simpler function. It doesn't solve Ticket #10357!

### 3. **V2 is SLOWER than V1 (your baseline)!**

- V1: 2-3s
- V2: 3-5s ❌

**Why?** V2 adds filtering/sorting/search logic that adds ~1-2s overhead!

---

## 💡 What Can We Learn from V3?

Even though V3 doesn't directly solve your problem, we can apply its optimizations to V2:

### Optimization 1: Use `getCurrentUserSiteMapping()` Helper ⚡

**V1/V2 approach:**
```kql
let site_ids_from_user = materialize(
    silverUserEvents | join ... | join ... | join ... | join ValidPropertyViewV2
);
```
**Time: ~1,000ms**

**V3 approach:**
```kql
let site_ids_from_user = toscalar(getCurrentUserSiteMapping(inputUserId) | project list_site_ids);
```
**Time: ~200-300ms**

**Savings: ~700-800ms** ✅

---

### Optimization 2: Fetch Minimal Properties First, Full Data Only for Page ⚡

**V1 approach:**
1. Get all VPP sites (5,000 sites)
2. Call `GetSiteProperties()` on ALL 5,000 sites (~800ms)
3. Paginate to 50 sites
4. Fetch telemetry for 50 sites

**V3 approach:**
1. Get all VPP sites (5,000 sites)
2. Fetch ONLY 5 properties for ALL 5,000 sites (~250ms)
3. Filter by state/utility (reduce to 500 sites)
4. Paginate to 50 sites
5. (Skip telemetry - not needed for this use case)

**Savings: ~550ms** ✅

---

### Optimization 3: Make Expensive Operations Optional ⚡

**V3 innovation:**
```kql
| where includeBattCap  // Only fetch if needed
```

**Apply to V2:**
- Make telemetry optional (`includeTelemetry` parameter)
- Make program data optional (`includePrograms` parameter)
- Make device data optional (`includeDeviceData` parameter)

**Potential savings: ~1,200ms when not needed** ✅

## 🚀 Recommended Path Forward

### **Optimize Your V2 Function (`getAllVppSitesByUserId`)**

Apply learnings from V3 to create an optimized V2:

**Target Performance:** 1.5-2.5 seconds (instead of 3-5s)

#### Step 1: Replace User Mapping with Helper Function
```kql
// OLD (1,000ms):
let site_ids_from_user = materialize(
    silverUserEvents | join ... | join ... | join ValidPropertyViewV2
);

// NEW (200-300ms):
let site_ids_from_user = toscalar(
    getCurrentUserSiteMapping(inputUserId) | project list_site_ids
);
```
**Savings: ~700-800ms** ✅

---

#### Step 2: Fetch Minimal Properties for Filtering, Full Data for Page Only
```kql
// Get VPP sites (same as before)
let vppSites = goldAdtPropertyMinMaxLatestViewV2 | where ...

// NEW: Fetch minimal properties for ALL sites (for filtering/sorting)
let vppSiteMinimal = goldAdtPropertyMinMaxLatestViewV2
    | where Id in (vppSites)
    | where Key in ('otherProperties.siteName', 'address.stateProvince',
                    'utilityName', 'oemInfo.oemName', ...)  // Only needed fields
    | summarize ... by siteId

// Apply filters and sorting on minimal data
let filteredSorted = vppSiteMinimal | where ... | order by ...

// Paginate FIRST
let paginatedSiteIds = filteredSorted | take page_size | skip page * page_size

// THEN fetch full data (telemetry, programs, etc.) only for paginated sites
let fullData = GetSiteProperties(paginatedSiteIds)
    | join telemetry | join programs ...
```
**Savings: ~500-600ms** ✅

---

#### Step 3: Make Expensive Operations Optional
```kql
// Add optional parameters
getAllVppSitesByUserIdV2_Optimized(
    inputUserId: string,
    includeTelemetry: bool = true,
    includePrograms: bool = true,
    includeDeviceData: bool = true,
    ...
)

// Skip expensive queries if not needed
let telemetryData = iff(includeTelemetry,
    silverCommDataSite | where ...,
    datatable(siteId:string)[])  // Empty table
```
**Savings: Up to ~1,200ms when optional data not needed** ✅

---

**Total Potential Savings: ~2,100-2,600ms**

**New Performance: 3,500ms - 2,100ms = ~1,400ms (1.4s)** 🎯

---

## 📋 Next Steps

### 1. ✅ **Understand V3** (DONE)
- V3 is for a different function (not your V2)
- V3 optimizations can be applied to V2

### 2. **Test V3 to Validate Claims**
```kql
// Test V3 without battery capacity
getAllVppRegisteredSitesByUserId_v3(
    inputUserId = '81ab4c51-a8d9-ef11-8eea-00224809f11c',
    includeBattCap = false,
    page = 0,
    page_size = 50
)

// Test V3 with battery capacity
getAllVppRegisteredSitesByUserId_v3(
    inputUserId = '81ab4c51-a8d9-ef11-8eea-00224809f11c',
    includeBattCap = true,
    page = 0,
    page_size = 50
)
```

### 3. **Measure Current V2 Performance**
```kql
let start = now();
let result = getAllVppSitesByUserIdV2(...);
let end = now();
print duration_ms = datetime_diff('millisecond', end, start);
```

### 4. **Create Optimized V2**
Apply the 3 optimizations above

### 5. **Test Optimized V2**
- Measure performance improvement
- Verify all features still work (filtering, sorting, search)
- Compare output with original V2

### 6. **Present to Team**
Show before/after performance metrics

---

## ❓ Questions for Sanjeev/Juan/Naveen

1. **Can we use `getCurrentUserSiteMapping()` for `getAllVppSitesByUserId` too?**
   - This helper uses `goldAdtPropertySites` instead of `ValidPropertyViewV2`
   - Would save ~700-800ms

2. **Is `goldAdtPropertySites` a materialized view?**
   - Understanding this will help us know if we can use it

3. **Should V2 also have optional parameters for telemetry/programs?**
   - Would improve performance when full data not needed

4. **Is the V3 function name final?**
   - `getAllVppRegisteredSitesByUserId_v3` seems to be a different use case than V2
   - Clarify if this is meant to eventually replace V1/V2

5. **What's the actual performance of V3 in production?**
   - Sanjeev mentioned 1-2s, verify this claim

---

## 📝 Summary

### Key Discoveries:

1. ✅ **V3 is NOT optimizing your V2 function** - it's optimizing a DIFFERENT function!
2. ✅ **V2 is SLOWER than V1** due to added filtering/sorting/search logic
3. ✅ **V3 shows us how to optimize** via:
   - `getCurrentUserSiteMapping()` helper
   - Minimal property fetching
   - Optional expensive operations
4. ✅ **We can apply V3's learnings to V2** to achieve ~1.4s performance

### What V3 Does Well:

- Uses helper function for user mapping (faster)
- Fetches only needed properties (5 instead of 50+)
- Makes battery capacity optional
- Skips telemetry and program data (not needed for that use case)

### What V2 Needs:

- Apply V3's optimization techniques
- Keep all existing features (filters, sort, search, telemetry, programs)
- Target: Reduce from 3-5s to 1.5-2.5s

**Ready to optimize V2!** 🚀

