# Deeper Analysis: getSiteDispatchCommandSummary Issues

**Date:** May 14, 2026  
**Scenario:** getMultipleEventsSiteDispatchResults EXISTS in PROD

---

## 🔍 Other Potential Issues in getSiteDispatchCommandSummary

Since `getMultipleEventsSiteDispatchResults` exists in PROD, let's look at what could cause `getSiteDispatchCommandSummary` to return 0 rows:

---

## 🚨 **Issue #1: Filter at Line 50 (command_type != 'stop')**

<augment_code_snippet path="ticket-12654/getSiteDispatchCommandSummary.csv" mode="EXCERPT">
```kusto
| where tolower(command_type) != 'stop'
```
</augment_code_snippet>

**In getVPPSiteLevelPerformance line 50:**
```kusto
| where tolower(command_type) != 'stop'
```

**Scenario:** If ALL commands for this event are classified as 'stop', they get filtered out!

**Test in PROD:**
```kusto
getSiteDispatchCommandSummary(inputEventIds = pack_array('ca0c0d89-614d-4358-b31f-2cb27a29cf5f'), inputSiteIds = dynamic([]))
| summarize count() by command_type
```

**If only 'stop' commands exist → they get filtered → 0 rows!**

---

## 🚨 **Issue #2: Table Mismatch - silver_dispatch_events vs silver_stream_dispatch_events**

**Line 44 of getSiteDispatchCommandSummary:**
```kusto
silver_dispatch_events 
| summarize arg_max(ingestion_time(),start_time, sites) by event_id
```

**Question:** Does `silver_dispatch_events` exist in PROD and have data for this event?

**Test in PROD:**
```kusto
// Check if table exists
.show tables | where TableName == 'silver_dispatch_events'

// Check if event exists in this table
silver_dispatch_events
| where event_id == 'ca0c0d89-614d-4358-b31f-2cb27a29cf5f'
| take 10
```

**If table doesn't exist or has no data → left join fails → wrong event_start_time → calculations fail!**

---

## 🚨 **Issue #3: Left Join Returns No Matches**

**Lines 43-48:**
```kusto
| join kind=leftouter (
    silver_dispatch_events 
    | summarize arg_max(ingestion_time(),start_time, sites) by event_id
    | mv-expand sites
    | project event_id, event_start_time = start_time, site_id = tostring(sites), command_group_id = 1
) on event_id, site_id, command_group_id
```

**Join Keys:** event_id, site_id, **command_group_id**

**Potential Issue:** If `command_group_id` doesn't match (always = 1), join fails!

**From line 29-32, command_group_id is calculated as:**
```kusto
command_group_id = row_cumsum(
    iif(event_id != prev(event_id, 1) or site_id != prev(site_id, 1) or command != prev(command, 1) , 1, 0)
    ,   event_id != prev(event_id, 1) or site_id != prev(site_id, 1)
)
```

**If command_group_id > 1 for all rows → join fails → event_start_time is NULL → calculations fail!**

---

## 🚨 **Issue #4: getMultipleEventsSiteDispatchResults Returns 0 Rows**

Even though the function exists, it might return 0 rows if:

1. **No matching data in silver_dispatch_result_dto**
2. **No telemetry in silverCommDataSite during event window**
3. **dispatch_status_code filtering** (line 10 is commented out but might be active in PROD)
4. **Different version of the function in PROD vs DEV**

**Test in PROD:**
```kusto
getMultipleEventsSiteDispatchResults(
    dynamic(['ca0c0d89-614d-4358-b31f-2cb27a29cf5f']), 
    dynamic([])
)
| take 10
```

**If returns 0 rows → function exists but returns no data!**

---

## 🚨 **Issue #5: Data Filtering in Line 8-10**

```kusto
| where (event_id in (inputEventIds) or array_length(inputEventIds)==0) 
    and (site_id in (inputSiteIds) or array_length(inputSiteIds)==0)
    // and dispatch_status_code == 200
```

**Line 10 is commented out!** But:
- In PROD, this might be **UN-commented** (active)
- If filtering for `dispatch_status_code == 200` only
- Sites that failed (400, 500) get excluded
- From our analysis: 2 sites succeeded (200), 2 failed (400, 500)

