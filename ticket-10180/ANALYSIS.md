# Ticket 10180: Analysis - MWh Exports Widget Returns Empty Array

**Program:** DSGS
**Issue:** Widget showing empty array instead of **2.272 MWh**
**Function:** `getVPPExportSummaryByProgram`
**Analyst:** Jagan Murikinati
**Date:** 2026-04-02 (UPDATED - ROOT CAUSE CONFIRMED)

---

## 🎯 **FINAL ROOT CAUSE - CONFIRMED**

**Status:** ✅ **ROOT CAUSE IDENTIFIED AFTER 7-LAYER DEEP TRACE**

**The Problem:**
DSGS program uses a **PASSIVE** monitoring strategy (`CHARGE_FROM_SOLAR`), but the widget architecture is designed exclusively for **ACTIVE** dispatch events that generate command records.

**The Evidence:**
- ✅ Event metadata EXISTS in `silver_stream_dispatch_events`
- ✅ Site telemetry EXISTS in `silverCommDataSite` (2,000+ records)
- ❌ **NO dispatch results in `silver_dispatch_result_dto` (0 ROWS)** ← **ROOT CAUSE**
- ❌ All 7 downstream functions cascade fail from this missing source data
- ❌ Widget returns empty array `[]`

**Why it's empty:**
Passive strategies don't send active commands to sites → No command responses → No records in `silver_dispatch_result_dto` → Entire calculation chain breaks.

---

## 🔬 **THE 7-LAYER DEEP TRACE - COMPLETE DEPENDENCY CHAIN**

We traced the failure through **7 nested layers** of functions to find the actual source of empty data:

### **Layer 7: Widget (Top Layer) - BROKEN**
```
MWh Exports = Energy Delivered Widget
↓ Calls: getVPPExportSummaryByProgram('DSGS')
↓ Result: Empty array []
↓ Evidence: vppexportsummary_dsgs.csv (0 rows)
```

### **Layer 6: Program Summary Function - EMPTY**
```
getVPPExportSummaryByProgram('DSGS')
↓ Queries: silver_dispatch_summary (INNER JOIN)
↓ Result: Empty (INNER JOIN drops all records)
↓ Evidence: getVPPexportsummary_by_program_function.csv
```

### **Layer 5: Summary Table - EMPTY**
```
silver_dispatch_summary
WHERE event_id = '1b55ba12-07eb-4b55-b29c-4947002f04b2'
↓ Populated by: getVPPDispatchSummary()
↓ Result: 0 rows
↓ Evidence: silver_dispatch_summary_dsgs.csv
```

### **Layer 4: Dispatch Summary Function - EMPTY**
```
getVPPDispatchSummary('1b55ba12-07eb-4b55-b29c-4947002f04b2')
↓ Calls: getSiteDispatchCommandSummary()
↓ Result: Empty
↓ Evidence: dispatch_summary_dsgs_event.csv
```

### **Layer 3: Command Summary Function - EMPTY**
```
getSiteDispatchCommandSummary('1b55ba12-07eb-4b55-b29c-4947002f04b2')
↓ Calls: getMultipleEventsSiteDispatchResults()
↓ Result: Empty
↓ Evidence: getSiteDispatchCommandSummary_function.csv
↓ Tested: Returned empty
```

### **Layer 2: Multi-Event Results Function - EMPTY**
```
getMultipleEventsSiteDispatchResults(
    dynamic(['1b55ba12-07eb-4b55-b29c-4947002f04b2']),
    dynamic([])
)
↓ Loops through events calling: getSiteDispatchResults()
↓ Uses: partition by + invoke fxn_wrapper()
↓ Result: Empty (no data from underlying function)
↓ Evidence: getMultipleEventsSiteDispatchResults_function.csv
↓ Tested: Returned empty
```

### **Layer 1: Site Dispatch Results Function - EMPTY**
```
getSiteDispatchResults('1b55ba12-07eb-4b55-b29c-4947002f04b2', dynamic([]))
↓ Queries: silver_dispatch_result_dto (THE SOURCE TABLE)
↓ Result: Empty
↓ Evidence: getSiteDispatchResults_function.csv
↓ Tested: Returned empty
```

### **🚨 Layer 0: SOURCE TABLE - ROOT CAUSE (0 ROWS)**
```
silver_dispatch_result_dto
WHERE event_id = '1b55ba12-07eb-4b55-b29c-4947002f04b2'
↓ Should contain: Dispatch commands/results for each site
↓ Result: 0 ROWS (only headers)
↓ Evidence: silver_dispatch_result_dto_dsgs.csv
↓ THIS IS THE ROOT CAUSE
```

