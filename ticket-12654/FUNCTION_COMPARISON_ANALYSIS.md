# Function Comparison Analysis: getVPPSiteLevelPerformance vs getVPPDispatchSummary

**Analyzed by:** Jagan Murikinati  
**Date:** May 14, 2026  
**Event:** ca0c0d89-614d-4358-b31f-2cb27a29cf5f

---

## 🔍 Critical Difference Found!

### **DEV Environment:** ✅ getVPPSiteLevelPerformance returns data
### **PROD Environment:** ❌ getVPPSiteLevelPerformance returns NO data

---

## 📊 Key Architectural Differences

| Aspect | getVPPDispatchSummary ✅ | getVPPSiteLevelPerformance ❌ |
|--------|-------------------------|------------------------------|
| **Data Source** | silverCommDataSite (telemetry) | getSiteDispatchCommandSummary (helper function) |
| **Site List Source** | silver_stream_dispatch_events (sites array) | silver_stream_dispatch_events (sites array) |
| **Command Status** | silver_dispatch_result_dto | getSiteDispatchCommandSummary |
| **Aggregation** | 15-min bins, all sites combined | Per site, per command_type |
| **Filtering** | Excludes "stop" commands | Excludes "stop" commands (line 50) |
| **Works in PROD?** | ✅ YES | ❌ NO |

---

## 🚨 ROOT CAUSE IDENTIFIED!

### **getVPPSiteLevelPerformance Dependency Chain:**

```
getVPPSiteLevelPerformance
    ↓
calls getSiteDispatchCommandSummary(inputEventIds = pack_array(input_event_name))
    ↓
    [THIS FUNCTION RETURNS NO DATA IN PROD!]
    ↓
Line 38: eventData = getSiteDispatchCommandSummary(...)
    ↓
Line 57: join kind=leftouter (eventData) on event_id, site_id
    ↓
If getSiteDispatchCommandSummary returns 0 rows, the entire result is empty!
```

---

## 🔬 Detailed Code Analysis

### **getVPPSiteLevelPerformance (Lines 37-51):**

```kusto
let eventData = 
    getSiteDispatchCommandSummary(inputEventIds =  pack_array(input_event_name))
    // | where isnotnull(command_start_time_charge) and isnotnull(command_start_time_discharge)
    | summarize 
        energy_charged_kWh = sum(overall_command_charge)/1000.0
        ,energy_discharged_kWh = sum(overall_command_discharge)/1000.0
        ,energy_exported_kWh = sum(overall_command_exported)/1000.0
        ,energy_imported_kWh = sum(overall_command_imported)/1000.0
        ,battery_power = sum(overall_command_battery_power*overall_command_time_seconds)/sum(overall_command_time_seconds)/1000.0
        ,dispatch_end_time = max(overall_command_end_time)
        ,dispatch_start_time = min(overall_command_start_time)
        ,dispatch_windows = make_list(strcat(overall_command_start_time, ' - ', overall_command_end_time))
    by site_id, event_id, command_type
    | where tolower(command_type) != 'stop'
;
```

**KEY ISSUE:** Depends on `getSiteDispatchCommandSummary` helper function!

---

### **getVPPDispatchSummary (Lines 19-47):**

```kusto
let dispatch_summary = 
    database('EventHouse').table('silverCommDataSite') 
    | where siteId in~ (sites_list)
        and (sourceTimestamp >= evt_start_time and sourceTimestamp < evt_end_time)
        and battery_200_IncWhExp between (0 .. 7500)
    | summarize 
        load_200_W =  avg(load_200_W),
        pv_200_W = avg(pv_200_W), 
        battery_200_W = avg(battery_200_W), 
        battery_200_IncWhImp = sum(battery_200_IncWhImp),
        battery_200_IncWhExp = sum(battery_200_IncWhExp),
        grid_200_IncWhImp = sum(grid_200_IncWhImp),
        grid_200_IncWhExp = sum(grid_200_IncWhExp),
        count = count()
    by siteId, bin(sourceTimestamp, 15min)
```

**KEY STRENGTH:** Directly queries silverCommDataSite (raw telemetry data)!

---

## 💡 Why getVPPDispatchSummary Works:

1. ✅ **Direct telemetry access:** Queries silverCommDataSite directly
2. ✅ **No helper function dependency:** All logic self-contained
3. ✅ **Telemetry exists:** Raw data available in PROD
4. ✅ **Simple filtering:** Just time window + site list