**If PROD version has line 10 active → filters to only successful sites → might still get 0 rows if calculation fails!**

---

## 🔬 **Step-by-Step Debugging in PROD:**

### **Test 1: Test getMultipleEventsSiteDispatchResults**
```kusto
getMultipleEventsSiteDispatchResults(
    dynamic(['ca0c0d89-614d-4358-b31f-2cb27a29cf5f']), 
    dynamic([])
)
```
**Expected:** Multiple rows with site_id, event_id, dispatch_time, cu_* columns  
**If 0 rows:** This function returns no data ❌

---

### **Test 2: Test getSiteDispatchCommandSummary (Before Filter)**
```kusto
getSiteDispatchCommandSummary(
    inputEventIds = pack_array('ca0c0d89-614d-4358-b31f-2cb27a29cf5f'), 
    inputSiteIds = dynamic([])
)
// Don't apply the 'stop' filter yet
```
**Expected:** Rows with command_type including 'discharge', 'stop', etc.  
**Check:** Are there ANY rows? What command_types exist?

---

### **Test 3: Check Command Types**
```kusto
getSiteDispatchCommandSummary(
    inputEventIds = pack_array('ca0c0d89-614d-4358-b31f-2cb27a29cf5f'), 
    inputSiteIds = dynamic([])
)
| summarize count() by command_type
```
**If only shows 'stop':** That's why it gets filtered out! ❌

---

### **Test 4: Check silver_dispatch_events Table**
```kusto
silver_dispatch_events
| where event_id == 'ca0c0d89-614d-4358-b31f-2cb27a29cf5f'
| take 10
```
**If 0 rows:** Table doesn't have this event → join fails ❌  
**If has rows:** Table exists and has data ✅

---

### **Test 5: Compare Function Versions**
```kusto
// In PROD:
.show function getSiteDispatchCommandSummary

// Compare with the CSV file you have
// Look for differences in line 10 (dispatch_status_code filter)
```

---

## 📊 **Most Likely Scenarios:**

### **Scenario 1: getMultipleEventsSiteDispatchResults Returns 0 Rows** (80% likely)
- Function exists but returns no data for this event
- Could be data issue, filtering issue, or calculation issue
- **Fix:** Debug why getMultipleEventsSiteDispatchResults returns nothing

### **Scenario 2: All Commands Are 'stop' Type** (15% likely)
- getSiteDispatchCommandSummary returns only 'stop' commands
- Line 50 filters them out
- Result: 0 rows
- **Fix:** Check command_type classification logic

### **Scenario 3: silver_dispatch_events Missing/Empty** (5% likely)
- Table doesn't exist or has no data for this event
- Join fails, event_start_time is NULL
- Calculations fail
- **Fix:** Populate silver_dispatch_events or use silver_stream_dispatch_events

---

## 🎯 **Action Plan:**

1. **Run Test 1:** Check if getMultipleEventsSiteDispatchResults returns data
2. **If 0 rows:** Investigate that function next (need to see its code)
3. **If has rows:** Run Test 2 to check getSiteDispatchCommandSummary
4. **If has rows:** Run Test 3 to check command_type distribution
5. **Report findings**

---

## 💡 **Quick Test to Run NOW:**

```kusto
// Test the full chain
getMultipleEventsSiteDispatchResults(
    dynamic(['ca0c0d89-614d-4358-b31f-2cb27a29cf5f']), 
    dynamic([])
)
| take 10

// If above returns data, test next level:
getSiteDispatchCommandSummary(
    inputEventIds = pack_array('ca0c0d89-614d-4358-b31f-2cb27a29cf5f'), 
    inputSiteIds = dynamic([])
)
| take 10

// Check command types:
getSiteDispatchCommandSummary(
    inputEventIds = pack_array('ca0c0d89-614d-4358-b31f-2cb27a29cf5f'), 
    inputSiteIds = dynamic([])
)
| summarize count() by command_type
```

**This will tell us EXACTLY where the chain breaks!** 🚀
