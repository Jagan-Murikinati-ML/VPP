# Investigation Findings: Event ca0c0d89-614d-4358-b31f-2cb27a29cf5f

**Investigated by:** Jagan Murikinati  
**Date:** May 14, 2026  
**Tickets:** #10180, #12654, #15308

---

## 📋 Summary

Investigated the energy discharge discrepancy for event `ca0c0d89-614d-4358-b31f-2cb27a29cf5f` as requested by Shaun Roach.

**Key Finding:** `getVPPSiteLevelPerformance` function returns **NO DATA** while `getVPPDispatchSummary` returns aggregated data.

---

## 🔍 Investigation Details

### Event Information
- **Event ID:** `ca0c0d89-614d-4358-b31f-2cb27a29cf5f`
- **Program:** DSGS
- **Event Start:** 2026-05-12 07:15:00 UTC
- **Event End:** 2026-05-12 08:15:00 UTC
- **Strategy:** discharge
- **Sites in Event:** 4 sites (400029108, 400031093, 400032980, 400033526)
- **Event Duration:** 60 minutes

---

### Sites Command Status (from silver_dispatch_result_dto)

Based on Shaun's findings:

| Site ID | Command Status | Reason |
|---------|---------------|--------|
| 400029108 | ❌ Failed | Bad event parameters (start time in past) |
| 400031093 | ❌ Failed | Connector team issue |
| 400032980 | ✅ Succeeded | Command executed |
| 400033526 | ✅ Succeeded | Command executed |

**Sites for Analysis:** 400032980, 400033526 (successful commands only)

---

## 📊 Function Comparison Results

### 1. getVPPSiteLevelPerformance Function
```kusto
getVPPSiteLevelPerformance(input_event_name='ca0c0d89-614d-4358-b31f-2cb27a29cf5f')
```

**Result:** ❌ **NO DATA RETURNED**

---

### 2. getVPPDispatchSummary Function
```kusto
getVPPDispatchSummary("ca0c0d89-614d-4358-b31f-2cb27a29cf5f")
```

**Result:** ✅ **DATA RETURNED** (4 rows - see `last_event_summary_data.csv`)

| Timestamp | Energy Discharged (Wh) | Energy Charged (Wh) | Sites Participation |
|-----------|------------------------|---------------------|---------------------|
| 07:15:00 | 831,647 | 9,353 | 606 |
| 07:30:00 | 1,700,049 | 19,155 | 606 |
| 07:45:00 | 2,451,651 | 27,536 | 606 |
| 08:00:00 | 3,136,302 | 36,052 | 606 |

**Total Energy Discharged:** ~3.14 MWh (3,136,302 Wh)

---

## 🔬 Raw Telemetry Analysis

### Site 400032980 (SolarEdge)
- **Telemetry Records:** 10 records between 07:15 - 08:15
- **battery_200_IncWhExp:** 0 Wh (all records)
- **battery_713_SoC:** 0.24% (constant - battery nearly empty!)
- **Observation:** Battery did NOT discharge (SOC remained constant at 0.24%)

### Site 400033526 (Tesla)
- **Telemetry Records:** 27 records between 07:15 - 08:15
- **battery_200_IncWhExp:** Minimal values (0-4 Wh per record)
- **battery_713_SoC:** 14.23% → 13.52% (dropped 0.71%)
- **Observation:** Very minimal battery discharge despite SOC drop

### Site 400029108 (Enphase)
- **Command Status:** Failed
- **Telemetry Records:** 3 records
- **Observation:** Not analyzed (command failed)

### Site 400031093
- **Command Status:** Failed
- **Telemetry Records:** None in this time window
- **Observation:** Not analyzed (command failed)

---

## 🚨 Root Cause Analysis

### Issue #1: getVPPSiteLevelPerformance Returns NO DATA

**Possible Causes:**
1. Function filters sites based on command success but may be using wrong table
2. Function joins may be failing for this specific event
3. Function may require data in a different format/table than available
4. Time window filtering logic may be incorrect

**Evidence:**
- `getVPPDispatchSummary` works (returns 606 participating sites)
- `getVPPSiteLevelPerformance` fails (returns 0 rows)
- This is the **SAME ISSUE** as ticket #12654

---

### Issue #2: UI Showing 0.1 kWh vs Expected Discharge

**Kushal's Report:** SOC dropped from 53% → 15% but UI shows only 0.1 kWh

**Our Findings:**
- **getVPPDispatchSummary** shows 3.14 MWh total energy discharged for the entire event
- **Raw telemetry** for the 2 successful sites (400032980, 400033526) shows minimal discharge
- **606 sites participated** according to summary (not just the 4 test sites!)

**Explanation:**
- The 4 sites Kushal mentioned are just **test sites** or specific sites being monitored
- The actual event had **606 participating sites** 
- The 3.14 MWh discharge is spread across all 606 sites, not just the 4 test sites
- Site 400032980 battery was already nearly empty (0.24% SOC)
- Site 400033526 had minimal discharge (0.71% SOC drop)

---

## 💡 Conclusion

### Primary Issue:
**`getVPPSiteLevelPerformance` function is broken** - returns NO DATA for this event

### Secondary Issue:
The UI is likely calling `getVPPSiteLevelPerformance` which returns nothing, hence showing "-" or minimal values

### This is NOT a telemetry issue - this is a FUNCTION LOGIC issue

---

## 📝 Recommendation

1. **Investigate `getVPPSiteLevelPerformance` function logic:**
   - Check table joins
   - Check filtering conditions
   - Compare with working `getVPPDispatchSummary` function

2. **Fix the function** to return site-level data similar to how dispatch summary works

3. **Root cause is same as Ticket #12654** - site-level performance function fails while summary function works

---

## 📎 Supporting Files

- `last_event_silver_stream_dispatch_events.csv` - Event metadata
- `last_event_summary_data.csv` - getVPPDispatchSummary output
- `last_event_telemetry_data.csv` - Raw silverCommDataSite telemetry

---

**Next Steps:** Need to analyze `getVPPSiteLevelPerformance` function code to identify why it returns no data.
