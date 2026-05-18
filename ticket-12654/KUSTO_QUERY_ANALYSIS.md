# Kusto Query Analysis - ADO-12654

**Date:** 2026-03-27  
**Event:** Prg -20260318-85e2

---

## 🎯 **CRITICAL FINDINGS**

### **Root Cause Identified:**
The `getVPPDispatchSummary` function uses **TWO different data sources**:
1. **Site Count:** `silver_dispatch_result_dto` (command-based)
2. **Energy Calculation:** `silverCommDataSite` (telemetry-based)

**Result:** Mismatch between sites that received commands vs sites that performed!

---

## Event Structure

The event "Prg -20260318-85e2" consists of **3 child event IDs:**

| Event ID | Event Name | Sites (Non-Stop Commands) |
|----------|------------|---------------------------|
| `b45c6b33-ff43-4b66-9fb8-359c2c45eb57` | Event1-0820-0835 | **4 sites** |
| `fdf0e836-a75d-4d54-b1e4-15af16ba53dc` | Event2-0851-0855 | **4 sites** |
| `44d6d4b8-7b81-4c8d-9cc0-313143973f6f` | Event3-0838-0850 | **3 sites** |

---

## Query Results

### Query 1: Sites WITHOUT "stop" Commands
**File:** `site_count_with_no_stop_command.csv`

```
Total Sites: 4
Sites: ["400005226", "400002331", "400002333", "400005338"]
Commands: ["CHARGE_FROM_GRID_AND_SOLAR", "SELF_CONSUMPTION"]
```

✅ **This is what the function counts as "sites_participation"**

---

### Query 2: Sites WITH "stop" Commands
**File:** `site_count_with_stop_command.csv`

```
Total Sites: 3
Sites: ["400005338", "400002333", "400002331"]
Commands: ["StopDispatchCommandDto"]
```

❌ **Site 400005226 is NOT in this list!**

---

### Query 3: Breakdown by Event ID
**File:** `breakdown_by_event_id_data.csv`

| Event ID | Site Count | Sites |
|----------|------------|-------|
| b45c6b33... (Event1) | **4** | 400005226, 400002331, 400002333, 400005338 |
| fdf0e836... (Event2) | **4** | 400002333, 400002331, 400005338, 400005226 |
| 44d6d4b8... (Event3) | **3** | 400005338, 400002333, 400002331 |

---

## Site 400005226 - The "Ghost" Site

### Commands Received:
**File:** `commands_for_3_site_ids.csv`

- **Event1** (`b45c6b33...`): 1x `CHARGE_FROM_GRID_AND_SOLAR` (Line 21)
- **Event2** (`fdf0e836...`): 1x `CHARGE_FROM_GRID_AND_SOLAR` (Line 5)
- **Event3** (`44d6d4b8...`): **No commands**

### Telemetry Data:
**File:** `sitelevelperformance-table-1.csv`

- **NOT present in the CSV** (or has 0 energy)
- Energy Charged: 0 kWh
- Energy Discharged: 0 kWh
- Net Energy: 0 kWh

### Impact:
✅ **Counted in site participation** (received non-stop command)  
❌ **Does NOT contribute to energy** (no telemetry data)

---

## The Mismatch

### What We Expected:
Based on our queries, the summary should show:
- **Sites:** 4 (based on commands sent)
- **Energy:** Should aggregate telemetry from all 4 sites

### What Past Events List Shows:
- **Sites:** 3 ❓
- **Energy:** 2.3 kWh

### What Site-Level Performance Shows:
- **Sites:** 4 (with site 400005226 having 0 energy)
- **Energy:** 2.9 kWh (Net Energy)

---

## 🚨 **CRITICAL QUESTION:**

**Our query shows 4 sites with non-stop commands, but Past Events shows 3 sites!**

**Possible Explanations:**
1. Past Events is showing only **ONE event ID** (not all 3 combined)
2. There's **additional filtering logic** in the API we haven't seen
3. The `getVPPDispatchSummary` function has a **bug** in how it counts sites
4. The function is called with a different event ID than we think

---

## Next Steps

1. ✅ **Determine which event ID(s)** the Past Events List is querying
2. ⏳ **Execute `getVPPDispatchSummary`** function directly with the actual event ID
3. ⏳ **Ask Naveen/Sanjeev** which event ID the UI is using
4. ⏳ **Validate** if the function should aggregate across all 3 child events or just one

---

**Files Referenced:**
- `site_count_with_no_stop_command.csv`
- `site_count_with_stop_command.csv`
- `breakdown_by_event_id_data.csv`
- `commands_for_3_site_ids.csv`
- `sitelevelperformance-table-1.csv`
- `dispatach_summary_function_output.csv`

