@Ayub Shirgaonkar @Naveen - Investigation complete on MWh Exports widget returning empty array for DSGS.

---

## Root Cause

The widget calculation chain depends on `silver_dispatch_result_dto` table. For DSGS event `1b55ba12-07eb-4b55-b29c-4947002f04b2`, this table has **0 rows**, causing all downstream functions to fail.

**What EXISTS:**
- ✅ Event metadata in `silver_stream_dispatch_events` (strategy: `CHARGE_FROM_SOLAR`)
- ✅ Site telemetry in `silverCommDataSite` (2,000+ records for 400+ sites)

**What's MISSING:**
- ❌ Dispatch results in `silver_dispatch_result_dto` (0 rows)

---

## Need Your Input

**Question:** Is `CHARGE_FROM_SOLAR` strategy supposed to populate `silver_dispatch_result_dto`?

- **If YES** → There's a pipeline bug, need to fix ETL process
- **If NO** → Need to build alternative calculation from telemetry

---

## Next Steps

**Temporary Fix (15 min):** Change INNER JOIN to LEFT JOIN - shows `0 MWh` instead of crashing

**Proper Fix:** Depends on your answer above
- Pipeline fix, OR
- Modify function to calculate from telemetry: `sum(max(energy) - min(energy))` per site

---

Please advise which path to pursue. Complete analysis and evidence files in `ticket-10180/` folder.

Thanks!

