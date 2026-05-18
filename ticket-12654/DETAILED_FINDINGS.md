# Detailed Image Analysis - ADO-12654

**Date:** March 25, 2026  
**Analyst:** Jagan Murikinati  

---

## 📸 IMAGE ANALYSIS

### **Image 1: Past Events List (Summary View)**

**What it shows:**
- A list of past VPP dispatch events
- Event highlighted: `Prg -20260318-85e2`
- Event time: **3:20 AM - 3:55 AM** (35 minutes total)
- Dispatch Energy: **Both** (charge + discharge)
- **No. of Groups Dispatched: 3**
- **No. of Sites Dispatched: 3** ⚠️
- **Total Energy (kWh): 2.3** ⚠️

**Data Source:**
- Browser network tab visible in image shows API call
- JSON payload contains: `"totalEnergy": 2300` (in Wh)
- UI converts to kWh: 2300 Wh → 2.3 kWh

---

### **Image 2: Site-Level Performance (Detail View)**

**What it shows:**
- Individual site performance data for event `Prg -20260318-85e2`
- **7 rows highlighted** (but only 3 unique site IDs!)

**Detailed Breakdown:**

| Row | Site ID   | Time Window | Energy Discharged | Energy Charged | Row Total |
|-----|-----------|-------------|-------------------|----------------|-----------|
| 1   | 400005338 | 3:20-3:35   | 0 kWh             | 0 kWh          | 0 kWh     |
| 2   | 400002333 | 3:20-3:35   | 0.1 kWh           | 1.3 kWh        | 1.4 kWh   |
| 3   | 400002331 | 3:20-3:35   | 0 kWh             | 1.6 kWh        | 1.6 kWh   |
| 4   | 400005338 | 3:52-3:55   | 0 kWh             | 0 kWh          | 0 kWh     |
| 5   | 400002333 | 3:52-3:55   | 0 kWh             | 0.3 kWh        | 0.3 kWh   |
| 6   | 400002331 | 3:52-3:55   | 0 kWh             | 0.4 kWh        | 0.4 kWh   |
| 7   | 400005338 | (unknown)   | 0 kWh             | 0 kWh          | 0 kWh     |

**Calculations:**
- **Total Energy (sum of all 7 rows):** 0 + 1.4 + 1.6 + 0 + 0.3 + 0.4 + 0 = **3.7 kWh**
- **Unique Site IDs:** 3 (400005338, 400002333, 400002331)
- **Total Rows:** 7

---

## 🔍 KEY OBSERVATION: Multiple Dispatch Windows

**Critical Pattern Discovered:**

The event runs from **3:20 AM to 3:55 AM** (35 minutes), but it's **NOT continuous**!

**Dispatch Windows:**
1. **Window 1:** 3:20 - 3:35 (15 minutes)
2. **Gap:** 3:35 - 3:52 (17 minutes - no dispatch)
3. **Window 2:** 3:52 - 3:55 (3 minutes)

**Why Same Sites Appear Multiple Times:**
- Site 400005338 appears in: Row 1 (Window 1), Row 4 (Window 2), Row 7 (unknown)
- Site 400002333 appears in: Row 2 (Window 1), Row 5 (Window 2)
- Site 400002331 appears in: Row 3 (Window 1), Row 6 (Window 2)

**This is NORMAL behavior** - sites can participate in multiple windows within one event!

---

## ⚠️ THE BUG

### **Comparison:**

| Metric        | Past Events List | Site Performance (Actual) | Match? |
|---------------|------------------|---------------------------|--------|
| Total Energy  | 2.3 kWh          | 3.7 kWh                   | ❌ NO  |
| Site Count    | 3 sites          | 3 unique sites            | ✅ YES |

### **The Problem:**

**Energy Mismatch:**
- Past Events API shows: **2.3 kWh**
- Actual sum of all rows: **3.7 kWh**
- **Difference: 1.4 kWh missing!** ❌

**Site Count:**
- Past Events API shows: **3 sites**
- Actual unique sites: **3 sites**
- **This appears correct** ✅ (but need to verify the API is using `COUNT(DISTINCT site_id)`)

