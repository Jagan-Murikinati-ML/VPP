# DSGS 2026 Data Extraction - Implementation Plan

**Date:** April 9, 2026  
**Ticket:** 13204  
**Developer:** Jagan Murikinati  
**Approach:** Hybrid (Shuai's Excel + Asset Registry meterId lookup)

---

## 🎯 APPROACH SUMMARY

**What we're doing:**
1. Use Shuai's Excel (7,700 site IDs) as the authoritative DSGS site list ✅
2. Look up corresponding meterId from Asset Registry for each site
3. Extract telemetry data for sites that have both siteId + meterId
4. Document sites missing meterId or telemetry data

**Why hybrid approach:**
- Shuai's Excel has `Site Id` but NOT `meterId`
- Juan's script needs `meterId` to join telemetry data
- Asset Registry can provide the siteId → meterId mapping
- Some sites (up to 2,700) may not have meterId in Asset Registry

---

## 📋 STEP-BY-STEP IMPLEMENTATION

### **STEP 1: Convert Excel to Dynamic Array (PRODUCTION-SAFE)**

**Action:** Convert Shuai's Excel site IDs to KQL dynamic array

**Why:** Production workspace has no write permissions (can't create tables/upload files)

**How:**

1. Open `Initial DSGS Site List 2026.xlsx`
2. Add new column (Column S)
3. In S2, enter formula: `="    """ & A2 & ""","`
4. Drag formula down to all 7,700 rows
5. Copy Column S (all formatted values)
6. Paste into KQL script at line 48

**See detailed guide:** `EXCEL_TO_DYNAMIC_ARRAY_GUIDE.md`

**Result:** Dynamic array with all 7,700 site IDs

**Time:** ~10 minutes

---

### **STEP 2: Complete the Modified Script**

**File:** `DSGS_2026_April_Extraction_MODIFIED.kql`

**What to do:**

1. **Paste site list array (line 48):**
   ```kql
   let dsgs_site_list = dynamic([
       "400040232",
       "400040229",
       ... (paste all 7,700 site IDs from Excel)
       "400099999"  // No comma on last item!
   ]);
   ```

2. **Verify ModelId filter (line 59):**
   ```kql
   and ModelId startswith 'dtmi:qcells:contract:leapContract'
   ```
   - ASK JUAN: Is this correct for DSGS 2026?
   - Or should it be: `dtmi:qcells:contract:dsgsContract`?

3. **Add Juan's remaining code (Lines 112-173):**
   - Copy from Juan's script: Lines 112-173
   - Paste after current script ends
   - This includes the joining logic and output formatting

---

### **STEP 3: Run Diagnostic Queries**

**Before full extraction, check data availability:**

```kql
// Query 1: How many Excel sites have meterId in Asset Registry?
let dsgs_site_list = dynamic([
    "400040232",
    ... (your full array)
]);

let meterId =
    goldAdtPropertyMinMaxLatestViewV2
    | where Key == 'meterId' and tolower(actionMax) != 'delete'
    | join kind=inner (goldAdtAllRelationshipsLatestView
        | where tolower(Action) != 'delete'
        | project siteId = Source, Target)
        on $left.Id == $right.Target
    | distinct meterId = valueMax, siteId
    | where siteId in (dsgs_site_list)  // Filter to Excel sites
;

print total_excel_sites = array_length(dsgs_site_list),
      sites_with_meterId = toscalar(meterId | count),
      sites_missing_meterId = array_length(dsgs_site_list) - toscalar(meterId | count)
```

**Expected result:**
```
total_excel_sites: 7,700
sites_with_meterId: ~5,000 (or more if Asset Registry updated)
sites_missing_meterId: ~2,700
```

---

```kql
// Query 2: Which sites are missing meterId?
let dsgs_site_list = DSGS_Sites_2026 | project siteId = tostring(SiteId);

let meterId = ... (same as above)

dsgs_site_list
| join kind=leftanti (meterId) on siteId
| join kind=inner (DSGS_Sites_2026) on $left.siteId == $right.SiteId
| project SiteId, CustomerName, OEMName, Program
| order by SiteId asc
```

**Save this list** to document missing sites for Shuai

---

```kql
// Query 3: How many sites have telemetry data for April 1-10?
let meterId = ... (site list with meterIds)

silverCommDataSite
| where siteId in (meterId | project siteId)
| where sourceTimestamp between (datetime(4/1/2026) .. datetime(4/11/2026))
| summarize interval_count = count() by siteId
| summarize sites_with_data = count(), 
            avg_intervals = avg(interval_count),
            min_intervals = min(interval_count),
            max_intervals = max(interval_count)
```

**Expected:**
- Sites with data: 5,000 (or fewer if some have no telemetry)
- Avg intervals: ~960 (10 days × 96 intervals/day)
- Some sites may have fewer intervals (missing data)

---

### **STEP 5: Run Full Extraction**

**Execute:** `DSGS_2026_April_Extraction_MODIFIED.kql`

**Expected output:**
- Format: meter_id, interval_start_time_utc, interval_end_time_utc, energy_net_kwh, ...
- Rows: ~5,000 sites × 960 intervals = ~4.8 million rows (if 5k sites have data)
- Missing intervals: Shown as "Null" in energy fields

---

### **STEP 6: Validate Output**

```kql
// Validation 1: Row count
final_output | count
// Expected: Millions of rows

// Validation 2: Unique sites
final_output | summarize dcount(meter_id)
// Expected: ~5,000 (sites with meterId + telemetry)

// Validation 3: Date range
final_output 
| summarize min(interval_start_time_utc), max(interval_start_time_utc)
// Expected: 2026-04-01 00:00:00 to 2026-04-10 23:45:00

// Validation 4: Null values
final_output
| where energy_net_kwh == "Null"
| count
// This shows missing telemetry intervals
```

---

### **STEP 7: Export to CSV**

**Option A: UI Export**
1. Run query
2. Click "Export" → CSV
3. Save as: `DSGS_April_1-10_2026.csv`

**Option B: KQL Export**
```kql
final_output
| take 1000000  // Export in chunks if too large
```

---

### **STEP 8: Document Results**

**Create summary report for Shuai:**

```
DSGS 2026 April 1-10 Data Extraction Summary

Date Range: April 1-10, 2026
Total Sites in Excel: 7,700

Results:
- Sites with meterId in Asset Registry: 5,234
- Sites missing meterId: 2,466
- Sites with telemetry data: 5,102
- Sites with no telemetry data: 132

Output:
- Total rows: 4,897,920
- Complete intervals: 4,650,000
- Missing intervals (Null): 247,920
- Output file: DSGS_April_1-10_2026.csv

Sites Missing meterId:
[Attach list from Query 2]

Sites Missing Telemetry:
[List sites with meterId but no data]

Next Steps:
- Review missing sites with Asset Registry team
- Investigate sites with no telemetry data
- Confirm DSGS program enrollment accuracy
```

---

## ⚠️ KNOWN ISSUES & MITIGATION

### **Issue 1: 2,700 sites missing meterId**

**Why:** Not all DSGS sites enrolled in Asset Registry yet

**Impact:** These sites will NOT appear in output

**Mitigation:**
- Document which sites are missing
- Shuai/Sanjeev to update Asset Registry
- Re-run extraction after update

---

### **Issue 2: Some sites have no telemetry data**

**Why:** 
- Battery not reporting data
- Communication issues
- Recently installed (no historical data)

**Impact:** Sites appear in output with all "Null" values

**Mitigation:**
- Document sites with no data
- Operations team to investigate battery connectivity

---

### **Issue 3: Missing intervals (< 960 per site)**

**Why:**
- Battery offline temporarily
- Data not yet synced
- Communication gaps

**Impact:** Some intervals show "Null"

**Mitigation:**
- Normal for real-world data
- LEAP/DSGS accepts Null intervals
- Document completion percentage

---

## 💬 QUESTIONS FOR JUAN IN CALL

1. **MeterId lookup approach**: "I'm using Asset Registry to look up meterId for Shuai's Excel sites. Does this make sense?"

2. **Missing sites**: "2,700 sites may not have meterId in Asset Registry. Should I document this and proceed, or wait for Asset Registry update?"

3. **Data validation**: "After extraction, what % of Null intervals is acceptable? What should I flag for review?"

4. **Output size**: "~5M rows expected. Should I split into multiple files or export as one large CSV?"

---

## ✅ SUCCESS CRITERIA

- [ ] All 7,700 Excel sites processed (meterId lookup attempted)
- [ ] Sites with meterId extracted successfully
- [ ] Output matches LEAP template format
- [ ] Date range correct (April 1-10, 2026)
- [ ] Missing sites documented
- [ ] Missing data documented
- [ ] CSV exported and shared with Shuai
- [ ] Summary report created

---

**Estimated Time:**
- Step 1-2 (Prep & Upload): 30 minutes
- Step 3 (Script completion): 1 hour
- Step 4 (Diagnostics): 30 minutes
- Step 5-6 (Run & Validate): 1 hour
- Step 7-8 (Export & Document): 1 hour

**Total: ~4 hours of work**
