@Ayub Shirgaonkar @Naveen - I've completed the investigation on the MWh Exports widget issue for DSGS program.

---

## 🎯 **Root Cause Identified**

The widget returns an empty array `[]` because the entire calculation chain depends on data in the `silver_dispatch_result_dto` table. For the DSGS event (ID: `1b55ba12-07eb-4b55-b29c-4947002f04b2`), this table has **0 rows**.

**What I traced:**
- Started from the widget → `getVPPExportSummaryByProgram('DSGS')`
- Traced through 7 nested functions
- Found that every function queries `silver_dispatch_result_dto` as the source
- This table is empty for the DSGS event → All functions return empty → Widget breaks

---

## 📊 **What's Available vs Missing**

**Available (✅):**
- Event metadata in `silver_stream_dispatch_events` 
  - Event ID: `1b55ba12-07eb-4b55-b29c-4947002f04b2`
  - Strategy: `CHARGE_FROM_SOLAR`
  - Sites: 400+, Time: 2026-02-11 21:00-22:00 UTC
- Site telemetry in `silverCommDataSite` (2,000+ records with power/energy data)

**Missing (❌):**
- `silver_dispatch_result_dto` → **0 rows** for this event
- This is the foundation table for all energy calculations
- Without this data, every downstream function fails

---

## ❓ **Need Guidance**

**Key Question:**  
Is `CHARGE_FROM_SOLAR` dispatch strategy **supposed to** populate `silver_dispatch_result_dto` table?

**If YES (Pipeline Issue):**
- There's a bug in the data pipeline/ETL process
- Need to investigate why dispatch results aren't being recorded
- Need to identify and fix the pipeline, then backfill data

**If NO (Different Calculation Needed):**
- The widget's current architecture doesn't support this strategy
- Need to build alternative calculation using telemetry from `silverCommDataSite`
- Calculate energy as: `max(grid_200_IncWhExp) - min(grid_200_IncWhExp)` during event window

---

## 🚀 **Proposed Next Steps**

**Option 1 - Temporary Fix (15 min):**
- Change INNER JOIN to LEFT JOIN in `getVPPExportSummaryByProgram`
- Widget shows `0 MWh` instead of empty array
- Prevents widget from breaking while we investigate proper fix

**Option 2 - Proper Fix (depends on answer above):**
- If pipeline issue → Fix ETL process
- If different calc needed → Modify function to calculate from telemetry

---

## 📎 **Supporting Evidence**

I've documented the complete investigation in the repository folder `ticket-10180/` with:
- All diagnostic query results
- Function definitions traced
- Evidence of empty `silver_dispatch_result_dto` table
- Technical analysis document

**Please advise:**
1. Should `CHARGE_FROM_SOLAR` populate `silver_dispatch_result_dto`?
2. Which solution path should I pursue?
3. Should I deploy the temporary fix while we investigate?

Ready to implement once I get your direction. Thanks!