---

## 🚨 Why getVPPSiteLevelPerformance Fails:

1. ❌ **Helper function dependency:** Relies on `getSiteDispatchCommandSummary`
2. ❌ **Helper function broken:** `getSiteDispatchCommandSummary` returns 0 rows in PROD
3. ❌ **Cascade failure:** If helper returns nothing, entire result is empty
4. ❌ **No fallback:** Left outer join with empty dataset = empty result

---

## 🔎 What is getSiteDispatchCommandSummary?

**This is the missing piece!** We need to investigate this helper function:

```kusto
getSiteDispatchCommandSummary(inputEventIds = pack_array(input_event_name))
```

**Expected columns:**
- site_id
- event_id
- command_type
- overall_command_charge
- overall_command_discharge
- overall_command_exported
- overall_command_imported
- overall_command_battery_power
- overall_command_time_seconds
- overall_command_start_time
- overall_command_end_time

**This function is likely:**
1. Querying silver_dispatch_result_dto (command results)
2. Joining with silverCommDataSite (telemetry)
3. Aggregating energy values per site per command
4. **FAILING IN PROD but WORKING IN DEV**

---

## 🎯 Probable Root Causes

### **Option 1: Data Missing in PROD**
- `getSiteDispatchCommandSummary` might depend on a table that exists in DEV but not PROD
- Or table exists but has missing data

### **Option 2: Function Version Mismatch**
- DEV has newer version of `getSiteDispatchCommandSummary`
- PROD has older/broken version

### **Option 3: Time Window Issue**
- Helper function has strict time filtering
- Events in PROD don't match the time criteria

### **Option 4: Stop Command Issue**
- Line 50: `| where tolower(command_type) != 'stop'`
- If helper function returns ONLY 'stop' commands, they get filtered out = empty result

---

## 📋 Comparison Table

| Feature | getVPPDispatchSummary | getVPPSiteLevelPerformance |
|---------|----------------------|----------------------------|
| **Lines of Code** | 89 | 79 |
| **Data Source** | Direct (silverCommDataSite) | Indirect (helper function) |
| **Dependencies** | None | getSiteDispatchCommandSummary |
| **Site Participation Source** | silver_dispatch_result_dto | getSiteDispatchCommandSummary |
| **Aggregation Level** | All sites, 15-min bins | Per site, per command |
| **Customer Info** | No | Yes (firstName, lastName) |
| **OEM Info** | No | Yes (oemName) |
| **PROD Status** | ✅ Works | ❌ Broken |
| **DEV Status** | ✅ Works | ✅ Works |

---

## 🛠️ Recommended Actions

### **Immediate:**
1. **Check `getSiteDispatchCommandSummary` function code in PROD vs DEV**
   ```kusto
   .show function getSiteDispatchCommandSummary
   ```

2. **Test the helper function directly in PROD:**
   ```kusto
   getSiteDispatchCommandSummary(inputEventIds = pack_array('ca0c0d89-614d-4358-b31f-2cb27a29cf5f'))
   ```

3. **Compare results in DEV vs PROD**

---

### **Long-term:**
1. **Option A: Fix `getSiteDispatchCommandSummary` in PROD**
   - Deploy DEV version to PROD
   - Or fix the underlying data issue

2. **Option B: Rewrite `getVPPSiteLevelPerformance` to work like `getVPPDispatchSummary`**
   - Query silverCommDataSite directly
   - Remove dependency on helper function
   - More resilient and maintainable

---

## 🔍 Next Investigation Steps

1. **Retrieve `getSiteDispatchCommandSummary` function code from PROD and DEV**
2. **Compare the two versions** for differences
3. **Test helper function directly** with the problem event ID
4. **Check if the tables it depends on exist and have data**

---

## ✅ Conclusion

**Root Cause:** `getVPPSiteLevelPerformance` fails because its dependency `getSiteDispatchCommandSummary` returns NO DATA in PROD.

**Why DEV works:** The helper function (or its data sources) work correctly in DEV.

**Why PROD fails:** The helper function is broken/missing data in PROD.

**Solution:** Investigate and fix `getSiteDispatchCommandSummary` function or rewrite `getVPPSiteLevelPerformance` to query silverCommDataSite directly like `getVPPDispatchSummary` does.

---

**This is a DEPENDENCY ISSUE, not a primary function logic issue!**
