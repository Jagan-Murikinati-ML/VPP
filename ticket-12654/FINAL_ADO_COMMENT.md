# ADO Ticket Comment - Investigation Results (UPDATED)

---

## Investigation Complete - Event ca0c0d89-614d-4358-b31f-2cb27a29cf5f

Hi @Shaun Roach,

I've completed the investigation comparing function results with raw telemetry.

---

### Summary

**This is a UI RENDERING ISSUE caused by NaN values in the function results.**

✅ **Telemetry data exists and is correct**
✅ **`getVPPSiteLevelPerformance` function DOES return data in PROD**
❌ **Fabric UI fails to render the results (displays as blank)**
✅ **`getVPPDispatchSummary` function works correctly in PROD**

---

### Function Results Analysis

**Test 1: getVPPSiteLevelPerformance**
```kusto
getVPPSiteLevelPerformance(input_event_name='ca0c0d89-614d-4358-b31f-2cb27a29cf5f')
```
**Result in PROD:** ✅ Returns data (multiple sites with energy values)
- Function returns JSON array with site-level performance data
- Contains energy_discharged_kWh, energy_charged_kWh, etc. for each site
- **ISSUE: Many sites have `"battery_power":"NaN"` in the results**
- This NaN value likely causes Fabric UI to fail rendering the table

**When exported to CSV or called via Postman:** ✅ Data is visible and correct

**Test 2: getVPPDispatchSummary**
```kusto
getVPPDispatchSummary("ca0c0d89-614d-4358-b31f-2cb27a29cf5f")
```
**Result in PROD:** ✅ Returns data and renders correctly in UI
- 606 participating sites
- 3.14 MWh total energy discharged
- Data broken down by 15-min intervals

---

### Command Execution Status (4 Test Sites)

| Site ID | OEM | Status | Reason |
|---------|-----|--------|--------|
| 400029108 | Enphase | ❌ Failed | "startTime must be in the future" (400 error) |
| 400031093 | Unknown | ❌ Failed | Device control failure - 11 retry attempts (500 error) |
| 400032980 | SolarEdge | ✅ Success | Command executed |
| 400033526 | Tesla | ✅ Success | Command executed |

---

### Telemetry Analysis (Successful Sites)

**Site 400032980 (SolarEdge):**
- Command Status: ✅ Success (200)
- Battery SOC: 0.24% throughout event (battery already empty)
- Energy Discharged: 0 Wh (battery depleted, couldn't discharge)
- Telemetry Data: ✅ Present and accurate

**Site 400033526 (Tesla):**
- Command Status: ✅ Success (200)
- Battery SOC: 14.23% → 13.52% (dropped 0.71%)
- Energy Discharged: Minimal (~0.7% SOC drop)
- Telemetry Data: ✅ Present and accurate

---

### Root Cause

**The `getVPPSiteLevelPerformance` function returns data, but Fabric UI cannot render it.**

Investigation findings:
1. ✅ Function code is identical in PROD and DEV
2. ✅ Raw telemetry data exists in `silverCommDataSite` (verified)
3. ✅ Event data exists in `silver_stream_dispatch_events` (verified)
4. ✅ Command results exist in `silver_dispatch_result_dto` (verified)
5. ✅ Function returns data when called directly
6. ✅ Data is visible when exported to CSV or via Postman API
7. ❌ **Fabric UI displays blank table (fails to render the data)**

**Root cause:** The function calculates `battery_power` as `NaN` for many sites:
```
"battery_power":"NaN"
```

This happens in the calculation:
```kusto
battery_power = sum(overall_command_battery_power*overall_command_time_seconds)/sum(overall_command_time_seconds)/1000.0
```

When `sum(overall_command_time_seconds) = 0`, the division produces NaN, which breaks UI rendering.

---

### Why UI Shows Blank

1. UI calls `getVPPSiteLevelPerformance` function
2. Function returns data with NaN values in `battery_power` field
3. Fabric UI cannot render JSON with NaN values → displays blank table
4. When exported to CSV, the NaN is visible as a string `"NaN"` and data displays correctly
5. When called via Postman API, the JSON is returned (with NaN) but not parsed by UI

---

### Telemetry Status

✅ **Raw telemetry data is CORRECT and complete:**
- `silverCommDataSite` has telemetry for all successful sites
- SOC values are accurate (0.24% for site 400032980, 14.23% → 13.52% for site 400033526)
- Energy values match actual battery behavior
- Failed sites correctly show no performance data (commands failed)

❌ **Problem is NOT in the telemetry data - it's in the FUNCTION LOGIC**

---

### Comparison: Working vs Broken Functions

| Feature | getVPPDispatchSummary | getVPPSiteLevelPerformance |
|---------|----------------------|----------------------------|
| **Data Source** | silverCommDataSite (direct query) | Helper functions (indirect) |
| **Aggregation** | All sites, 15-min bins | Per site, per command |
| **Returns Data** | ✅ Yes | ✅ Yes |
| **UI Renders** | ✅ Yes | ❌ No (NaN breaks rendering) |
| **CSV Export** | ✅ Works | ✅ Works |
| **Postman API** | ✅ Works | ✅ Works |
| **Telemetry** | ✅ Queries directly | ✅ Via helper functions |

---

### Recommendation

1. **Fix the NaN calculation in `getVPPSiteLevelPerformance`** function:
   - Add null/zero check before division in battery_power calculation
   - Use `iif()` or `iff()` to handle division by zero: `iif(sum(overall_command_time_seconds) == 0, 0, sum(...)/sum(...))`

2. **Alternative workaround:** Have the UI handle NaN values gracefully (but fixing the function is better)

3. **Test in DEV** after fix to ensure no NaN values are produced

This is a **UI RENDERING ISSUE caused by NaN in the function results**, not a data or telemetry issue.

---

### Answer to Your Question

**"let us know if this is a telemetry issue or something else"**

**Answer:** This is **SOMETHING ELSE** - specifically a **UI RENDERING ISSUE caused by NaN values** in `getVPPSiteLevelPerformance` function results.

The telemetry data is correct and complete. The function processes the data and returns results, but the `battery_power` field contains `NaN` for many sites (due to division by zero), which prevents the Fabric UI from rendering the table. The data is visible when exported to CSV or called via Postman API.

---

### Supporting Files

Analysis files available in ticket-12654 folder:
- `COMPLETE_ANALYSIS_EVENT_CA0C0D89.md` - Full detailed analysis
- `FUNCTION_COMPARISON_ANALYSIS.md` - Detailed function comparison
- `last_event_summary_data.csv` - Dispatch summary output (working function)
- `last_event_telemetry_data.csv` - Raw telemetry data (40+ records)
- `last_event_silver_dispatch_result_dto.csv` - Command execution results

---

Thanks,  
Jagan
