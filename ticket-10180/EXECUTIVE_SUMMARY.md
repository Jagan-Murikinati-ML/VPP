# 🎯 Ticket 10180 - Executive Summary

**To:** Ayub Shirgaonkar, Naveen  
**From:** Jagan Murikinati  
**Date:** 2026-04-02  
**Subject:** ROOT CAUSE IDENTIFIED - MWh Exports Widget Empty Array Issue

---

## ⚡ **TL;DR - 60 Second Summary**

**The Problem:**
MWh Exports widget returns empty array `[]` for DSGS program instead of showing energy values.

**The Root Cause:**
The entire widget calculation chain depends on data in `silver_dispatch_result_dto` table. For the DSGS event (strategy: `CHARGE_FROM_SOLAR`), this table has **0 rows**. Every function in the 7-layer chain queries this empty table → Complete cascade failure.

**The Evidence:**
- ✅ Event metadata EXISTS in `silver_stream_dispatch_events`
- ✅ Site telemetry EXISTS in `silverCommDataSite` (2,000+ records)
- ❌ `silver_dispatch_result_dto` has **0 ROWS** for DSGS event
- ❌ All 7 downstream functions return empty

**Need Guidance On:**
Is `CHARGE_FROM_SOLAR` strategy supposed to populate `silver_dispatch_result_dto`?
- If YES → Fix data pipeline issue
- If NO → Build alternative calculation from telemetry

---

## 📊 **THE DISCOVERY - 7-Layer Deep Trace**

I traced the failure through the complete function dependency chain:

```
Layer 7: Widget → Empty []
Layer 6: getVPPExportSummaryByProgram() → Empty
Layer 5: silver_dispatch_summary table → 0 rows
Layer 4: getVPPDispatchSummary() → Empty
Layer 3: getSiteDispatchCommandSummary() → Empty
Layer 2: getMultipleEventsSiteDispatchResults() → Empty
Layer 1: getSiteDispatchResults() → Empty
Layer 0: silver_dispatch_result_dto table → 0 ROWS ← ROOT CAUSE
```

**Why Layer 0 is empty:**  
DSGS strategy = `CHARGE_FROM_SOLAR` = passive monitoring = no commands sent = no dispatch results recorded

---

## 🔬 **THE DATA GAP**

### **What's Available:**
- ✅ Event metadata in `silver_stream_dispatch_events`
  - Event ID: `1b55ba12-07eb-4b55-b29c-4947002f04b2`
  - Strategy: `CHARGE_FROM_SOLAR`
  - Sites: 400+
  - Time: 2026-02-11 21:00-22:00 UTC

- ✅ Site telemetry in `silverCommDataSite`
  - 2,000+ records for DSGS sites
  - Power, energy, SoC data available

### **What's Missing:**
- ❌ `silver_dispatch_result_dto` has **0 ROWS** for this event
  - This table is the foundation for ALL energy calculations
  - All functions query this table
  - Empty table = empty results at every layer

### **The Question:**
**Is this table SUPPOSED to have data for `CHARGE_FROM_SOLAR` events?**
- If YES → Something broke in the data pipeline
- If NO → Widget needs a different calculation method

---

## ✅ **WHAT WE KNOW FOR CERTAIN**

| Component | Status | Evidence |
|-----------|--------|----------|
| Event Metadata | ✅ EXISTS | 1 DSGS event in `silver_stream_dispatch_events` |
| Site Telemetry | ✅ EXISTS | 2,000+ records for 400+ sites in `silverCommDataSite` |
| Dispatch Results | ❌ **EMPTY** | 0 rows in `silver_dispatch_result_dto` |
| Event Strategy | `CHARGE_FROM_SOLAR` | Passive monitoring (no commands) |
| Widget Output | ❌ **BROKEN** | Empty array `[]` instead of energy value |

**Event ID Tested:** `1b55ba12-07eb-4b55-b29c-4947002f04b2`  
**Event Time:** 2026-02-11 21:00:00 to 22:00:00 UTC  
**Sites:** 400+ DSGS sites

---

