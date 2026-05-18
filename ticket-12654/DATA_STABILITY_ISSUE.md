# Data Stability Issue - ADO-12654

**Date Discovered:** 2026-03-30  
**Issue:** `silverCommDataSite` table appears to have changing data over time

---

## 🚨 **THE PROBLEM:**

Event: **Prg -20260318-85e2**  
Event Date: **2026-03-18**  
Analysis Dates: **2026-03-27 (Monday) vs 2026-03-30 (Today)**

### **Monday 2026-03-27 - Query Results:**

**Query:**
```kusto
silverCommDataSite
| where sourceTimestamp >= datetime(2026-03-18 03:00:00)
    and sourceTimestamp < datetime(2026-03-18 04:00:00)
    and siteId in ("400005338", "400002333", "400002331", "400005226")
| summarize 
    total_charged = sum(battery_200_IncWhImp),
    total_discharged = sum(battery_200_IncWhExp),
    row_count = count(),
    min_time = min(sourceTimestamp),
    max_time = max(sourceTimestamp)
    by siteId
| extend net_energy = total_charged - total_discharged
```

**Results:**

| Site ID | Charged | Discharged | Rows | Net Energy |
|---------|---------|------------|------|------------|
| 400005226 | 0 Wh | 0 Wh | 12 | 0 Wh |
| 400002333 | 0 Wh | 1,200 Wh | 12 | -1,200 Wh |
| 400002331 | 0 Wh | 2,400 Wh | 12 | -2,400 Wh |
| **Total** | **0 Wh** | **3,600 Wh** | **36 rows** | **-3.6 kWh** |

**Evidence:** `check_all_sites_for that data_in_silvercommdatasites.csv`

---

### **Today 2026-03-30 - Query Results:**

**Same query, different results:**

- ❌ Different number of rows
- ❌ Different values
- ❌ Possibly different sites

---

## ❓ **WHY THIS IS A PROBLEM:**

1. **Cannot reproduce bug:** Data changes between analysis sessions
2. **Cannot verify UI behavior:** What did the UI show on 2026-03-18 vs what data shows today?
3. **Unreliable investigation:** Analysis based on unstable data
4. **Cannot pinpoint root cause:** If data changes, we can't tell if:
   - UI had a bug on the event date
   - Data was wrong on the event date
   - Data pipeline changed values later
   - We're querying the wrong table

---

## ✅ **QUESTIONS FOR TEAM:**

### **Question 1: Is `silverCommDataSite` a live/mutable table?**

- Does it get updated/recalculated over time?
- Is there a data refresh process?
- Should we use a historical/snapshot table instead?

---

### **Question 2: What table does the UI actually use?**

- Past Events List: Which table/API?
- Site-Level Performance: Which table/API?
- Are they reading from `silverCommDataSite` or something else?

---

### **Question 3: Is there a stable historical table?**

Possible names:
- `gold_site_performance`
- `silverCommDataSite_archive`
- `historical_telemetry`
- Materialized view
- API endpoint that returns stable results

---

### **Question 4: Can we query the Past Events List API directly?**

Instead of reverse-engineering from database:
- API endpoint URL
- Authentication method
- Request format for event summary

This would give us the EXACT values the UI shows.

---

## 🎯 **IMPACT ON ADO-12654:**

### **Current Status:**

**What we know from Monday's data:**
- Event2 has NO data in `silverCommDataSite`
- Event1 + Event3 = 3.6 kWh discharged (negative net)
- Site 400005226 has 0 performance
- 4 sites received commands, 3 have energy

**What we DON'T know:**
- Is this data still accurate today?
- Did the UI see different values on the event date?
- Where does the 2.9 kWh in Site-Level Performance come from if not this table?

---

## 📝 **NEXT STEPS:**

1. ✅ Ask Naveen about historical/snapshot tables
2. ✅ Ask for Past Events List API endpoint
3. ✅ Confirm which table the UI reads from
4. ✅ Check if there are materialized views
5. ✅ Hold investigation until we have stable data source

---

## 💾 **PRESERVED EVIDENCE:**

All CSV files from Monday 2026-03-27 are saved:
- `check_all_sites_for that data_in_silvercommdatasites.csv`
- `event1_data_in_silvercommdatasite.csv`
- `event3_data_in_silvercommdatasite.csv`
- `event1_summary.csv`
- `event3_summary.csv`

These represent the data as it existed on Monday and are our baseline for comparison.

---

**Created:** 2026-03-30  
**Status:** BLOCKED - Waiting for data source clarification

