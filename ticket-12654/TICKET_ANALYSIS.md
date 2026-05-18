# Bug Analysis: ADO-12654
## Total Energy & Site Count Mismatch in Past Events List

**Date:** March 20, 2026  
**Analyst:** Jagan Murikinati  
**Status:** Initial Analysis  

---

## 📋 TICKET SUMMARY

**Bug:** The total energy value & number of dispatched sites displayed in the "Past Events List" does not match the site-level performance data for the same event.

**Example Event ID:** `Prg -20260318-85e2`

**Impact:** Inconsistent reporting - users see different numbers in the summary vs. detailed view

---

## 🔍 PROBLEM BREAKDOWN

### What's Happening:
1. **Past Events List** shows:
   - Total Energy: X kWh
   - Number of Dispatched Sites: Y sites

2. **Site-Level Performance Data** (for the same event) shows:
   - Sum of all site energy (charge/discharge): Different from X
   - Count of sites with performance data: Different from Y

### Expected Behavior:
- Past Events List totals should **exactly match** the sum of site-level performance data
- Site count should match the number of sites that actually participated/dispatched

---

## 🎯 ROOT CAUSE HYPOTHESES

### Hypothesis 1: Different Data Sources
**Most Likely**

**Scenario:**
- **Past Events List** pulls from: Postgres aggregated view or cached summary table
- **Site-Level Performance** pulls from: Kusto real-time telemetry data

**Why this causes mismatch:**
- Postgres may have stale data
- Aggregation logic may be incorrect
- Data pipeline sync issues between Postgres and Kusto

---

### Hypothesis 2: Incorrect Aggregation Logic
**Likely**

**Scenario:**
- The query that calculates totals for "Past Events List" has a bug:
  - Wrong JOIN conditions (missing sites)
  - Wrong WHERE filters (excluding some sites)
  - Wrong SUM calculation (not handling NULL values)
  - Counting sites incorrectly (duplicates or missing)

---

### Hypothesis 3: Timing/Sync Issues
**Possible**

**Scenario:**
- Past Events List shows data from when event was created
- Site-Level Performance shows updated data after event completed
- No refresh mechanism to update the summary

---

### Hypothesis 4: Different Filtering Logic
**Possible**

**Scenario:**
- Past Events List counts "dispatched" sites (sites that received command)
- Site-Level Performance shows "responded" sites (sites that actually performed)
- These two numbers may legitimately differ, but should be clarified

---

## 🔎 WHAT WE NEED TO INVESTIGATE

### 1. **Find the "Past Events List" Code**
**Questions:**
- Where is this UI/API endpoint?
- What query does it run?
- What table/view does it query?
- Is it Postgres or Kusto?

**Likely locations:**
- API endpoint: `/api/events/past` or similar
- Postgres view: `vw_past_events` or `vw_event_summary`
- Kusto function: `getPastEvents()` or similar

---

### 2. **Find the "Site-Level Performance" Code**
**Questions:**
- Where is this data coming from?
- What query aggregates site performance?
- Is it real-time from Kusto or cached in Postgres?

**Likely locations:**
- Kusto query on telemetry tables
- API endpoint: `/api/events/{eventId}/sites` or similar

---

### 3. **Compare the Two Queries**
**What to check:**
- Are they querying the same tables?
- Are they using the same JOIN conditions?
- Are they filtering by the same criteria?
- Are they handling NULL values the same way?
- Are they counting/summing the same fields?

---

## 📊 DATA ARCHITECTURE (Based on Previous Work)

### Known Components:
1. **Postgres (assetdb):**
   - `asset.tb_bas_program_info` - Program metadata
   - `asset.tb_bas_site` - Site metadata
   - `asset.tb_vpp_group_site` - VPP group-site relationships
   - `asset.tb_opr_program_site_info` - Program-site operational info

2. **Kusto (Eventhouse):**
   - Event performance telemetry data
   - Site-level energy metrics
   - Real-time dispatch data

3. **Data Flow:**
   ```
   Postgres (metadata) → Data Pipeline → Kusto (silver tables)
   Kusto (telemetry) → Aggregation → Summary views
   ```

---

## 🎯 INVESTIGATION PLAN

### Step 1: Identify the Data Sources (30 min)
**Actions:**
- Ask Sanjeev/Juan: "Where does the Past Events List get its data from?"
- Ask: "Where does Site-Level Performance data come from?"
- Find the API endpoints or UI code

### Step 2: Review the Queries (1 hour)
**Actions:**
- Get the SQL/KQL queries for both views
- Compare side-by-side
- Identify differences in logic

### Step 3: Test with Example Event (30 min)
**Actions:**
- Use event ID: `Prg -20260318-85e2`
- Run both queries manually
- Document the differences

### Step 4: Propose Fix (1 hour)
**Actions:**
- Identify the incorrect query
- Write corrected version
- Test with multiple events

---

## 💬 QUESTIONS FOR SANJEEV & JUAN

### Message Draft:

```
Hi @Sanjeev @Juan,

I'm analyzing bug ADO-12654 (energy/site count mismatch in Past Events List).

To understand the root cause, I need to know:

1. **Past Events List:**
   - Where does this UI/report pull data from?
   - Is it a Postgres view, Kusto function, or API endpoint?
   - Can you share the query or code location?

2. **Site-Level Performance Data:**
   - Where does this data come from?
   - Is it real-time from Kusto telemetry or cached in Postgres?
   - Can you share the query or code location?

3. **Event ID for Testing:**
   - The ticket mentions "Prg -20260318-85e2"
   - Is this event still available in DEV for testing?

4. **Expected Behavior:**
   - Should "dispatched sites" count sites that received commands?
   - Or sites that actually responded with performance data?

Once I understand the data flow, I can identify where the aggregation logic is incorrect.

Thanks!
Jagan
```

---

## 📁 NEXT STEPS

1. ✅ Create this analysis document
2. ⏳ Send message to Sanjeev & Juan
3. ⏳ Wait for response with code locations
4. ⏳ Review queries and identify bug
5. ⏳ Propose fix
6. ⏳ Test fix in DEV
7. ⏳ Submit PR or update ticket

---

**Status:** Ready to send inquiry to team

