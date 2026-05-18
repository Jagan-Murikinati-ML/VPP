# Ticket 10180 - Investigation Summary

**Analyst:** Jagan Murikinati
**Date:** 2026-04-02
**Status:** ✅ Root Cause Identified - PASSIVE EVENT INCOMPATIBILITY
**Program:** DSGS
**Issue:** MWh Exports widget returns empty array `[]`

---

## 🎯 **ROOT CAUSE IDENTIFIED - PASSIVE VS ACTIVE EVENTS**

The `getVPPExportSummaryByProgram('DSGS')` function returns an empty array because:

### **The Core Issue:**

**DSGS uses a PASSIVE monitoring strategy (`CHARGE_FROM_SOLAR`), but the widget is designed for ACTIVE dispatch events.**

### **What We Found:**

1. ✅ **DSGS dispatch event EXISTS** in `silver_stream_dispatch_events`
   - Event ID: `1b55ba12-07eb-4b55-b29c-4947002f04b2`
   - Event time: 2026-02-11 21:00:00 to 22:00:00 UTC
   - Strategy: `CHARGE_FROM_SOLAR` (passive)
   - 400+ sites included

2. ✅ **Site telemetry data EXISTS** in `silverCommDataSite`
   - 2,000+ telemetry records for DSGS sites
   - Power, energy, SoC data available
   - Data exists during event window

3. ❌ **NO dispatch results recorded** in `silver_dispatch_result_dto` table
   - **0 rows for DSGS event** (only column headers)
   - Passive strategy = no commands sent to sites
   - No commands = no dispatch results recorded

4. ❌ **ALL downstream functions fail:**
   - `getSiteDispatchResults()` → Empty (no source data)
   - `getMultipleEventsSiteDispatchResults()` → Empty
   - `getSiteDispatchCommandSummary()` → Empty
   - `getVPPDispatchSummary()` → Empty
   - `silver_dispatch_summary` table → Empty
   - `getVPPExportSummaryByProgram()` → Empty array `[]`

---

## 📊 **INVESTIGATION DETAILS**

### **Complete Function Chain Analysis:**

| Layer | Function/Table | Result | Evidence File |
|-------|---------------|--------|---------------|
| **Event Metadata** | `silver_stream_dispatch_events` | ✅ 1 row | `silver_stream_dispatch_events_dsgs.csv` |
| **Telemetry Data** | `silverCommDataSite` (400+ sites) | ✅ 2,000+ rows | `query6.csv.csv` |
| **🚨 ROOT CAUSE** | `silver_dispatch_result_dto` | ❌ **0 ROWS** | `silver_dispatch_result_dto_dsgs.csv` |
| **Layer 1** | `getSiteDispatchResults()` | ❌ Empty | Tested - returned empty |
| **Layer 2** | `getMultipleEventsSiteDispatchResults()` | ❌ Empty | Tested - returned empty |
| **Layer 3** | `getSiteDispatchCommandSummary()` | ❌ Empty | Tested - returned empty |
| **Layer 4** | `getVPPDispatchSummary()` | ❌ Empty | `dispatch_summary_dsgs_event.csv` |
| **Layer 5** | `silver_dispatch_summary` table | ❌ 0 rows | `silver_dispatch_summary_dsgs.csv` |
| **Layer 6** | `getVPPExportSummaryByProgram('DSGS')` | ❌ Empty `[]` | `vppexportsummary_dsgs.csv` |
| **Layer 7** | `getVPPSiteLevelPerformance()` | ❌ Empty | Tested - returned empty |
| **Widget** | MWh Exports = Energy Delivered | ❌ **BROKEN** | Shows empty array |

### **Why This Stopped Working:**

**The Data Gap:**

**What We Know:**
- ✅ DSGS event exists with strategy `CHARGE_FROM_SOLAR`
- ✅ Site telemetry data is being collected
- ❌ `silver_dispatch_result_dto` table has **0 rows** for this event
- ❌ Widget depends on this table → No data → Returns empty array

**What We Don't Know:**
- ❓ Is `CHARGE_FROM_SOLAR` strategy **supposed to** populate `silver_dispatch_result_dto`?
- ❓ Or does this strategy work differently than other dispatch strategies?
- ❓ Did DSGS previously use a different strategy that DID populate this table?
- ❓ Is there a data pipeline issue, or is this expected behavior?

**Key Insight:** The widget's entire calculation chain depends on `silver_dispatch_result_dto` having data. If this strategy doesn't populate that table (by design or by bug), the widget cannot function.

---

## 🚀 **SOLUTION OPTIONS - NEED GUIDANCE**

### **Option 1: Fix the Data Pipeline** 🔧

**If `CHARGE_FROM_SOLAR` is SUPPOSED to populate `silver_dispatch_result_dto`:**

**Approach:**
- Investigate why dispatch results are not being recorded
- Find and fix the data pipeline/ETL process
- Backfill missing data for DSGS event(s)

**Impact:**
- ✅ Fixes root cause permanently
- ✅ Widget shows actual energy values
- ✅ Prevents future occurrences
- ⏳ Requires pipeline investigation and fix

