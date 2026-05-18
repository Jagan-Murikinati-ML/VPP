# ADO-12654: Final Analysis & Questions for Naveen's Team

**Date:** 2026-03-27  
**Analyst:** Jagan Murikinati  
**Event:** Prg -20260318-85e2

---

## 📊 **EXECUTIVE SUMMARY**

We've completed a thorough analysis of the data discrepancy between the Past Events List and Site-Level Performance views. We've identified the root causes and need clarification on the expected behavior to propose the correct fix.

---

## 🔍 **WHAT WE FOUND**

### **The Bug:**
| View | Total Energy | Sites Dispatched |
|------|--------------|------------------|
| **Past Events List** | 2.3 kWh | 3 sites |
| **Site-Level Performance** | 2.9 kWh (net) | 4 sites |
| **Difference** | ❌ -0.6 kWh | ❌ -1 site |

---

## 🎯 **ROOT CAUSES IDENTIFIED**

### **1. Event Structure:**
Event "Prg -20260318-85e2" consists of **3 child events:**

| Event ID | Event Name | Time | Strategy | Sites with Commands |
|----------|------------|------|----------|---------------------|
| `b45c6b33-...` | Event1-0820-0835 | 03:20-03:35 | charge | 4 |
| `fdf0e836-...` | Event2-0851-0855 | 03:52-03:55 | charge | 4 |
| `44d6d4b8-...` | Event3-0838-0850 | 03:39-03:50 | self consumption | 3 |

---

### **2. Data Source Mismatch:**

The `getVPPDispatchSummary` function uses **TWO different data sources:**

**A. Site Count:** `silver_dispatch_result_dto` (command-based)
- Counts: Sites that **received commands** (excluding "stop" commands)
- Result: **4 sites** for Event1/Event2, **3 sites** for Event3

**B. Energy Calculation:** `silverCommDataSite` (telemetry-based)
- Counts: Sites that **sent telemetry data**
- Result: Only sites with actual performance data

**Problem:** Sites that received commands but didn't perform (0 energy) are counted but contribute 0 kWh!

---

### **3. The "Ghost" Site - 400005226:**

**Commands Sent:**
- Event1: ✅ `CHARGE_FROM_GRID_AND_SOLAR`
- Event2: ✅ `CHARGE_FROM_GRID_AND_SOLAR`
- Event3: ❌ No command

**Performance Data:**
- Start Time = End Time (03:21 to 03:21) → **0-minute dispatch window**
- Energy: **0 kWh charged, 0 kWh discharged**

**Impact:**
- ✅ Counted in site participation (got command)
- ❌ Contributes 0 energy

---

### **4. Function Execution Results:**

We executed `getVPPDispatchSummary` for each child event:

**Event1 (`b45c6b33-...`):**
- Energy Charged: 1.8 kWh
- Energy Discharged: 0.1 kWh
- Net Energy: **1.7 kWh**
- Sites: **4**

**Event2 (`fdf0e836-...`):**
- ❌ **NO DATA RETURNED** (function returns empty)
- But site-level performance CSV shows this event HAS data (0.7 kWh charged)!

**Event3 (`44d6d4b8-...`):**
- Energy Charged: 0 kWh
- Energy Discharged: 0.4 kWh
- Net Energy: **-0.4 kWh**
- Sites: **3**

---

### **5. Energy Calculation from Site-Level Performance:**

| Site ID | Event1 | Event2 | Event3 | Total (Net) |
|---------|--------|--------|--------|-------------|
| 400005338 | 0 kWh | 0 kWh | 0 kWh | 0 kWh |
| 400002333 | +1.2 kWh | +0.3 kWh | -0.2 kWh | +1.3 kWh |
| 400002331 | +1.6 kWh | +0.4 kWh | -0.4 kWh | +1.6 kWh |
| 400005226 | 0 kWh | 0 kWh | 0 kWh | 0 kWh |
| **TOTAL** | **+2.8 kWh** | **+0.7 kWh** | **-0.6 kWh** | **+2.9 kWh** |

---

## ❓ **QUESTIONS FOR NAVEEN'S TEAM**

### **1. Event ID Mapping:**
**Question:** Which event ID(s) does the Past Events List query to get the 2.3 kWh value?
- Is it querying a parent event ID?
- Or aggregating all 3 child events?
- Or only showing Event1?

**Why we need this:** We need to understand which function call(s) produce the 2.3 kWh to identify where the calculation is wrong.

---

### **2. Event2 Data Missing:**
**Question:** Why does `getVPPDispatchSummary("fdf0e836-...")` return NO data?
- Event2 has site-level performance data (0.7 kWh charged)
- Event2 has commands sent to 4 sites
- But the function returns empty

**Why we need this:** If Event2 data is missing from the summary function, this explains part of the energy gap (0.7 kWh).

---

### **3. Business Rule for Site Participation:**
**Question:** Should "Sites Dispatched" count sites that:
- A) Received dispatch commands (command-based) → **4 sites**
- B) Actually performed and sent telemetry (performance-based) → **3 sites**

**Why we need this:** Site 400005226 received commands but had a 0-minute dispatch window (start time = end time). Should it be counted?

---

### **4. Energy Calculation Method:**
**Question:** Should "Total Energy" be:
- A) Net Energy (Charged - Discharged) → **2.9 kWh**
- B) Only Charged Energy → **3.6 kWh**
- C) Sum of absolute values → **4.3 kWh**
- D) Something else?

**Juan confirmed:** Net Energy (option A), but the Past Events List shows 2.3 kWh, not 2.9 kWh.

---

### **5. Dispatch Strategy Filtering:**
**Question:** Should "self consumption" events (Event3) be included in the total energy calculation?
- Event1 + Event2 (charge strategy) = 2.8 + 0.7 = 3.5 kWh
- Event3 (self consumption) = -0.6 kWh
- Total with Event3 = 2.9 kWh
- Total without Event3 = 3.5 kWh (closer to Past Events List value if we exclude discharge)

**Why we need this:** If only "charge" strategies count, this explains why Event3 is excluded.

---

### **6. Code Location:**
**Question:** Where is the Past Events List API code?
- Which endpoint returns the `totalEnergy` and `sitesDispatched` values?
- Does it call `getVPPDispatchSummary` or a different function?
- How does it aggregate across child events?

**Why we need this:** We need the actual API code to identify the exact bug and propose a fix.

---

## 🎯 **PROPOSED NEXT STEPS**

### **Once we get answers:**

1. **Identify the exact calculation bug** in the API code
2. **Decide on the correct business logic:**
   - Command-based vs performance-based site counting
   - Whether to include discharge/self-consumption events
   - How to handle 0-duration dispatch windows
3. **Propose a fix** with test cases
4. **Submit PR** for review

---

## 📂 **SUPPORTING DATA**

All analysis data is in folder: `ticket-12654/`

**Key Files:**
- `sitelevelperformance-table-1.csv` - Complete site performance data (16 rows)
- `event1_summary.csv` - Function output for Event1
- `event3_summary.csv` - Function output for Event3
- `commands_for_3_site_ids.csv` - All commands sent to sites
- `breakdown_by_event_id_data.csv` - Site count by event
- `KUSTO_QUERY_ANALYSIS.md` - Detailed query analysis

---

## 🚀 **READY TO PROCEED**

Once you provide answers to the above questions, I can:
1. Pinpoint the exact bug location
2. Propose the correct fix
3. Write tests to validate the fix
4. Submit for code review

**Please let me know which questions you can answer, or if you need me to investigate any specific areas further.**

---

**Contact:** Jagan Murikinati  
**Date:** 2026-03-27

