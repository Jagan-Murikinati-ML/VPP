# 🚨 CRITICAL FINDING: Root Cause Identified!

**Date:** May 14, 2026  
**Analyzed by:** Jagan Murikinati

---

## ✅ **KEY DISCOVERY:**

### **getVPPSiteLevelPerformance is IDENTICAL in PROD and DEV**

Both versions are **EXACTLY THE SAME** (79 lines, byte-for-byte identical).

**This means the problem is NOT in getVPPSiteLevelPerformance itself!**

---

## 🔍 **Root Cause: Helper Function Dependency**

The helper function `getSiteDispatchCommandSummary` has a **NESTED DEPENDENCY:**

```
getVPPSiteLevelPerformance (PROD = DEV ✅)
    ↓
getSiteDispatchCommandSummary (Line 7 below)
    ↓
getMultipleEventsSiteDispatchResults ❌ THIS IS THE PROBLEM!
```

---

## 📊 **Helper Function Analysis**

### **getSiteDispatchCommandSummary (Line 7):**

<augment_code_snippet path="ticket-12654/getSiteDispatchCommandSummary.csv" mode="EXCERPT">
```kusto
getMultipleEventsSiteDispatchResults(inputEventIds, inputSiteIds)
| where (event_id in (inputEventIds) or array_length(inputEventIds)==0) 
    and (site_id in (inputSiteIds) or array_length(inputSiteIds)==0)
```
</augment_code_snippet>

**Line 7 calls ANOTHER helper function:** `getMultipleEventsSiteDispatchResults`

---

## 🚨 **The Real Problem:**

### **Three-Level Dependency Chain:**

1. `getVPPSiteLevelPerformance` ✅ (same in PROD/DEV)
2. → calls `getSiteDispatchCommandSummary` ⚠️ (need to check PROD vs DEV)
3. → calls `getMultipleEventsSiteDispatchResults` ❌ **LIKELY BROKEN IN PROD**

---

## 🔬 **What getSiteDispatchCommandSummary Does:**

### **Data Source (Line 7):**
Calls `getMultipleEventsSiteDispatchResults` which likely:
- Queries `silver_dispatch_result_dto` (command results)
- Joins with `silverCommDataSite` (telemetry)
- Calculates cumulative energy values (cu_grid_200_IncWhImp, cu_battery_200_IncWhExp, etc.)

### **Key Columns Expected:**
- `cu_grid_200_IncWhImp` (cumulative grid import)
- `cu_grid_200_IncWhExp` (cumulative grid export)
- `cu_battery_200_IncWhImp` (cumulative battery charge)
- `cu_battery_200_IncWhExp` (cumulative battery discharge)
- `battery_200_W` (battery power)

**These columns have "cu_" prefix = CUMULATIVE values!**

---

## 📋 **Critical Tables/Functions:**

### **Helper Function Chain:**
1. `getVPPSiteLevelPerformance` (PROD = DEV ✅)
2. `getSiteDispatchCommandSummary` (need to verify PROD vs DEV)
3. `getMultipleEventsSiteDispatchResults` (**LIKELY MISSING/BROKEN IN PROD** ❌)

### **Data Tables Used:**
1. `silver_stream_dispatch_events` (event metadata)
2. `silver_dispatch_result_dto` (command results)
3. `silver_dispatch_events` (line 44 - event start times)
4. `silverCommDataSite` (implied - via getMultipleEventsSiteDispatchResults)

---

## 🎯 **Why It Fails in PROD:**

### **Most Likely Scenario:**

**`getMultipleEventsSiteDispatchResults` is either:**
1. ❌ **Missing in PROD** (not deployed)
2. ❌ **Different version in PROD** (older/broken)
3. ❌ **Depends on table that doesn't exist in PROD**
4. ❌ **Has different logic that filters out this event**

---

## 🔍 **Evidence from getSiteDispatchCommandSummary:**

### **Line 43-48: Uses silver_dispatch_events table**

<augment_code_snippet path="ticket-12654/getSiteDispatchCommandSummary.csv" mode="EXCERPT">
```kusto
| join kind=leftouter (
    silver_dispatch_events 
    | summarize arg_max(ingestion_time(),start_time, sites) by event_id
    | mv-expand sites
    | project event_id, event_start_time = start_time, site_id = tostring(sites), command_group_id = 1
) on event_id, site_id, command_group_id
```
</augment_code_snippet>

**Wait! This uses `silver_dispatch_events` (NOT `silver_stream_dispatch_events`)**

