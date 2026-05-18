Hi @Naveen @Shaun,

Found the root cause of incorrect `energy_discharged_kWh` values in `getVPPSiteLevelPerformance`. The function underreports discharge by ~97% for sites receiving a single command.

## Issue Found

When I call this function for the 1-hour event window:

```kusto
getSiteDispatchResults(
    input_event_id = dynamic(['ca0c0d89-614d-4358-b31f-2cb27a29cf5f']),
    input_site_id = dynamic(['400000837'])
)
```

**Expected:** 12-13 rows (one per 5-minute telemetry reading)
**Actual:** Only 1 row returned

## Root Cause (Line 44)

```kusto
| where sourceTimestamp < dispatch_time or isnull(sourceTimestamp)
```

This is filtering based on `dispatch_time` value, which filters out all telemetry after the command was sent. Since it's missing all the time windows except the first timestamp, we're losing ~97% of the discharge data.

**Question:** Should this filter be using `next_command_timestamp` instead of `dispatch_time`?

The function already calculates `next_command_timestamp = 4040-12-31` when there's no next command, which would capture the full event window.

Please let me know if my understanding is correct.

I'll attach the output screenshot showing only 1 row being returned.
