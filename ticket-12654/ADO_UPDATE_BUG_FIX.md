# ADO Update - Root Cause Found & Fix Identified

Hi @Shaun Roach @Naveen,

I've completed the investigation and found the root cause of the incorrect discharge values in `getVPPSiteLevelPerformance`.

---

## 🎯 ROOT CAUSE

**Function:** `getSiteDispatchResults()` (helper function)  
**Line:** 39  
**Bug:**
```kusto
| where sourceTimestamp < dispatch_time or isnull(sourceTimestamp)
```

This filters out ALL telemetry AFTER the command dispatch time, causing the function to only capture one instant instead of the full event duration.

---

## 📊 EXAMPLE - Site 400000837

**Event:** ca0c0d89-614d-4358-b31f-2cb27a29cf5f  
**Duration:** 07:15 - 08:15 (1 hour)

**Actual Discharge (from telemetry):** 6.677 kWh  
**Function Returns:** 0.23 kWh  
**Error:** 96.6% underreporting ❌

**Why:**
- Command sent at 07:17:11
- Line 39 filters out telemetry after 07:17:11
- Only captures telemetry at 07:15 (230 Wh)
- Misses all discharge from 07:20-08:15 (6,447 Wh)

---

## ✅ THE FIX

**Change Line 39 in `getSiteDispatchResults()` from:**
```kusto
| where sourceTimestamp < dispatch_time or isnull(sourceTimestamp)
```

**To:**
```kusto
| where sourceTimestamp < next_command_timestamp or isnull(sourceTimestamp)
```

**Why this works:**
- `next_command_timestamp` = time of next command (or 4040-12-31 if no next command)
- Captures ALL telemetry from current command until next command
- For site 400000837: captures full 07:15-08:15 window
- Result: 6.677 kWh ✅

---

## 📋 VERIFICATION

After fix, for site 400000837:
```
Telemetry at 07:15: cu_battery_200_IncWhExp = 230 Wh (start)
Telemetry at 08:15: cu_battery_200_IncWhExp = 6,907 Wh (end)
Discharge = 6,907 - 230 = 6,677 Wh = 6.677 kWh ✅
```

---

## 🚨 IMPACT

**Affected:** All sites with ONE command per event (most common scenario)  
**Severity:** CRITICAL - underreports discharge by up to 97%  
**Scope:** `getVPPSiteLevelPerformance` only (dispatch summary not affected)

---

## 📁 DETAILED ANALYSIS

Full bug report with call chain, test cases, and examples:  
`ticket-12654/BUG_REPORT_DISCHARGE_CALCULATION.md`

---

**Next Steps:**
1. Review and approve fix
2. Test in DEV environment
3. Deploy to PROD

Thanks,  
Jagan
