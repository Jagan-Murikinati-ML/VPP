# Query Timeout Solution - Batching Strategy

**Problem:** 7,781 sites cause query timeout  
**Solution:** Process in smaller batches

---

## ⚡ QUICK FIX - TEST FIRST:

### **Step 1: Run Test with 100 Sites (2-3 minutes)**

**File:** `DSGS_2026_TEST_100_Sites.kql`

**What it does:**
- Tests first 100 sites only
- Adds diagnostics (site count, meterId count)
- Limits output to 1000 rows
- Quick test to verify query works

**Expected:**
- Runtime: < 2 minutes
- Output: ~100 sites × 960 intervals = ~96,000 rows (limited to 1000 for test)
- If this works → Continue to larger batches

---

### **Step 2: Determine Optimal Batch Size**

Based on 100-site test results:

**If 100 sites = 2 minutes:**
- 500 sites = ~10 minutes ✅ (Safe)
- 1000 sites = ~20 minutes ✅ (OK)
- 2000 sites = ~40 minutes ❌ (Might timeout)

**Recommendation:** Use batches of 500-1000 sites

---

## 📊 BATCHING APPROACH:

### **Option A: Manual Batches (Simple)**

**Total sites:** 7,781  
**Batch size:** 1,000 sites  
**Number of batches:** 8 batches

**Batches:**
```
Batch 1: Sites 1-1000     (lines 16-115 from full array)
Batch 2: Sites 1001-2000  (lines 116-215)
Batch 3: Sites 2001-3000  (lines 216-315)
Batch 4: Sites 3001-4000  (lines 316-415)
Batch 5: Sites 4001-5000  (lines 416-515)
Batch 6: Sites 5001-6000  (lines 516-615)
Batch 7: Sites 6001-7000  (lines 616-715)
Batch 8: Sites 7001-7781  (lines 716-797) - Last 781 sites
```

**Steps:**
1. Copy full script 8 times
2. Change `dsgs_site_list` array in each to respective batch
3. Run each batch separately
4. Export each to CSV
5. Combine CSVs manually or with script

---

### **Option B: Automated Python Script (Advanced)**

Create Python script to:
1. Split site array into batches
2. Generate 8 separate KQL files
3. (Optional) Auto-execute and combine results

**Script:** `generate_batches.py` (I can create this if you want)

---

## 🔧 IMMEDIATE ACTION PLAN:

### **TODAY - With Juan:**

**Step 1: Run 100-site test**
```
File: DSGS_2026_TEST_100_Sites.kql
Time: 2-3 minutes
Purpose: Verify query works
```

**Step 2: Ask Juan:**
- "Query times out with 7,781 sites. I'm batching into groups of 1,000. Does this approach make sense?"
- "Any way to optimize the query to handle more sites?"
- "Should I process all batches or is 100-site test enough for now?"

---

### **AFTER CALL - If Juan approves batching:**

**Step 3: Create 8 batch scripts**
- Manually copy site IDs from full array into 8 separate files
- OR use Python script to auto-generate

**Step 4: Run all 8 batches**
- Run each batch (10-20 min each)
- Export to CSV after each batch
  - `DSGS_Batch1_April_1-10_2026.csv`
  - `DSGS_Batch2_April_1-10_2026.csv`
  - ...
  - `DSGS_Batch8_April_1-10_2026.csv`

**Step 5: Combine CSVs**
```powershell
# PowerShell command to combine
Get-Content DSGS_Batch*.csv | 
  Select-Object -Skip 1 | 
  Set-Content DSGS_Combined_April_1-10_2026.csv

# Add header manually to combined file
```

---

## 💡 ALTERNATIVE SOLUTIONS:

### **Solution 1: Increase Query Timeout (Ask Juan)**
```kql
set query_results_max_timeout = 1h;
// Then run full query
```

**Pros:** Simple  
**Cons:** May not be allowed, may still timeout

---

### **Solution 2: Use Materialized View (If Write Access)**
```kql
// Pre-create site list table
.create table DSGS_Sites_Temp (siteId: string)
// But you said no write permissions ❌
```

---

### **Solution 3: Simplify Query (Remove OEM adjustment)**

Remove SolarEdge adjustment to speed up:
```kql
// Comment out lines 905-906 (SolarEdge time adjustment)
// | extend interval_start_time_utc = iif(...)  // ← Comment this
```

**Might save:** 10-20% runtime

---

## ✅ RECOMMENDED APPROACH:

**For today's call with Juan:**
1. ✅ Show him 100-site test working
2. ✅ Explain timeout issue with full 7,781 sites
3. ✅ Propose batching into 8 groups of ~1,000 sites
4. ✅ Ask if there's a better way

**If Juan approves batching:**
1. Create 8 batch scripts
2. Run each (2-3 hours total for all 8)
3. Combine CSVs
4. Done!

**If Juan has optimization idea:**
1. Apply optimization
2. Try full 7,781 sites again
3. If works → Great!
4. If still times out → Fall back to batching

---

## 📁 FILES READY:

- ✅ `DSGS_2026_TEST_100_Sites.kql` - Test script (100 sites)
- ✅ `DSGS_2026_BATCH_1_Sites_1-1000.kql` - Batch 1 template
- ✅ `DSGS_2026_April_Extraction_MODIFIED.kql` - Full script (for reference)

---

**NEXT:** Run 100-site test, then discuss with Juan! 🚀
