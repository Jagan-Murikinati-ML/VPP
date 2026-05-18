# Quick Start - Run the Script

**File:** `DSGS_2026_April_Extraction_MODIFIED.kql`  
**Status:** ✅ READY TO RUN (944 lines)

---

## ⚡ FASTEST PATH TO RESULTS:

### **Step 1: Open Script (30 seconds)**
- File: `DSGS_2026_April_Extraction_MODIFIED.kql`
- Open in Fabric/Eventhouse query editor

### **Step 2: Verify ONE Setting (1 minute)**
**Line 841:** Check ModelId
```kql
and ModelId startswith 'dtmi:qcells:contract:leapContract'
```
- ✅ If DSGS uses LEAP contracts → Keep as-is
- ❌ If DSGS has separate contract → Ask Juan what to change to

### **Step 3: Run Diagnostic (2 minutes)**
**Copy lines 1-857 and add:**
```kql
print total_excel_sites = array_length(dsgs_site_list),
      sites_with_meterId = toscalar(meterId | count),
      missing_meterId = array_length(dsgs_site_list) - toscalar(meterId | count)
```

**Expected output:**
```
total_excel_sites: 7781
sites_with_meterId: ~5000
missing_meterId: ~2700
```

If numbers look reasonable → Continue  
If sites_with_meterId = 0 → Check ModelId!

### **Step 4: Run Full Script (5-15 minutes)**
- Execute entire script (all 944 lines)
- Wait for completion
- Check row count

**Expected:** ~4-5 million rows

### **Step 5: Export CSV (5-10 minutes)**
- Click "Export" → CSV
- Save as: `DSGS_April_1-10_2026.csv`
- File size: Hundreds of MB

### **Step 6: Document Results (5 minutes)**
Create summary:
```
DSGS April 1-10 Extraction Results:

Excel Sites: 7,781
Sites with meterId: X
Sites with telemetry: Y
Total rows: Z
File: DSGS_April_1-10_2026.csv

Missing Sites: X - Y = Z sites
(List attached separately)
```

---

## 🆘 IF SOMETHING GOES WRONG:

### **Error: "meterId not found" or similar**
**Fix:** Line 841 - change ModelId to correct DSGS contract type

### **Error: Query timeout**
**Fix:** Split into batches - run for 2000 sites at a time

### **Warning: Too many NULL values (>50%)**
**Check:** Is telemetry data available for April 1-10?

---

## ✅ THAT'S IT!

**Total time:** ~30 minutes (if everything works)

**You're ready to run!** 🚀