---

## 🎯 ROOT CAUSE HYPOTHESIS

### **Most Likely: Missing Time Windows in Aggregation**

The Past Events API is likely:

1. **Only counting ONE time window** (3:20-3:35)
   - Sum of Window 1: 0 + 1.4 + 1.6 = 3.0 kWh
   - Still doesn't match 2.3 kWh... 🤔

2. **Using wrong WHERE clause** that filters out some rows

3. **Querying a different table** that doesn't have all the data

4. **Aggregating BEFORE the event completes** (snapshot at 3:35, missing 3:52-3:55 window)

---

## 📋 QUESTIONS TO ASK TEAM

1. **Where is the Past Events API code?**
   - Which endpoint returns the `totalEnergy` and `sitesDispatched`?
   - What query does it use?

2. **Where is the Site Performance data from?**
   - Kusto table name?
   - Is this the source of truth?

3. **How should energy be calculated?**
   - Sum ALL rows for the event?
   - Sum per site, then sum sites?
   - Should be the same result either way!

4. **When is the summary calculated?**
   - Real-time during event?
   - After event completes?
   - Cached/pre-aggregated?

---

## 🚀 NEXT STEPS

1. ✅ Send message to Sanjeev & Juan (MESSAGE_TO_TEAM.md)
2. ⏳ Wait for code locations
3. ⏳ Review both queries side-by-side
4. ⏳ Identify the exact bug
5. ⏳ Propose fix
6. ⏳ Test in DEV with event "Prg-20260318-85e2"
7. ⏳ Submit PR

---

**Status:** Page 2 data received - analysis updated

---

## 🆕 UPDATE: PAGE 2 DATA RECEIVED

### **Page 2 Contains 5 Additional Rows:**

| Row | Site ID   | Discharge | Charge | Total |
|-----|-----------|-----------|--------|-------|
| 8   | (no data) | -         | -      | 0     |
| 9   | 400002333 | 0.2 kWh   | 0 kWh  | 0.2   |
| 10  | 400002331 | 0.4 kWh   | 0 kWh  | 0.4   |
| 11  | 400005226 | 0 kWh     | 0 kWh  | 0     |
| 12  | 400005226 | 0 kWh     | 0 kWh  | 0     |

---

## 🚨 COMPLETE DATA ANALYSIS (ALL 12 ROWS)

### **Total Energy Calculation:**

**If Total Energy = Discharge + Charge:**

**All Discharge:** 0.1 + 0.2 + 0.4 = **0.7 kWh**
**All Charge:** 1.3 + 1.6 + 0.3 + 0.4 = **3.6 kWh**
**GRAND TOTAL:** **4.3 kWh**

### **Unique Site Count:**

1. **400005338** (rows 1, 4, 7)
2. **400002333** (rows 2, 5, 9)
3. **400002331** (rows 3, 6, 10)
4. **400005226** (rows 11, 12) ⚠️ **NEW SITE!**

**Total Unique Sites: 4**

---

## ⚠️ UPDATED BUG SUMMARY

### **BOTH Metrics Are Wrong!**

| Metric | Past Events API | Actual (Complete Data) | Discrepancy |
|--------|-----------------|------------------------|-------------|
| Total Energy | 2.3 kWh | **4.3 kWh** | **-2.0 kWh** ❌ |
| Site Count | 3 sites | **4 sites** | **-1 site** ❌ |

### **Key Finding:**

The API is missing:
- **Site 400005226** completely (not counted in site count)
- **2.0 kWh of energy** (missing from total)

**Possible reasons:**
1. API filters out sites with 0 total energy (400005226 has all 0s)
2. API only queries certain time windows (missing Page 2 data)
3. API has wrong WHERE clause or JOIN condition

---

**Status:** Juan confirmed calculation method - updating analysis

---

## 🆕 JUAN'S RESPONSE: Energy Calculation Method

**Juan confirmed:** Total Energy = **Net Energy (Charge - Discharge)**

Also requested to track:
- Column B: Discharge only
- Column C: Charge only
- Column D: Net (Charge - Discharge) ← **This is Total Energy**