### **Key Finding:**

The entire calculation chain depends on `silver_dispatch_result_dto` having records for each event. For DSGS:
- **Expected:** Records for 400+ sites × multiple timestamps during event
- **Actual:** 0 records
- **Impact:** Every function up the chain returns empty → Widget breaks

---

## 🔍 **FUNCTION ANALYSIS**

### **How getVPPExportSummaryByProgram Works:**

The function queries two tables with an **INNER JOIN**:

```kql
silver_stream_dispatch_events  (Events metadata: program, sites, times)
    ↓
    INNER JOIN
    ↓
silver_dispatch_summary  (Energy calculations: energy_exported)
    ↓
    Filter by program_name = "DSGS"
    ↓
    Aggregate: daily, monthly, yearly, lifetime energy
```

### **The Critical INNER JOIN:**

```kql
silver_stream_dispatch_events
| summarize arg_max(event_processed_utc_time, *) by event_id
| join kind = inner (
    silver_dispatch_summary
    | summarize arg_max(ts_time, *) by event_id
) on $left.event_id == $right.event_id
```

**Why INNER JOIN is a problem:**
- ✅ If event exists in BOTH tables → Returns data
- ❌ If event exists ONLY in `silver_stream_dispatch_events` → **Returns EMPTY**
- ❌ If event exists ONLY in `silver_dispatch_summary` → **Returns EMPTY**

---

## 🎯 **WHY IS `silver_dispatch_result_dto` EMPTY? - THE ARCHITECTURE EXPLANATION**

### **Understanding Active vs Passive Event Strategies:**

The VPP system supports two types of dispatch events:

#### **ACTIVE Dispatch Events** (Command-Driven)
**Examples:** `DISCHARGE_TO_HOME_AND_GRID`, `CHARGE_FROM_GRID`, `SELF_CONSUMPTION`

**How they work:**
1. ✅ Event created in `silver_stream_dispatch_events`
2. ✅ System sends **active commands** to each site
3. ✅ Sites respond with telemetry updates
4. ✅ **Commands + responses stored in `silver_dispatch_result_dto`**
5. ✅ Functions calculate energy from command results
6. ✅ Widget shows energy values

**Data Flow:**
```
Create Event → Send Commands → Sites Respond → Record Results → Calculate Energy → Display
```

---

#### **PASSIVE Monitoring Events** (Observation-Only)
**Examples:** `CHARGE_FROM_SOLAR`

**How they work:**
1. ✅ Event created in `silver_stream_dispatch_events`
2. ✅ Sites charge from solar **naturally** (no commands sent)
3. ✅ Telemetry data flows to `silverCommDataSite`
4. ❌ **NO commands sent = NO dispatch results recorded**
5. ❌ `silver_dispatch_result_dto` remains **empty**
6. ❌ Functions designed for active events **fail**
7. ❌ Widget returns empty array

**Data Flow:**
```
Create Event → Sites Operate Independently → Telemetry Flows → [NO DISPATCH RESULTS] → Functions Fail → Widget Breaks
```

---

### **DSGS Event Details - Confirming Passive Strategy:**

From `silver_stream_dispatch_events_dsgs.csv`:
```csv
dispatch_strategy: "CHARGE_FROM_SOLAR"
dispatch_payload: {"soc_target":100}
```

**What this means:**
- DSGS tells sites: "Charge your batteries from solar to 100% SoC"
- Sites do this **autonomously** using existing solar charging logic
- **No active dispatch commands are sent** every 15 minutes
- System just **monitors** what sites do naturally
- Result: Clean renewable energy charging, but **no command records**

---

### **Why This Broke The Widget:**

**The widget architecture assumes:**
- ✅ Every event has dispatch results in `silver_dispatch_result_dto`
- ✅ Energy calculations come from `max(telemetry) - min(telemetry)` per command
- ✅ Commands define the time windows for aggregation

**DSGS reality:**
- ❌ No dispatch results exist
- ❌ No commands to define aggregation windows
- ❌ Telemetry exists but functions can't access it
- ❌ Widget designed for active events encounters passive event → Fails

---

### **Historical Context - "It Used To Work":**

**HYPOTHESIS:** DSGS previously used an **active** dispatch strategy:

**BEFORE (Widget Worked):**
```
DSGS Strategy: DISCHARGE_TO_HOME_AND_GRID (active)
↓ Commands sent every 15 minutes
↓ Dispatch results recorded
↓ Functions work
↓ Widget shows energy values ✅
```

**AFTER (Widget Broke):**
```
DSGS Strategy: CHARGE_FROM_SOLAR (passive)
↓ No commands sent
↓ No dispatch results
↓ Functions fail
↓ Widget returns empty array ❌
```

**Timeline of Change:**
- Unknown when strategy changed
- Need to ask Ayub/team when DSGS switched to `CHARGE_FROM_SOLAR`
- This would explain why "it used to work"

---

## 🚨 **CONFIRMED ROOT CAUSES**

### **✅ Confirmed: Passive Event Architecture Incompatibility** ⭐ **ROOT CAUSE**

**Evidence:**
- ✅ Event EXISTS: `silver_stream_dispatch_events` has 1 DSGS event
- ✅ Telemetry EXISTS: `silverCommDataSite` has 2,000+ records for 400+ DSGS sites
- ❌ **Dispatch results EMPTY:** `silver_dispatch_result_dto` has 0 rows
- ❌ Strategy is PASSIVE: `CHARGE_FROM_SOLAR` doesn't generate dispatch commands
- ❌ All 7 functions CASCADE FAIL from missing source data

**Why this happens:**
- Widget and all underlying functions are designed exclusively for **ACTIVE** dispatch events
- DSGS uses a **PASSIVE** monitoring strategy
- Passive strategies don't create the dispatch result records that functions expect
- Result: Complete failure of the calculation chain

**Evidence files:**
- `silver_dispatch_result_dto_dsgs.csv` (0 rows - only headers)
- `silver_stream_dispatch_events_dsgs.csv` (strategy = CHARGE_FROM_SOLAR)
- `query6.csv.csv` (2,000+ telemetry records available)

**Why this happens:**
- Sites offline or not communicating
- Configuration issue preventing data ingestion
- Similar to missing battery_200_IncWhExp data in Ticket 12654

**Evidence needed:**
- Run Query 6 to check telemetry data

---

## 📋 **DIAGNOSTIC PLAN**

### **Step 1: Run Diagnostic Queries** ⚠️ **START HERE**

Execute queries in this order:

1. **Query 1:** Check DSGS events in `silver_stream_dispatch_events`
2. **Query 2:** Check DSGS events in `silver_dispatch_summary`
3. **Query 3:** Compare all programs (identify which have missing data)
4. **Query 4:** Get sample DSGS event IDs
5. **Query 5:** Test `getVPPDispatchSummary()` with DSGS event ID
6. **Query 6:** Check telemetry data for DSGS sites

**All queries are in:** `ticket-10180/diagnostic_queries.kql`

---

### **Step 2: Interpret Results**

| Query 1 Result | Query 2 Result | Diagnosis |
|----------------|----------------|-----------|
| 0 events | 0 events | **No DSGS events exist** → Data issue |
| >0 events | 0 events | **Missing dispatch summary** → Processing issue ⭐ |
| >0 events | >0 events | **Different issue** → Run Query 3 & 5 |

---

### **Step 3: Determine Fix**

**If Scenario 1 (Missing Dispatch Summary):**
- Need to backfill `silver_dispatch_summary` for DSGS events
- Run `getVPPDispatchSummary()` for each missing event
- Or fix the ETL/ingestion process that populates this table

**If Scenario 2 (No Events):**
- Investigate why DSGS has no dispatch events
- Check if program name is correct (case sensitive?)
- Look for events with similar names

**If Scenario 4 (No Telemetry):**
- Check site connectivity
- Verify data ingestion pipelines
- Investigate why sites aren't reporting

---

## 🔧 **POTENTIAL SOLUTIONS**

### **Solution A: Change INNER JOIN to LEFT JOIN** ⚠️ **Quick Fix**

**Modify the function:**
```kql
| join kind = leftouter (  // Changed from 'inner'
    silver_dispatch_summary
```

**Result:**
- Events without summary data will appear with `0` energy
- Widget won't be empty anymore
- But doesn't fix the ROOT CAUSE

---

### **Solution B: Backfill Missing Data** ⭐ **Proper Fix**