### **🚨 POTENTIAL ISSUE #1:**
- `getVPPSiteLevelPerformance` uses `silver_stream_dispatch_events` (line 11)
- `getSiteDispatchCommandSummary` uses `silver_dispatch_events` (line 44)

**Are these the same table?** Or is one missing in PROD?

---

## 🔬 **Complex Energy Calculations (Lines 59-66):**

The helper function calculates cumulative energy by:
1. Taking start time values (command_start_time_discharge, etc.)
2. Taking end time values (command_end_time_discharge, etc.)
3. Looking at next command start values
4. Calculating deltas: `next_start - command_start` or `command_end - command_start`

**This is VERY complex logic - if any value is NULL, entire calculation fails!**

---

## 📊 **Data Flow:**

```
getMultipleEventsSiteDispatchResults(eventIds, siteIds)
    ↓
Returns rows with:
    - event_id, site_id, dispatch_time, command
    - cu_grid_200_IncWhImp (cumulative grid import)
    - cu_battery_200_IncWhExp (cumulative battery discharge)
    - battery_200_W (battery power)
    ↓
getSiteDispatchCommandSummary filters and aggregates
    ↓
Groups by command_type (discharge/charge/stop)
    ↓
Calculates overall_command_discharge, overall_command_charge, etc.
    ↓
getVPPSiteLevelPerformance summarizes per site
    ↓
Returns final site-level data
```

**If getMultipleEventsSiteDispatchResults returns 0 rows → entire chain fails!**

---

## 💡 **Next Investigation Steps:**

### **Step 1: Check if getMultipleEventsSiteDispatchResults exists in PROD**

```kusto
.show functions
| where Name == 'getMultipleEventsSiteDispatchResults'
```

### **Step 2: Test the function directly in PROD**

```kusto
getMultipleEventsSiteDispatchResults(
    dynamic(['ca0c0d89-614d-4358-b31f-2cb27a29cf5f']), 
    dynamic([])
)
```

**Expected:** Should return rows with event_id, site_id, dispatch_time, cu_* columns

**If returns 0 rows** → THIS IS THE ROOT CAUSE! ❌

### **Step 3: Check silver_dispatch_events vs silver_stream_dispatch_events**

```kusto
// Check if both tables exist
.show tables
| where TableName in ('silver_dispatch_events', 'silver_stream_dispatch_events')

// Check if they have data for this event
silver_dispatch_events
| where event_id == 'ca0c0d89-614d-4358-b31f-2cb27a29cf5f'
| take 10

silver_stream_dispatch_events
| where event_id == 'ca0c0d89-614d-4358-b31f-2cb27a29cf5f'
| take 10
```

---

## ✅ **Confirmed Facts:**

1. ✅ `getVPPSiteLevelPerformance` is IDENTICAL in PROD and DEV
2. ✅ `getVPPDispatchSummary` works in PROD (queries silverCommDataSite directly)
3. ✅ Raw telemetry data exists in PROD (we verified this)
4. ✅ `silver_stream_dispatch_events` has event data in PROD (we queried it)
5. ❌ `getVPPSiteLevelPerformance` returns 0 rows in PROD
6. ✅ `getVPPSiteLevelPerformance` returns data in DEV

---

## 🎯 **Conclusion:**

**Root Cause is in the nested dependency chain:**

1. **getMultipleEventsSiteDispatchResults** is likely broken/missing in PROD
2. OR `silver_dispatch_events` table is missing/empty in PROD
3. OR the cumulative calculation logic fails with PROD data

**Next Action:** Test `getMultipleEventsSiteDispatchResults` directly in PROD!

---

## 🚀 **Updated ADO Comment for Shaun:**

```
Hi @Shaun Roach,

Further investigation reveals a 3-level dependency chain:

getVPPSiteLevelPerformance (PROD = DEV ✅)
  → getSiteDispatchCommandSummary
     → getMultipleEventsSiteDispatchResults ❌ LIKELY BROKEN IN PROD

The main function is identical in PROD and DEV. The issue is in a nested helper function.

Can you please test this in PROD:
getMultipleEventsSiteDispatchResults(dynamic(['ca0c0d89-614d-4358-b31f-2cb27a29cf5f']), dynamic([]))

This should return site-level dispatch results with cumulative energy values.
If it returns 0 rows, that's the root cause.

Also, please check if these tables exist in PROD:
- silver_dispatch_events (used by getSiteDispatchCommandSummary)
- silver_stream_dispatch_events (used by getVPPSiteLevelPerformance)

Thanks,
Jagan
```