---

## 🧮 RECALCULATED WITH CORRECT FORMULA

### **All Calculation Methods:**

**Method B - Discharge Only:**
```
0.1 + 0.2 + 0.4 = 0.7 kWh
```

**Method C - Charge Only:**
```
1.3 + 1.6 + 0.3 + 0.4 = 3.6 kWh
```

**Method D - Net Energy (Charge - Discharge):** ⭐ **CORRECT**
```
Row-by-row net:
Row 1: 0 - 0 = 0
Row 2: 1.3 - 0.1 = 1.2
Row 3: 1.6 - 0 = 1.6
Row 4: 0 - 0 = 0
Row 5: 0.3 - 0 = 0.3
Row 6: 0.4 - 0 = 0.4
Row 7: 0 - 0 = 0
Row 9: 0 - 0.2 = -0.2
Row 10: 0 - 0.4 = -0.4
Row 11: 0 - 0 = 0
Row 12: 0 - 0 = 0

Total Net: 1.2 + 1.6 + 0.3 + 0.4 - 0.2 - 0.4 = 2.9 kWh
```

---

## ⚠️ FINAL BUG ANALYSIS (With Correct Formula)

| Metric | Past Events API | Actual (Correct Formula) | Discrepancy |
|--------|-----------------|--------------------------|-------------|
| Total Energy (Net) | 2.3 kWh | **2.9 kWh** | **-0.6 kWh** ❌ |
| Discharge Only | ??? | 0.7 kWh | ??? |
| Charge Only | ??? | 3.6 kWh | ??? |
| Site Count | 3 sites | 4 sites | **-1 site** ❌ |

### **Key Findings:**

1. **Missing Site:** API doesn't count site 400005226
2. **Missing Energy:** API is missing 0.6 kWh of net energy
3. **Possible Cause:** API might be:
   - Filtering out site 400005226 (has 0 net energy)
   - Missing certain time windows
   - Excluding rows with negative net energy (rows 9, 10)
   - Using wrong WHERE clause

---

**Status:** Call with Juan completed - root cause identified

---

## 🆕 CALL WITH JUAN: ROOT CAUSE IDENTIFIED

### **Juan's Findings:**

**Past Events List Data Source:**
- Function: `getVPPDispatchSummary`
- Table: `silver_dispatch_result_dto` (Kusto)
- Logic: `COUNT(DISTINCT siteID WHERE command NOT LIKE '%stop%')`

**The Problem:**
Site 400005226:
- ✅ Received a dispatch command → Counted in `silver_dispatch_result_dto`
- ❌ Never actually performed → 0 energy in all telemetry rows
- 🤔 Should it be counted as "participated" or not?

### **Two Different Definitions:**

| View | Definition of "Participated" | Data Source | Includes 400005226? |
|------|------------------------------|-------------|---------------------|
| **Past Events** | Received dispatch command | `silver_dispatch_result_dto` | Maybe YES |
| **Site Performance** | Actually performed (sent telemetry) | Performance telemetry | YES (but 0 energy) |

### **The Core Issue:**

**Juan's Quote:**
> "If it never truly participated, we shouldn't have received this command either, but we count it as having participated in the function as it currently stands."

**Mismatch:**
- Command-based counting (what was **dispatched**)
- vs.
- Performance-based counting (what actually **happened**)

---

## 🎯 NEXT STEPS: Ask Naveen

### **Critical Question:**

**"Can you provide a site-by-site breakdown of the 2.3 kWh from Past Events List?"**

This will reveal:
1. Which sites are included in 2.3 kWh
2. Is site 400005226 excluded or included?
3. Where is the 0.6 kWh discrepancy?

### **Business Logic Clarification Needed:**

1. Should "Sites Dispatched" count:
   - A) Sites that received commands? OR
   - B) Sites that actually performed?

2. Should site 400005226 (command received, zero performance) be:
   - A) Included in count?
   - B) Excluded from count?

3. What is the expected behavior for the "Total Energy" calculation?

---

**Status:** Awaiting Naveen's response on site-by-site breakdown and business logic

