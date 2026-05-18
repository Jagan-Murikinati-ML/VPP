# Fix Comparison - getSiteDispatchResults

---

## 📝 **FUNCTION:** `getSiteDispatchResults`

## 🔧 **LINE TO CHANGE:** 44

---

## ❌ **BEFORE (Current PROD - Buggy):**

```kusto
| where sourceTimestamp < dispatch_time or isnull(sourceTimestamp)
```

---

## ✅ **AFTER (Fixed):**

```kusto
| where sourceTimestamp < next_command_timestamp or isnull(sourceTimestamp)
```

---

## 📊 **WHAT CHANGES:**

| Variable | Old (Buggy) | New (Fixed) |
|----------|-------------|-------------|
| Filter cutoff | `dispatch_time` | `next_command_timestamp` |

**One word change:** `dispatch_time` → `next_command_timestamp`

---

## 🎯 **WHY THIS WORKS:**

### For Site 400000837:

**Old Behavior (Buggy):**
```
dispatch_time = 07:17:11
Filter: sourceTimestamp < 07:17:11
Result: Only keeps telemetry at 07:15
Misses: 07:20, 07:25, 07:30, ..., 08:15
Discharge: 230 Wh (0.23 kWh) ❌
```

**New Behavior (Fixed):**
```
next_command_timestamp = 4040-12-31 (no next command)
Filter: sourceTimestamp < 4040-12-31
Result: Keeps ALL telemetry from 07:15 to 08:15
Includes: 07:15, 07:20, 07:25, 07:30, ..., 08:15
Discharge: 6,677 Wh (6.677 kWh) ✅
```

---

## 🧪 **HOW TO TEST:**

### 1. Apply fix in DEV

Update the `getSiteDispatchResults` function with the fixed line 44.

### 2. Run test query

```kusto
getVPPSiteLevelPerformance(input_event_name='ca0c0d89-614d-4358-b31f-2cb27a29cf5f')
| where site_id == '400000837'
| project site_id, energy_discharged_kWh, dispatch_start_time, dispatch_end_time
```

### 3. Expected result

```
site_id: 400000837
energy_discharged_kWh: 6.677 (currently 0.23)
dispatch_start_time: 2026-05-12 07:15:00 (currently 07:17:11)
dispatch_end_time: 2026-05-12 08:15:00 (currently 07:17:11)
```

---

## 📁 **FILES:**

- `getSiteDispatchResults.csv` - Current PROD code (buggy)
- `getSiteDispatchResults_FIXED.csv` - Fixed code (ready to deploy)

---

## ✅ **DEPLOYMENT:**

1. Backup current function
2. Replace line 44 with fixed version
3. Test in DEV
4. Deploy to PROD
5. Verify with multiple events

---

**Simple. One line. Huge impact.** 🚀
