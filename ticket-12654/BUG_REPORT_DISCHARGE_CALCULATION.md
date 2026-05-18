# BUG REPORT: Incorrect Battery Discharge Calculation in getVPPSiteLevelPerformance

**Date:** May 14, 2026  
**Ticket:** #12654, #10180, #15308  
**Severity:** CRITICAL  
**Status:** Root Cause Identified

---

## 🚨 EXECUTIVE SUMMARY

The `getVPPSiteLevelPerformance` function returns incorrect `energy_discharged_kWh` values, showing ~97% less discharge than actual battery performance.

**Example:**
- **Actual Discharge:** 6.677 kWh (verified from telemetry)
- **Function Returns:** 0.23 kWh
- **Error:** 96.6% underreporting

---

## 🔍 ROOT CAUSE

**Function:** `getSiteDispatchResults()` (helper function)  
**Line:** 39  
**Buggy Code:**
```kusto
| where sourceTimestamp < dispatch_time or isnull(sourceTimestamp)
```

**Issue:** This filters out ALL telemetry data AFTER the command dispatch time, causing the function to only capture telemetry from a single instant instead of the entire event duration.

---

## 📊 DETAILED ANALYSIS - Site 400000837

### Event Details:
- **Event ID:** ca0c0d89-614d-4358-b31f-2cb27a29cf5f
- **Event Window:** 07:15:00 - 08:15:00 (1 hour)
- **Site ID:** 400000837
- **OEM:** SolarEdge

### Command Dispatch:
- **Command Time:** 07:17:11 (ONE command sent)
- **Command:** DISCHARGE_TO_HOME_AND_GRID
- **Status:** 200 (Success)

### Telemetry Data Available:
- **Readings:** 13 telemetry points (every 5 minutes from 07:15 to 08:15)
- **Actual Discharge:** 6,677 Wh (6.677 kWh)

### What the Function Returns:
- **Discharge:** 230 Wh (0.23 kWh) ❌
- **Error:** 96.6% underreporting

---

## 🐛 HOW THE BUG OCCURS

### Step 1: `getSiteDispatchResults()` Queries Telemetry

**Line 39:**
```kusto
| where sourceTimestamp < dispatch_time or isnull(sourceTimestamp)
```

For site 400000837:
- `dispatch_time` = 07:17:11
- Telemetry readings: 07:15, 07:20, 07:25, 07:30, ..., 08:15

**Filter Result:**
- ✅ Keeps: 07:15:00 (before dispatch_time)
- ❌ Filters out: 07:20, 07:25, 07:30, ..., 08:15 (all AFTER dispatch_time)

**Returns:** Only ONE telemetry reading at 07:15 with `cu_battery_200_IncWhExp = 230 Wh`

---

### Step 2: `getSiteDispatchCommandSummary()` Uses arg_min/arg_max

**Lines 38-40:**
```kusto
| summarize 
    (command_start_time, command_start_time_discharge, ...) = arg_min(dispatch_time, energy_discharged, ...)
    ,(command_end_time, command_end_time_discharge, ...) = arg_max(dispatch_time, energy_discharged, ...)
```

**Result:**
- `arg_min` returns: `command_start_time_discharge = 230` Wh
- `arg_max` returns: `command_end_time_discharge = 230` Wh (SAME VALUE!)

---

### Step 3: Calculate overall_command_discharge

**Line 62:**
```kusto
overall_command_discharge = iff(isnull(next_command_start_discharge), command_end_time_discharge, next_command_start_discharge) 
                            - iif(command_group_id == 1, 0.0, command_start_time_discharge)
```

**Calculation:**
```
overall_command_discharge = 230 - 0 = 230 Wh
```

**Should be:**
```
overall_command_discharge = 6,907 - 230 = 6,677 Wh
```

---

### Step 4: Convert to kWh

**`getVPPSiteLevelPerformance` Line 42:**
```kusto
energy_discharged_kWh = sum(overall_command_discharge)/1000.0
                      = 230/1000
                      = 0.23 kWh ❌
```

---

## ✅ THE FIX

### Change in `getSiteDispatchResults()` Line 39:

**FROM:**
```kusto
| where sourceTimestamp < dispatch_time or isnull(sourceTimestamp)
```

**TO:**
```kusto
| where sourceTimestamp < next_command_timestamp or isnull(sourceTimestamp)
```

---

## 🎯 WHY THIS FIX WORKS

### Current Behavior (Buggy):
- Uses `dispatch_time` (07:17:11) as the cutoff
- Only captures telemetry BEFORE the command was sent
- Misses all discharge that happens AFTER the command

### Fixed Behavior:
- Uses `next_command_timestamp` as the cutoff
- For the last command: `next_command_timestamp = 4040-12-31` (effectively no limit)
- Captures ALL telemetry from command start until next command (or end of event)
- Gets cumulative discharge at event end (6,907 Wh) minus start (230 Wh) = **6,677 Wh** ✅

---

## 📊 VERIFICATION - After Fix

### Expected Results:
```
command_start_time_discharge: 230 Wh (cumulative at 07:15)
command_end_time_discharge: 6,907 Wh (cumulative at 08:15)
overall_command_discharge: 6,677 Wh
energy_discharged_kWh: 6.677 kWh ✅
```

---

## 🔗 FUNCTION CALL CHAIN

```
getVPPSiteLevelPerformance()
  ↓ Line 38
getSiteDispatchCommandSummary()
  ↓ Line 7
getMultipleEventsSiteDispatchResults()
  ↓ Loop
getSiteDispatchResults() ⚠️ BUG HERE - Line 39
  ↓
silverCommDataSite (telemetry table)
```

---

## 🚨 IMPACT

### Affected Functions:
- ✅ `getVPPSiteLevelPerformance` (site-level performance reports)
- ❌ `getVPPDispatchSummary` (NOT affected - uses different logic)

### Affected Sites:
- **All sites that receive ONLY ONE command per event**
- Sites with multiple commands during an event are less affected (but may still have errors)

### Severity:
- **CRITICAL** - Underreports battery discharge by up to 97%
- Affects billing, performance reporting, and grid operator settlement
- Causes UI to show blank/incorrect data

---

## 📋 TESTING RECOMMENDATIONS

### Test Case 1: Single Command Event
- Event with ONE command sent at event start
- Battery runs for full hour
- Verify discharge matches telemetry sum

### Test Case 2: Multiple Command Event  
- Event with multiple commands (charge, discharge, stop)
- Verify each command window captures correct telemetry

### Test Case 3: Failed Command
- Command with status code 400/500
- Verify function handles gracefully

---

## 🎯 NEXT STEPS

1. ✅ Apply fix to `getSiteDispatchResults()` line 39
2. ✅ Test in DEV environment with event `ca0c0d89-614d-4358-b31f-2cb27a29cf5f`
3. ✅ Verify site 400000837 returns 6.677 kWh
4. ✅ Deploy to PROD
5. ✅ Reprocess historical events (optional)

---

**Prepared by:** Jagan Murikinati  
**Reviewed by:** [Pending - Shaun/Naveen]  
**Date:** May 14, 2026
