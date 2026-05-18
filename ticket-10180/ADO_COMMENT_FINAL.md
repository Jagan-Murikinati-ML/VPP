@Naveen @Ayub - I have completed the investigation on the MWh Exports widget issue for DSGS program.

---

## Root Cause

The widget returns an empty array `[]` because `getVPPExportSummaryByProgram('DSGS')` performs an INNER JOIN between two tables:
- `silver_stream_dispatch_events` - Contains event metadata for DSGS ✅
- `silver_dispatch_summary` - Contains NO data for DSGS ❌

Since `silver_dispatch_summary` is empty, the INNER JOIN returns no results, causing the widget to display an empty array.

---

## Deep Dive - Why is `silver_dispatch_summary` Empty?

I traced through the downstream functions to find why this table has no data:

**Function chain investigated:**
```
getVPPSiteLevelPerformance
  ↓
getVPPDispatchSummary (event_id)
  ↓
getMultipleEventsSiteDispatchResults (event_id)
  ↓
getSiteDispatchResults (event_id, site_ids)
  ↓
silver_dispatch_result_dto table → **0 ROWS** ← ROOT CAUSE
```

**Event tested:** `1b55ba12-07eb-4b55-b29c-4947002f04b2`

---

## What I Found

**All downstream functions fail due to missing source data:**
- `getSiteDispatchResults(event_id, site_ids)` → Empty (queries `silver_dispatch_result_dto` which has 0 rows)
- `getMultipleEventsSiteDispatchResults(event_id)` → Empty (depends on above)
- `getSiteDispatchCommandSummary(event_id)` → Empty (depends on above)
- `getVPPDispatchSummary(event_id)` → **Returns data structure** with energy values BUT `sites_participation = 0` for all rows
  - This indicates the function runs but finds no site-level participation data
  - Output file: `getVPPDispatchSummary_dsgs.csv` shows 4 rows with timestamps but 0 participating sites
- `silver_dispatch_summary` table → Empty (not populated because upstream has no valid site participation)

**Root cause:** `silver_dispatch_result_dto` table has **0 rows** for DSGS event `1b55ba12-07eb-4b55-b29c-4947002f04b2`.

This table is supposed to contain dispatch command/result records for each site during the event. Without this source data, the entire calculation chain fails.

---

## What Data IS Available

✅ **Event metadata exists:**
- Table: `silver_stream_dispatch_events`
- Event ID: `1b55ba12-07eb-4b55-b29c-4947002f04b2`
- Dispatch Strategy: `CHARGE_FROM_SOLAR`
- Payload: `{"soc_target":100}`
- Event Time: 2026-02-11 21:00:00 to 22:00:00 UTC
- Sites: 400+ DSGS sites

✅ **Site telemetry data exists:**
- Table: `database('EventHouse').silverCommDataSite`
- Queried all DSGS program sites (extracted from event metadata)
- Result: 3,386 sites have telemetry data with min/max timestamps
- Data coverage: Sites have telemetry from 2025-03 through 2026-03 (covers event window)
- This proves sites ARE reporting telemetry data

❌ **Dispatch results missing:**
- Table: `silver_dispatch_result_dto`
- 0 rows for this event
- This is the foundation for all energy calculations

---

## Need Your Guidance

**Critical Question:** Should `CHARGE_FROM_SOLAR` dispatch strategy populate the `silver_dispatch_result_dto` table?

**If YES:**
- There's a data pipeline/ETL issue
- Need to identify where/how this table is populated
- Need to fix the pipeline and backfill missing data

**If NO:**
- The current widget architecture doesn't support this strategy
- Need to build alternative calculation using telemetry from `silverCommDataSite`
- Calculate energy as: `sum(max(energy) - min(energy))` per site during event window

---

## Proposed Solutions

**Option 1 - Temporary Fix (15 minutes):**
- Change INNER JOIN to LEFT JOIN in `getVPPExportSummaryByProgram`
- Widget shows DSGS with 0 MWh instead of empty array
- Prevents widget from breaking while we investigate proper fix

**Option 2 - Proper Fix:**
- **If pipeline issue:** Investigate and fix ETL process populating `silver_dispatch_result_dto`
- **If calculation needed:** Modify function to calculate energy directly from `silverCommDataSite` telemetry

---

## Questions for You

1. Should `CHARGE_FROM_SOLAR` strategy populate `silver_dispatch_result_dto`?
2. Do you know which process/pipeline populates this table?
3. Where did the 2.272 MWh value mentioned in the ticket come from?
4. Should I deploy the temporary fix while we investigate the proper solution?

---

All investigation evidence and detailed analysis documented in repository folder: `ticket-10180/`

Please advise on next steps. Thanks!