**Process:**
1. Get all DSGS event IDs from `silver_stream_dispatch_events`
2. For each event, run `getVPPDispatchSummary(event_id)`
3. This populates `silver_dispatch_summary`
4. Function will now return data

---

### **Solution C: Fix Data Ingestion Pipeline**

**Long-term fix:**
- Identify why `silver_dispatch_summary` isn't being populated
- Fix the scheduled job/pipeline that processes events
- Ensure all future events are automatically processed

---

## ✅ **ROOT CAUSE CONFIRMED - SCENARIO 1**

### **Diagnostic Query Results:**

| Query | What It Checks | Result | Status |
|-------|---------------|--------|--------|
| **Query 1** | DSGS events in `silver_stream_dispatch_events` | ✅ **1 event found** | Event ID: `1b55ba12-07eb-4b55-b29c-4947002f04b2` |
| **Query 2** | DSGS events in `silver_dispatch_summary` | ❌ **0 events (empty)** | **NO DATA in summary table** |
| **Direct Query** | `silver_stream_dispatch_events WHERE event_id = "1b55ba12..."` | ✅ **1 row** | Contains 400+ sites, event time: 21:00-22:00 |
| **Direct Query** | `silver_dispatch_summary WHERE event_id = "1b55ba12..."` | ❌ **0 rows (only headers)** | **Confirmed missing** |
| **Function Test** | `getVPPExportSummaryByProgram('DSGS')` | ❌ **Empty array []** | INNER JOIN drops DSGS |
| **Site-Level Test** | `getVPPSiteLevelPerformance(input_event_name='{1b55ba12...}')` | ❌ **Empty response** | Depends on missing summary |

### **Conclusion:**
✅ **Scenario 1 Confirmed:** DSGS event exists in metadata table but **NOT in dispatch summary table**

---

## 🔍 **WHY THE WIDGET STOPPED WORKING**

### **The Data Pipeline Gap:**

```
┌────────────────────────────────────────────────────────────────┐
│  Event Creation (DSGS dispatch event created on 2026-02-11)   │
│  ✅ Stored in: silver_stream_dispatch_events                   │
└────────────────────────────────────────────────────────────────┘
                              │
                              ↓
┌────────────────────────────────────────────────────────────────┐
│  Energy Calculation Pipeline (SHOULD RUN)                     │
│  ❌ FAILED or NEVER RAN for DSGS                              │
│  Should call: getVPPDispatchSummary(event_id)                │
│  Should calculate: energy_exported, energy_charged, etc.      │
└────────────────────────────────────────────────────────────────┘
                              │
                              ↓
┌────────────────────────────────────────────────────────────────┐
│  Summary Storage                                               │
│  ❌ NOT stored in: silver_dispatch_summary                    │
└────────────────────────────────────────────────────────────────┘
                              │
                              ↓
┌────────────────────────────────────────────────────────────────┐
│  Widget Query: getVPPExportSummaryByProgram('DSGS')           │
│  ❌ INNER JOIN finds no match → Returns []                    │
└────────────────────────────────────────────────────────────────┘
```

**The widget used to work → Something changed in the data pipeline → Now DSGS summaries aren't being calculated**

---

## 🔍 **AYUB'S COMMENT ANALYSIS**

**Ayub said:**
> "This value (2,272.16 kWh / 2.272 MWh) is retrieved from the Fabric function `getVPPSiteLevelPerformance(input_event_name='{eventId}')` at the event level."

**But when we tested:**
```kql
getVPPSiteLevelPerformance(input_event_name='{1b55ba12-07eb-4b55-b29c-4947002f04b2}')
```
**Result:** ❌ Empty response

**Why?** Looking at `getVPPSiteLevelPerformance_function.csv` (line 38):
```kql
let eventData =
    getSiteDispatchCommandSummary(inputEventIds = pack_array(input_event_name))
```

This function depends on `getSiteDispatchCommandSummary()` which likely:
- Calculates energy from raw telemetry data
- But the **calculated results aren't stored** in `silver_dispatch_summary`
- So both functions return empty

**Key Insight:** Ayub might have seen 2.272 MWh **when the widget was working**, but that data is **no longer accessible** because it wasn't stored properly or was lost.

---

## 🚀 **RECOMMENDED FIX - TWO-PART SOLUTION**

### **Part 1: Quick Fix (Stop Empty Array)** ⚡

**Change the function to use LEFT JOIN:**

