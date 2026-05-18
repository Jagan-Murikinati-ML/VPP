# Call Prep: Ticket 12654/15308 - Site Performance Data Issue

**Date:** Tomorrow, 9:00 AM PST (9:30 PM IST)  
**Participants:** Naveen, Jagan  
**Purpose:** Discuss site-level performance data discrepancy

---

## 🎯 **QUICK SUMMARY (30 Second Version)**

**The Bug:**
- Past Events List shows: **2.3 kWh, 3 sites**
- Site-Level Performance shows: **2.9 kWh, 4 sites**
- **Discrepancy: -0.6 kWh, -1 site**

**Root Cause:**
- Two different data sources with different counting logic
- Past Events: Command-based (who received commands)
- Site Performance: Telemetry-based (who actually performed)
- "Ghost" site 400005226: Got command, but 0 energy/0 performance

---

## 📊 **THE ISSUE IN DETAIL**

### **Event:** `Prg -20260318-85e2`

**Event Structure:** 3 child events

| Event ID (partial) | Time | Strategy | Sites |
|-------------------|------|----------|-------|
| `b45c6b33...` (Event1) | 03:20-03:35 | charge | 4 |
| `fdf0e836...` (Event2) | 03:52-03:55 | charge | 4 |
| `44d6d4b8...` (Event3) | 03:39-03:50 | self consumption | 3 |

---

### **The 4 Sites:**

| Site ID | Event1 | Event2 | Event3 | Total Net Energy |
|---------|--------|--------|--------|------------------|
| **400005338** | 0 kWh | 0 kWh | 0 kWh | 0 kWh |
| **400002333** | +1.2 kWh | +0.3 kWh | -0.2 kWh | **+1.3 kWh** |
| **400002331** | +1.6 kWh | +0.4 kWh | -0.4 kWh | **+1.6 kWh** |
| **400005226** | 0 kWh | 0 kWh | N/A | **0 kWh** ⚠️ |
| **TOTAL** | **+2.8 kWh** | **+0.7 kWh** | **-0.6 kWh** | **2.9 kWh** |

---

### **The "Ghost" Site: 400005226**

**What happened:**
- ✅ Received dispatch command: `CHARGE_FROM_GRID_AND_SOLAR`
- ✅ Shows in command logs
- ❌ **Dispatch window: Start time = End time** (0 minutes!)
- ❌ Performance: 0 kWh charged, 0 kWh discharged
- ❌ Only participated in Event1 & Event2, NOT Event3

**The Question:**
- Should this site be counted as "dispatched"?
- Command sent → YES (count it)
- No actual performance → NO (exclude it)

---

## 🔍 **WHAT WE FOUND**

### **1. Function Used:**

**`getVPPDispatchSummary(eventId)`**

**Data Sources:**
- **Site Count:** From `silver_dispatch_result_dto` (command-based)
  - Logic: `COUNT(DISTINCT siteID WHERE command NOT LIKE '%stop%')`
  - Counts sites that received commands
  
- **Energy Calculation:** From `silverCommDataSite` (telemetry-based)
  - Logic: Actual performance data
  - Only sites with telemetry data

---

### **2. Test Results:**

We executed `getVPPDispatchSummary` for each child event:

**Event1 (`b45c6b33...`):**
- ✅ Returned data
- Energy: 1.7 kWh net
- Sites: 4

**Event2 (`fdf0e836...`):**
- ❌ **NO DATA RETURNED!** (function returns empty)
- But CSV shows Event2 has 0.7 kWh of data!
- **This is a bug!**

**Event3 (`44d6d4b8...`):**
- ✅ Returned data
- Energy: -0.4 kWh net (discharge)
- Sites: 3

---

### **3. Key Questions Still Unanswered:**

❓ **Which event ID(s) does Past Events List query?**
- Parent event ID?
- All 3 child events?
- Just Event1?

❓ **Why does Event2 return empty?**
- 0.7 kWh is missing from the calculation!

❓ **Should "self consumption" events be included?**
- If we exclude Event3: 2.8 + 0.7 = 3.5 kWh (closer but still not 2.3)

❓ **What's the correct business logic for "dispatched sites"?**
- Command-based or performance-based?

---

## 🎯 **WHAT TO ASK NAVEEN**

### **Priority 1: Event ID Mapping**

**Question:**
> "Which event ID(s) does the Past Events List query to display 2.3 kWh?"

**Why we need this:**
- Need to understand which function call(s) produce 2.3 kWh
- Is it querying parent event or aggregating child events?

---

### **Priority 2: Event2 Missing Data**

**Question:**
> "Why does `getVPPDispatchSummary('fdf0e836...')` return NO data when Event2 has site-level performance data showing 0.7 kWh?"

**Why we need this:**
- Event2 missing could explain 0.7 kWh of the 0.9 kWh discrepancy
- Might be a bug in the function itself

---

### **Priority 3: Business Logic**

**Question:**
> "Should 'Sites Dispatched' count sites that received commands (4) or sites that actually performed (3)?"

**Context:**
- Site 400005226 received command but had 0-minute dispatch window
- Currently counted in command logs but 0 energy performance

---

### **Priority 4: Code Location**

**Question:**
> "Where is the Past Events List API code? Which endpoint returns the totalEnergy and sitesDispatched values?"

**Why we need this:**
- Need actual API code to identify exact bug
- Want to trace how 2.3 kWh is calculated

---

## 📁 **SUPPORTING DATA READY**

All in folder: `ticket-12654/`

**Key files to show Naveen:**
- `sitelevelperformance-table-1.csv` - Complete site data (all 4 sites)
- `event1_summary.csv` - Function output for Event1
- `event3_summary.csv` - Function output for Event3
- `commands_for_3_site_ids.csv` - All dispatch commands sent
- `FINAL_ANALYSIS_FOR_NAVEEN.md` - Detailed write-up

---

## ✅ **WHAT YOU'VE ALREADY DONE**

1. ✅ Analyzed all site-level performance data (12 rows)
2. ✅ Identified the 4 participating sites
3. ✅ Tested `getVPPDispatchSummary` function for all 3 child events
4. ✅ Found Event2 returns empty (potential bug)
5. ✅ Identified "ghost" site 400005226 (command but no performance)
6. ✅ Calculated correct net energy: 2.9 kWh
7. ✅ Identified discrepancy: -0.6 kWh, -1 site
8. ✅ Created detailed analysis documents

---

## 💡 **CONFIDENCE BOOSTERS**

### **You Know:**
- ✅ The exact event ID: `Prg -20260318-85e2`
- ✅ All 3 child event IDs
- ✅ All 4 participating sites
- ✅ The function used: `getVPPDispatchSummary`
- ✅ The data sources: `silver_dispatch_result_dto` and `silverCommDataSite`
- ✅ The correct calculation: Net Energy (Charge - Discharge) = 2.9 kWh
- ✅ The discrepancy: Past Events shows 2.3 kWh (missing 0.6 kWh)

### **You Have:**
- ✅ All CSV data files
- ✅ All query results
- ✅ Detailed analysis documents
- ✅ Clear questions prepared

---

## 🚀 **YOU'RE READY!**

**Key message for the call:**

> "I've analyzed the data discrepancy between Past Events List (2.3 kWh, 3 sites) and Site-Level Performance (2.9 kWh, 4 sites). I've identified the root causes and have specific questions about the business logic and code implementation to propose the correct fix."

**Then walk through the 4 priority questions above.**

---

**You got this!** 💪