**Questions to answer:**
- Where is `silver_dispatch_result_dto` populated?
- Is there an ETL job that should be running?
- Are there error logs for DSGS event processing?

---

### **Option 2: Alternative Calculation Method** 🎯

**If `CHARGE_FROM_SOLAR` is NOT supposed to populate `silver_dispatch_result_dto`:**

**Approach:**
- Calculate energy directly from `silverCommDataSite` telemetry
- Use event start/end time to filter telemetry window
- Compute energy exported/imported from cumulative readings
- Works for events WITHOUT dispatch result records

**Approach Example:**
```kql
// Calculate energy from telemetry when dispatch results missing
let eventTelemetry =
    database('EventHouse').silverCommDataSite
    | where siteId in (event_sites)
    | where sourceTimestamp between (event_start .. event_end)
    | summarize
        energy_exported = max(grid_200_IncWhExp) - min(grid_200_IncWhExp),
        energy_imported = max(grid_200_IncWhImp) - min(grid_200_IncWhImp)
    by siteId
    | summarize
        total_energy_exported = sum(energy_exported),
        total_energy_imported = sum(energy_imported)
;
```

**Impact:**
- ✅ Shows actual energy values from telemetry
- ✅ Works for events without dispatch results
- ✅ No pipeline investigation needed
- ⏳ Requires function development/modification
- ❓ Need to confirm this approach is acceptable

**Questions to answer:**
- Is this calculation method accurate?
- Does this align with business requirements?
- Should we support both calculation methods?

---

### **Option 3: Quick Temporary Fix (LEFT JOIN)** ⚡

**Change INNER JOIN to LEFT JOIN to prevent widget from breaking:**

```kql
| join kind = leftouter (  // Changed from 'inner'
    silver_dispatch_summary
) on event_id
| extend energy_exported = coalesce(energy_exported, 0.0)
```

**Impact:**
- ✅ Widget shows `0 MWh` instead of empty array `[]`
- ✅ Can be deployed in 15 minutes
- ❌ Shows `0` instead of actual energy value
- ❌ Doesn't fix root cause
- ⚠️ Temporary measure only

**Estimated Time:** 15 minutes

**Use case:** Deploy this while investigating proper fix (Option 1 or 2)

---

## ❓ **CRITICAL QUESTIONS FOR AYUB/NAVEEN**

@Ayub Shirgaonkar @Naveen - **We've identified the root cause. Need your guidance on next steps:**

### **1. Understanding `CHARGE_FROM_SOLAR` Strategy:**

**Question:** For events with `CHARGE_FROM_SOLAR` dispatch strategy:
- **A) SHOULD** `silver_dispatch_result_dto` be populated with dispatch results?
- **B) Should NOT** be populated (different calculation method needed)?

**Why this matters:**
- If **A (SHOULD)**: There's a data pipeline bug → Need to fix ETL process
- If **B (Should NOT)**: Widget needs alternative calculation → Need to modify function

---

### **2. The 2.272 MWh Value:**

You mentioned:
> "This value (2,272.16 kWh / 2.272 MWh) is retrieved from the Fabric function `getVPPSiteLevelPerformance(input_event_name='{eventId}')`"

**But our tests show:**
- ✅ `getVPPSiteLevelPerformance('{1b55ba12...}')` → **Empty response**
- ✅ All energy calculation functions → **Empty**
- ✅ `silver_dispatch_result_dto` table → **0 rows**

**Questions:**
- Where did you actually see the 2.272 MWh value?
- Was it from a **different event** or **different time period**?
- Was it calculated manually from telemetry?
- Or from a different widget/report?

---

### **3. Historical Context:**

**Questions:**
- When did this widget **last work** for DSGS? (Approximate date)
- Has DSGS **always** used `CHARGE_FROM_SOLAR` strategy?
- Or did it use a different strategy before?

**This helps us understand:**
- Whether this is a new issue or long-standing
- Whether something changed recently to break it
- What the expected behavior should be

---

### **4. Preferred Solution Path:**

Given the three options:

| Option | When to Use | Time | What It Does |
|--------|-------------|------|--------------|
| **1** | Pipeline bug | Varies | Fix ETL process populating `silver_dispatch_result_dto` |
| **2** | Different calc needed | 2-3 days | Calculate from telemetry instead of dispatch results |
| **3** | Temporary measure | 15 min | Prevent widget crash (shows 0) |

**Question:** Which path should we pursue?

---

### **5. Business Impact:**

**Questions:**
- How critical is this widget for DSGS program?
- Are stakeholders asking for this data?
- What's the acceptable timeline for a fix?
- Should we show "No data available" vs "0 MWh" vs "Calculate differently"?

---

## 📎 **NEXT STEPS**

**Awaiting Decision:**
- [ ] Approval to deploy Quick Fix (LEFT JOIN)
- [ ] Guidance on who owns the `silver_dispatch_summary` pipeline
- [ ] Timeline expectations for proper fix

**Once Approved:**
- [ ] Implement selected solution
- [ ] Test in Fabric environment
- [ ] Validate widget shows expected results
- [ ] Document the fix in ADO

---

**All investigation files attached in folder:** `ticket-10180/`