```kql
// Current (line 42-45 in function):
| join kind = inner (
    silver_dispatch_summary
    | summarize arg_max(ts_time, *) by event_id
) on $left.event_id == $right.event_id

// Change to:
| join kind = leftouter (
    silver_dispatch_summary
    | summarize arg_max(ts_time, *) by event_id
) on $left.event_id == $right.event_id
| extend energy_exported = coalesce(energy_exported, 0.0)
| extend energy_charged = coalesce(energy_charged, 0.0)
| extend energy_discharged = coalesce(energy_discharged, 0.0)
```

**Impact:**
- ✅ Widget shows DSGS with `0 MWh` instead of empty array
- ✅ Prevents widget from breaking for ANY program with missing summaries
- ❌ Doesn't show the actual 2.272 MWh (shows 0 instead)

---

### **Part 2: Proper Fix (Backfill Data)** 🎯

**Investigate and fix the data pipeline:**

1. **Find out WHY `silver_dispatch_summary` is empty for DSGS:**
   - Is there a scheduled pipeline that should populate this table?
   - Did it fail for DSGS specifically?
   - Is there an error in the processing logs?

2. **Options to backfill the data:**

   **Option A:** Run the summary function manually and INSERT results
   ```kql
   // Get the calculated summary (we already have this in dispatch_summary_dsgs_event.csv)
   getVPPDispatchSummary("1b55ba12-07eb-4b55-b29c-4947002f04b2")

   // Then INSERT into silver_dispatch_summary
   // (Need INSERT permissions and proper KQL syntax)
   ```

   **Option B:** Find and re-run the ETL pipeline
   - Locate the pipeline that processes dispatch events
   - Re-run it for the DSGS event
   - Verify it populates `silver_dispatch_summary`

   **Option C:** Contact data engineering team
   - Ask why DSGS events aren't being processed
   - Request backfill of all missing DSGS dispatch summaries

---

## 📊 **NEXT ACTIONS**

### **Immediate (Today):**
1. ✅ **Root cause confirmed** - DSGS event exists but has no dispatch summary
2. ⏳ **Decision needed:** Quick fix (LEFT JOIN) or wait for proper fix (backfill)?
3. ⏳ **Ask Ayub:**
   - "Where did you see the 2.272 MWh value? Was it in this widget before?"
   - "Is there a pipeline that should auto-populate `silver_dispatch_summary`?"
   - "Do you want me to modify the function to use LEFT JOIN as a quick fix?"

### **Short-term (This Week):**
4. ⏳ **Investigate data pipeline** - Why isn't `silver_dispatch_summary` being populated?
5. ⏳ **Implement fix** - Either change JOIN type or backfill data
6. ⏳ **Test** - Verify widget shows correct values

### **Long-term:**
7. ⏳ **Monitor** - Ensure future DSGS events are processed correctly
8. ⏳ **Alert** - Set up monitoring for missing dispatch summaries

---

## 📎 **FILES CREATED/ANALYZED**

| File | Purpose | Status |
|------|---------|--------|
| `diagnostic_queries.kql` | 6 diagnostic queries | ✅ Executed |
| `query1.csv.csv` | DSGS events in events table | ✅ 1 event found |
| `query2.csv.csv` | DSGS events in summary table | ❌ 0 events |
| `silver_stream_dispatch_events_dsgs.csv` | Raw event data | ✅ Has data |
| `silver_dispatch_summary_dsgs.csv` | Summary data | ❌ Only headers |
| `vppexportsummary_dsgs.csv` | Function output | ❌ Empty array |
| `getVPPSiteLevelPerformance_function.csv` | Function definition | ✅ Analyzed |
| `ANALYSIS.md` | This comprehensive analysis | ✅ Updated |

---

## 💬 **KEY QUESTIONS FOR STAKEHOLDERS**

**For Ayub Shirgaonkar:**
1. **Where did you see the 2.272 MWh value?** Was it in this widget before, or from a different source?
2. **When did this widget last work for DSGS?** Do you have a date/timestamp?
3. **Is there a scheduled pipeline** that should populate `silver_dispatch_summary` automatically?
4. **Should I implement the quick fix** (LEFT JOIN) so the widget at least shows `0` instead of breaking?

**For Data Engineering Team:**
5. **Why is `silver_dispatch_summary` empty for DSGS events?** Is there an ETL failure?
6. **Can we backfill the missing data?** Do you have logs showing why it wasn't processed?
7. **How are dispatch summaries supposed to be populated?** Manual function call or automated pipeline?