## 💡 **SOLUTION OPTIONS - NEED YOUR GUIDANCE**

### **Option 1: Fix Data Pipeline** 🔧

**If `CHARGE_FROM_SOLAR` SHOULD populate `silver_dispatch_result_dto`:**

**Approach:**
- Investigate why dispatch results are not being recorded
- Find and fix the ETL/pipeline process
- Backfill missing data for DSGS events

**Pros:**
- ✅ Fixes root cause permanently
- ✅ Widget shows actual energy values
- ✅ Prevents future occurrences

**Cons:**
- ⏳ Requires pipeline investigation
- ❓ Need to identify where/how table is populated

**Estimated Time:** Varies based on pipeline complexity

---

### **Option 2: Alternative Calculation** 🎯

**If `CHARGE_FROM_SOLAR` does NOT populate `silver_dispatch_result_dto`:**

**Approach:**
- Calculate energy directly from `silverCommDataSite` telemetry
- Use event start/end time to filter telemetry window
- Aggregate: `max(energy) - min(energy)` per site

**Example Logic:**
```kql
silverCommDataSite
| where siteId in (event_sites)
| where sourceTimestamp between (event_start .. event_end)
| summarize
    energy_exported = max(grid_200_IncWhExp) - min(grid_200_IncWhExp)
  by siteId
| summarize total = sum(energy_exported)
```

**Pros:**
- ✅ Shows actual energy values from telemetry
- ✅ Works for events without dispatch results
- ✅ No pipeline investigation needed

**Cons:**
- ⏳ Requires function development/modification (2-3 days)
- ❓ Need to confirm calculation accuracy

**Estimated Time:** 2-3 days

---

### **Option 3: Temporary Fix (LEFT JOIN)** ⚡

**Prevent widget from breaking while investigating:**

**Approach:**
- Change INNER JOIN to LEFT JOIN in function
- Show `0 MWh` instead of empty array `[]`

**Pros:**
- ✅ Quick (15 minutes)
- ✅ Widget doesn't crash

**Cons:**
- ❌ Shows `0` instead of actual energy
- ❌ Doesn't fix root cause
- ⚠️ Temporary only

**Estimated Time:** 15 minutes

**Use Case:** Deploy while investigating Option 1 or 2

---

## ❓ **QUESTIONS FOR YOU**

### **1. Event Type Intent:**
Is DSGS intended to be:
- **A) PASSIVE** (monitor solar charging, no commands) → Need Option 1
- **B) ACTIVE** (send charge commands, record results) → Need Option 2

### **2. The 2.272 MWh Value:**
You mentioned this value comes from `getVPPSiteLevelPerformance()`, but our tests show:
- All functions return empty for this event
- `silver_dispatch_result_dto` has 0 rows

**Where did you actually see 2.272 MWh?**  
(Different event? Manual calculation? Different widget?)

### **3. Historical Timeline:**
- When did this widget last work for DSGS?
- Did DSGS previously use a different strategy (e.g., `DISCHARGE_TO_HOME_AND_GRID`)?
- When did it switch to `CHARGE_FROM_SOLAR`?

### **4. Preferred Solution:**
Which option aligns with product strategy?

---

## 📎 **ALL EVIDENCE ATTACHED**

Complete investigation files in folder: **`ticket-10180/`**

Key files:
- `SUMMARY_FOR_ADO.md` - Detailed summary for ADO ticket
- `ANALYSIS.md` - Complete technical deep-dive (7-layer trace)
- `silver_dispatch_result_dto_dsgs.csv` - Proof of 0 rows (root cause)
- `silver_stream_dispatch_events_dsgs.csv` - Event metadata
- `query6.csv.csv` - Telemetry data proof
- All function definitions and test results

---

## 🚀 **RECOMMENDED NEXT STEPS**

**Once you confirm the event type and preferred solution:**

1. ✅ I'll implement the chosen solution
2. ✅ Test with the DSGS event
3. ✅ Validate widget shows expected energy values
4. ✅ Document the fix in ADO ticket
5. ✅ Deploy to production

**Ready to proceed once I get your input!** 🎯


