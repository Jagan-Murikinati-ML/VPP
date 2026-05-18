# ADO Ticket Comment - Event Investigation Results

---

## 📋 Investigation Complete - Event ca0c0d89-614d-4358-b31f-2cb27a29cf5f

Hi @Shaun Roach,

I've completed the investigation you requested. Here are my findings:

---

### Summary

**This is a FUNCTION LOGIC ISSUE, not a telemetry issue.**

---

### Function Comparison Results

**1. getVPPSiteLevelPerformance:**
```kusto
getVPPSiteLevelPerformance(input_event_name='ca0c0d89-614d-4358-b31f-2cb27a29cf5f')
```
**Result:** ❌ Returns **0 rows** (NO DATA)

**2. getVPPDispatchSummary:**
```kusto
getVPPDispatchSummary("ca0c0d89-614d-4358-b31f-2cb27a29cf5f")
```
**Result:** ✅ Returns **4 rows** with aggregated data
- 606 participating sites
- 3.14 MWh total energy discharged
- Data broken down by 15-min intervals

---

### Site Command Execution Status

| Site ID | Status | Reason |
|---------|--------|--------|
| 400029108 | ❌ Failed | "startTime must be in the future" (400 error) |
| 400031093 | ❌ Failed | Device control failure - connector issue (500 error, 11 retries) |
| 400032980 | ✅ Success | Command executed successfully |
| 400033526 | ✅ Success | Command executed successfully |

---

### Telemetry Analysis (Successful Sites Only)

**Site 400032980 (SolarEdge):**
- Command: ✅ Success
- Battery SOC: 0.24% (constant - battery was already empty)
- Energy Discharged: 0 Wh
- Reason: Battery depleted, couldn't discharge despite successful command

**Site 400033526 (Tesla):**
- Command: ✅ Success  
- Battery SOC: 14.23% → 13.52% (dropped 0.71%)
- Energy Discharged: Minimal (very small kWh based on 0.71% SOC drop)
- Telemetry: All data present and accurate

---

### Root Cause

**The `getVPPSiteLevelPerformance` function is broken:**
1. Returns NO DATA for this event
2. `getVPPDispatchSummary` works correctly for the same event
3. UI likely calls `getVPPSiteLevelPerformance` which returns nothing
4. When function returns no data, UI shows "-" or minimal values (0.1 kWh)

**This is the SAME ISSUE as Ticket #12654** - site-level performance function fails while summary function works.

---

### Telemetry Status

✅ **Telemetry data is CORRECT:**
- Raw data exists in silverCommDataSite for all successful sites
- SOC values are accurate
- Energy values match battery behavior
- Failed sites correctly show no data (commands failed)

❌ **Problem is NOT telemetry - it's the FUNCTION LOGIC**

---

### Recommendation

1. **Investigate `getVPPSiteLevelPerformance` function code** - compare with working `getVPPDispatchSummary`
2. **Check table joins and filtering logic** - function may be filtering out data incorrectly
3. **Fix the function** to return site-level performance data like dispatch summary does

---

### Supporting Files

Generated analysis files:
- `ticket-12654/COMPLETE_ANALYSIS_EVENT_CA0C0D89.md` - Full detailed analysis
- `last_event_summary_data.csv` - Dispatch summary output
- `last_event_telemetry_data.csv` - Raw telemetry data
- `last_event_silver_dispatch_result_dto.csv` - Command execution results

---

**Your Question:** "let us know if this is a telemetry issue or something else"

**Answer:** This is **SOMETHING ELSE** - specifically a **FUNCTION LOGIC ISSUE** in `getVPPSiteLevelPerformance`. Telemetry data is correct and complete.

Thanks,
Jagan
