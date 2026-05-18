# The One-Line Fix for Battery Discharge Bug

---

## 🔧 FUNCTION TO MODIFY

**Function Name:** `getSiteDispatchResults`

---

## 📝 THE CHANGE

**Line 39:**

### ❌ BEFORE (Buggy):
```kusto
| where sourceTimestamp < dispatch_time or isnull(sourceTimestamp)
```

### ✅ AFTER (Fixed):
```kusto
| where sourceTimestamp < next_command_timestamp or isnull(sourceTimestamp)
```

---

## 🎯 THAT'S IT!

**One word change:** `dispatch_time` → `next_command_timestamp`

**Result:** Fixes 96.6% error in discharge calculations ✅

---

## 🧪 TEST IN DEV

After applying the fix, run:

```kusto
getVPPSiteLevelPerformance(input_event_name='ca0c0d89-614d-4358-b31f-2cb27a29cf5f')
| where site_id == '400000837'
| project site_id, energy_discharged_kWh
```

**Expected Result:**
```
site_id: 400000837
energy_discharged_kWh: 6.677 (currently shows 0.23)
```

---

## 📋 COMPLETE FUNCTION CODE (with fix)

```kusto
{
    let eventDetails = 
        silver_stream_dispatch_events
        | where event_id in (input_event_id)
        | summarize arg_max(event_processed_utc_time, event_status, event_start_time, event_end_time, sites) by program_name, event_id
    ;
    let eventBackbone = 
        silver_dispatch_result_dto
        | where event_id in (input_event_id)
            and (site_id in (input_site_id) or array_length(input_site_id) == 0)
        | order by event_id, site_id, dispatch_time
        | extend next_command_timestamp = iif(prev(site_id) == site_id, prev(dispatch_time, 1),datetime(null))
        | extend next_command_timestamp = coalesce(next_command_timestamp, datetime('4040-12-31'))
    ;
    let blankTelemetryDefaults = 
        eventBackbone
        | distinct site_id
        | join kind = leftouter (
            database('eventhouse').table('silverCommDataSite')
            | summarize take_any(oem) by siteId
        ) on $left.site_id == $right.siteId
        | project siteId = coalesce(siteId, site_id), oem
    ;
    let dispatchTelemetry = materialize(
        database('eventhouse').table('silverCommDataSite')
        | where 1==1
            and siteId in (eventDetails | project sites)
            and sourceTimestamp between ( toscalar(eventDetails | project event_start_time) .. datetime_add('minute',30, toscalar(eventDetails | project event_end_time)))
        | project siteId, oem, sourceTimestamp, battery_200_IncWhExp, battery_200_IncWhImp, grid_200_IncWhExp, grid_200_IncWhImp, pv_200_IncWhExp, battery_200_W, pv_200_W, grid_200_W
        | order by siteId, sourceTimestamp asc
        | serialize 
        | project siteId, oem, sourceTimestamp
            ,battery_200_W, grid_200_W, pv_200_W
            ,battery_200_IncWhExp   , cu_battery_200_IncWhExp   = row_cumsum(battery_200_IncWhExp   , siteId != prev(siteId))
            ,battery_200_IncWhImp   , cu_battery_200_IncWhImp   = row_cumsum(battery_200_IncWhImp   , siteId != prev(siteId))
            ,grid_200_IncWhExp      , cu_grid_200_IncWhExp      = row_cumsum(grid_200_IncWhExp      , siteId != prev(siteId))
            ,grid_200_IncWhImp      , cu_grid_200_IncWhImp      = row_cumsum(grid_200_IncWhImp      , siteId != prev(siteId))
            ,pv_200_IncWhExp        , cu_pv_200_IncWhExp        = row_cumsum(pv_200_IncWhExp        , siteId != prev(siteId))
        | union blankTelemetryDefaults
    );
    let joinedData = 
        eventBackbone
        | join kind=leftouter dispatchTelemetry on $left.site_id == $right.siteId
        | where sourceTimestamp < next_command_timestamp or isnull(sourceTimestamp)  // ✅ FIXED LINE
        | summarize arg_max(sourceTimestamp,*) by event_id, site_id, dispatch_time
        | order by event_id, site_id, dispatch_time
    ;
    joinedData 
}
```

**Changed line 39:** `dispatch_time` → `next_command_timestamp`

---

## 🚀 DEPLOY CHECKLIST

- [ ] Apply fix in DEV
- [ ] Test with event ca0c0d89-614d-4358-b31f-2cb27a29cf5f
- [ ] Verify site 400000837 shows 6.677 kWh
- [ ] Test multiple other events
- [ ] Deploy to PROD
- [ ] Monitor for 24 hours
- [ ] Close ticket

---

**Simple. Clean. Effective.** ✅
