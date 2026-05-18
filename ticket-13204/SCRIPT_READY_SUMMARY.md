# DSGS 2026 Script - READY TO RUN! ✅

**Date:** April 9, 2026  
**Ticket:** 13204  
**Script:** `DSGS_2026_April_Extraction_MODIFIED.kql`  
**Status:** ✅ COMPLETE AND READY

---

## ✅ WHAT'S BEEN COMPLETED:

### **1. Site List Array (Lines 16-800)**
- ✅ All 7,781 site IDs from Shuai's Excel
- ✅ Compact format (10 sites per line)
- ✅ Total: 779 lines instead of 7,781 lines
- ✅ Production-safe (no write permissions needed)

### **2. Date Range Configuration (Lines 12-13)**
- ✅ Start: April 1, 2026
- ✅ End: April 11, 2026 (to include all of April 10)

### **3. Bad Data Filter (Lines 23-29)**
- ✅ Removes battery values >= 7500 Wh or < 0
- ✅ Date range: March 25 - April 15 (wider range for safety)

### **4. Time Backbone (Line 32)**
- ✅ Creates 15-minute intervals
- ✅ Total: 960 intervals (10 days × 96 intervals/day)

### **5. meterId Lookup (Lines 838-857)**
- ✅ Fetches from Asset Registry
- ✅ Filters to only sites in dsgs_site_list
- ✅ Returns (meterId, siteId) pairs

### **6. Telemetry Data Extraction (Lines 862-869)**
- ✅ Joins telemetry data for matched sites
- ✅ Removes bad data records
- ✅ Normalizes timestamps to 15-min intervals

### **7. Complete Juan's Logic (Lines 869-944)**
- ✅ OEM list for SolarEdge adjustment
- ✅ Join site list × time backbone × telemetry
- ✅ Energy calculations (Wh → kWh conversion)
- ✅ SolarEdge time adjustment
- ✅ Aggregation and formatting
- ✅ Output in LEAP template format

---

## 📊 EXPECTED OUTPUT:

**Format:**
```csv
meter_id,interval_start_time_utc,interval_end_time_utc,energy_net_kwh,energy_consumed_kwh,energy_generated_kwh,final,region
f9e463b0-3e50-4abe-9b83-2086403ad102,2026-04-01T00:00:00.0000Z,2026-04-01T00:15:00.0000Z,2.345,3.100,0.755,true,CA
...
```

**Expected Row Count:**
- Sites in Excel: 7,781
- Sites with meterId in Asset Registry: ~5,000 (estimated)
- Sites with telemetry data: ~5,000
- Intervals per site: 960
- **Total rows:** ~5,000 sites × 960 intervals = ~4.8 million rows

**File Size:** Large (hundreds of MB)

---

## 🎯 BEFORE RUNNING - CHECKLIST:

### **1. Verify ModelId (Line 841)**
```kql
and ModelId startswith 'dtmi:qcells:contract:leapContract'
```

**⚠️ ASK JUAN:** Is this correct for DSGS 2026?
- Option A: Keep as `leapContract` (if DSGS sites are under LEAP contract)
- Option B: Change to `dsgsContract` (if different contract type)

### **2. Check Access to Tables:**
- ✅ goldAdtPropertyMinMaxLatestViewV2
- ✅ goldAdtAllRelationshipsLatestView
- ✅ silverCommDataSite

### **3. Estimate Query Time:**
- 7,781 sites in dynamic array
- ~5,000 sites with meterId
- 10 days of data
- **Expected runtime:** 5-15 minutes (depending on cluster size)

---

## 🚀 HOW TO RUN:

### **Option 1: Run Full Script**

1. Open Fabric/Eventhouse
2. Paste entire script (944 lines)
3. Execute
4. Wait for completion (~5-15 min)
5. Export results to CSV

### **Option 2: Run Diagnostics First (RECOMMENDED)**

**Step 1: Check how many sites have meterId**
```kql
// Just run lines 1-857 and add this:
meterId | count
```

**Expected:** ~5,000 sites

**Step 2: Check telemetry availability**
```kql
// Run up to line 869 and add this:
sites | summarize dcount(siteId)
```

**Expected:** ~5,000 sites

**Step 3: Run full script**
Once diagnostics look good, run complete script

---

## 📝 VALIDATION QUERIES (After Running):

### **Query 1: Row Count**
```kql
// After running full script, check:
... | count
```
**Expected:** 4-5 million rows

### **Query 2: Unique Sites**
```kql
... | summarize dcount(meter_id)
```
**Expected:** ~5,000 unique meters

### **Query 3: Date Range**
```kql
... | summarize min(interval_start_time_utc), max(interval_start_time_utc)
```
**Expected:** 2026-04-01 to 2026-04-10

### **Query 4: Null Percentage**
```kql
... | summarize 
    total = count(),
    null_values = countif(energy_net_kwh == "Null"),
    null_pct = round(100.0 * countif(energy_net_kwh == "Null") / count(), 2)
```
**Acceptable:** < 20% null values

---

## ⚠️ EXPECTED ISSUES:

### **Issue 1: Sites Missing from Output**
**Count:** ~2,700 sites (7,781 - 5,000)
**Reason:** Not in Asset Registry
**Action:** Document for Shuai/Sanjeev

### **Issue 2: Some Null Values**
**Reason:** Battery offline, no telemetry data
**Action:** Normal - LEAP accepts Null values

### **Issue 3: Query Timeout**
**Reason:** Too many sites in dynamic array
**Solution:** Split into batches of 2,000 sites each

---

## 📧 EXPORT TO CSV:

### **Option A: UI Export**
1. Run query
2. Click "Export" → CSV
3. Save as: `DSGS_April_1-10_2026.csv`

### **Option B: Split Export (If file too large)**
```kql
// Export in chunks
... | where meter_id startswith "a" or meter_id startswith "b" ...
```

---

## 💬 QUESTIONS FOR JUAN (Call Today):

1. **ModelId:** Is `dtmi:qcells:contract:leapContract` correct for DSGS 2026?
2. **SolarEdge adjustment:** Still needed for April 2026? (Lines 905-906)
3. **Performance:** Any tips for optimizing 7,781-site query?
4. **Output size:** Should I split CSV if > 1GB?

---

## ✅ SUCCESS CRITERIA:

- [x] Script compiles (no syntax errors) ✅
- [ ] Run diagnostic queries
- [ ] Full script executes successfully
- [ ] Output format matches LEAP template
- [ ] Date range correct (April 1-10)
- [ ] Row count reasonable (~4-5M rows)
- [ ] CSV exported
- [ ] Missing sites documented

---

## 📁 FILES:

- ✅ `DSGS_2026_April_Extraction_MODIFIED.kql` (944 lines) - **READY TO RUN**
- ✅ `JUAN_SCRIPT_ANALYSIS.md` - Understanding guide
- ✅ `IMPLEMENTATION_PLAN.md` - Step-by-step plan
- ✅ `dsgs_site_list_array_compact.kql` - Site array (already in main script)

---

**Status:** ✅ SCRIPT READY - REVIEW WITH JUAN, THEN EXECUTE!

**Next:** Call with Juan → Confirm ModelId → Run script → Export CSV → Document results
