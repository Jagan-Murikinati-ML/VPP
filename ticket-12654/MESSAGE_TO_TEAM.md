# Message to Sanjeev & Juan - ADO-12654

**Purpose:** Request information to investigate the bug  
**Recipients:** Sanjeev Lakkaraju, Juan Pablo Culebro  

---

## 📧 MESSAGE (Copy & Paste to Teams/Email)

```
Hi @Sanjeev @Juan,

I've been assigned bug ticket ADO-12654 and have analyzed the images. I now understand the issue clearly.

## The Bug:

**Event:** Prg-20260318-85e2 (3:20 AM - 3:55 AM)

**Past Events List shows:**
- Total Energy: 2.3 kWh (from API: 2300 Wh)
- Sites Dispatched: 3

**Site-Level Performance shows:**
- 7 rows of data (same sites appear multiple times in different time windows)
- 3 unique site IDs: 400005338, 400002333, 400002331
- When I sum all energy (discharge + charge) from all 7 rows: ~3.7 kWh

**The Mismatch:**
- Energy: 2.3 kWh (Past Events) ≠ 3.7 kWh (Site Performance sum)
- Sites: Count seems correct (3 unique sites), but need to verify

## Key Observation:

The event has **multiple dispatch windows** (3:20-3:35, 3:52-3:55), so the same site appears in multiple rows with different time ranges. This is causing aggregation issues.

## What I Need:

### 1. Past Events List API
- Which API endpoint provides the Past Events List data?
- Can you share the code/query that calculates:
  - `totalEnergy` (currently showing 2300 Wh)
  - `sitesDispatched` (currently showing 3)
- Is it aggregating from Postgres or Kusto?

### 2. Site-Level Performance Data
- Where does this data come from? (Kusto telemetry table?)
- What's the correct way to sum energy when a site has multiple rows?
  - Sum ALL rows for the event? OR
  - Group by site_id first, then sum?

### 3. Energy Calculation Method - CRITICAL ⚠️
The site-level performance has two columns:
- Energy Discharged
- Energy Charged

**How should "Total Energy" be calculated?**
- A) Sum of (Discharge + Charge) for all rows? → Would give 3.7 kWh
- B) Sum of Discharge only? → Would give 0.1 kWh
- C) Sum of Charge only? → Would give 3.6 kWh
- D) Net energy (Charge - Discharge)? → Would give 3.5 kWh
- E) Something else?

**None of these match the 2.3 kWh shown in Past Events!**

Is there a filter being applied (e.g., exclude rows with 0 energy, or only count certain time windows)?

### 4. Expected Behavior
- Should site count = COUNT(DISTINCT site_id)?
- Are there any other filters I should know about?

### 5. Testing
- Is event "Prg-20260318-85e2" still in DEV?
- Can I query the raw data to verify the calculations?

## My Hypothesis:

The Past Events API is likely:
1. Missing some time windows (only counting 2.3 kWh instead of 3.7 kWh)
2. Using wrong aggregation logic (not summing all rows correctly)
3. Querying a different table than Site-Level Performance

Once I know where the API code is, I can compare it with the Site Performance query and fix the discrepancy.

Thanks!
Jagan
```

---

## 📋 FOLLOW-UP CHECKLIST

After sending the message:

- [ ] Wait for response (give 24 hours)
- [ ] If no response, ping again or ask in team channel
- [ ] Once you get code locations, document them
- [ ] Review the queries
- [ ] Update TICKET_ANALYSIS.md with findings

---

## 🎯 EXPECTED RESPONSES

### Best Case:
- They share exact file paths or query code
- They explain the data flow
- They point you to the bug location

### Likely Case:
- They share general locations
- You need to explore the code yourself
- They schedule a quick call to explain

### Worst Case:
- They're not sure / need to check with others
- You need to explore the codebase blindly
- May need to involve more people

---

## 💡 BACKUP PLAN

If they don't respond or don't know:

1. **Search the codebase:**
   - Search for "Past Events" or "PastEvents"
   - Search for event ID format: "Prg -"
   - Search for "dispatched sites" or "dispatchedSites"

2. **Check API endpoints:**
   - Look for `/api/events` or `/api/vpp/events`
   - Check Swagger/API documentation

3. **Check Kusto:**
   - Look for functions with "event" in the name
   - Check `es-eventhouse` repo

4. **Ask in team channel:**
   - Post in general VPP channel
   - Someone might know

---

**Status:** Ready to send

