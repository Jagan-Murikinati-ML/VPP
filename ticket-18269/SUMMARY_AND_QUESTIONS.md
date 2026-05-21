# Ticket 18269 - Summary & Questions for Shuai

## 📊 **What We've Discovered**

### **1. Type 1 OEM Data Exists (But Rarely)**

From Query 2 analysis:
- **Total Sites:** ~61,269
- **Sites with ONLY Type 0 OEM:** 60,725 (98.5%)
- **Sites with Type 1 OEM:** 544 (1.5%)

**Most Common Type 1 Combinations:**
- Qcells + Tesla: 328 sites (solar from Qcells, battery from Tesla)
- Enphase + Tesla: 67 sites (solar from Enphase, battery from Tesla)
- SolarEdge + Tesla: 20 sites (solar from SolarEdge, battery from Tesla)

### **2. Test Site Analysis**

**Site: 100003907** (Real example with Type 1 OEM)

**Current Report Shows:**
```
oem_name:    Qcells
oem_siteId:  100003907
```

**Asset Registry Has:**
```
Type 0: Qcells / 100003907
Type 1: Qcells / SSMAK9HTBP  ⬅️ MISSING FROM CURRENT REPORT!
```

**This site also has a battery device** (confirmed via Query 3).

---

## 🎯 **What Needs to Be Added**

### **1. Type 1 OEM Columns**

Add two new columns:
- `type1_oem_name` (from `oemInfo.1.oemName`)
- `type1_oem_siteId` (from `oemInfo.1.oemSiteId`)

**Expected Output:**
```csv
site_ids,oem_name,oem_siteId,type1_oem_name,type1_oem_siteId,has_battery,...
100003907,Qcells,100003907,Qcells,SSMAK9HTBP,Yes,...
400061892,Tesla,e324135f-...,,,Yes,...
100001549,Qcells,100001549,,,No,...
```

### **2. Battery Flag Column**

Add one new column:
- `has_battery` (Yes/No or True/False)

**Detection Options:**
- **Option A:** `productInfo_prodSubType in ('HybridInverter', 'BatteryInverter')`
  - ❌ Issue: Many sites have NULL product info
- **Option B:** `nameplateInfo.wMaxRtg > 0`
  - ❌ Issue: Many sites have empty wMaxRtg
- **Option C:** Check for battery device in Asset Registry relationships
  - ✅ Most accurate, but more complex

---

## ❓ **Questions for Shuai**

### **Question 1: Output Format Confirmation** ⭐

For site `100003907`, should the report output be:

```csv
site_ids,oem_name,oem_siteId,type1_oem_name,type1_oem_siteId,has_battery
100003907,Qcells,100003907,Qcells,SSMAK9HTBP,Yes
```

**Is this the expected format?** Should we add these 3 new columns?

---

### **Question 2: Type 1 OEM Meaning** ⭐

For site `100003907`:
- Type 0 OEM: Qcells / 100003907 (site ID)
- Type 1 OEM: Qcells / SSMAK9HTBP (looks like device serial?)

**What does Type 1 represent?**
- Solar inverter OEM vs Battery OEM?
- Main device vs Secondary device?
- Something else?

**Context:** We found 328 sites with "Qcells + Tesla", which suggests:
- Type 0 = Solar OEM (Qcells)
- Type 1 = Battery OEM (Tesla)

**Is this correct?**

---

### **Question 3: Examples of Multi-OEM Sites** ⭐

Can you provide 1-2 example site IDs for each combination:

1. **Qcells (solar) + Tesla (battery)** - Site ID: ?
2. **Enphase (solar) + Tesla (battery)** - Site ID: ?
3. **SolarEdge (solar) + Tesla (battery)** - Site ID: ?

We want to verify the expected output for these specific scenarios.

**OR** we can run `find_multi_oem_sites.kql` to find examples ourselves.

---

### **Question 4: Battery Flag Logic** ⭐

Site `100003907` has:
- Empty `productInfo_prodSubType`
- Empty `nameplateInfo.wMaxRtg`
- But HAS a battery device (confirmed via relationships)

**Which method should we use to determine battery flag?**

**Option A:** Product info fields
```kql
has_battery = prodSubType in ('HybridInverter', 'BatteryInverter')
```

**Option B:** Battery capacity
```kql
has_battery = wMaxRtg > 0
```

**Option C:** Check for battery device in relationships (most accurate)
```kql
has_battery = exists battery device with ModelId startswith 'dtmi:qcells:device:batt'
```

**Recommendation:** Option C (relationship-based) for accuracy.

---

### **Question 5: Current Report Data Source** ⭐

**Where does the current Asset Onboarding report data come from?**

- KQL function name?
- Materialized view name?
- Power BI dataset/semantic model?

We need to know what to modify to add the new columns.

---

### **Question 6: Empty Type 1 Values**

98.5% of sites will have empty Type 1 values.

**Should we:**
- A) Show empty cells (blank)
- B) Show `NULL`
- C) Show `N/A`
- D) Only show Type 1 if it's different from Type 0

---

## 📋 **Next Steps**

### **Option 1: We Run Additional Queries** (Recommended)

1. Run `find_multi_oem_sites.kql` to get examples of:
   - Qcells + Tesla sites
   - Enphase + Tesla sites
   - SolarEdge + Tesla sites
2. Compare these with current report data
3. Create draft expected output
4. Show you for confirmation

**Estimated Time:** 30 minutes

### **Option 2: You Provide Example Sites**

You give us 1-2 site IDs for each combination, and we'll:
1. Query their details
2. Create expected output
3. Show you for confirmation

**Estimated Time:** 15 minutes

---

## 🎯 **After Clarification**

Once you confirm the above questions, we can:

1. ✅ Identify the current report data source
2. ✅ Modify the query/function to add:
   - `type1_oem_name`
   - `type1_oem_siteId`
   - `has_battery`
3. ✅ Test with our example sites
4. ✅ Validate output matches expectations
5. ✅ Deploy to production

---

## 📂 **Files for Reference**

- `QUERY_RESULTS_ANALYSIS.md` - Detailed analysis of query results
- `TEST_SITE_COMPARISON.md` - Site 100003907 analysis
- `find_multi_oem_sites.kql` - Query to find multi-OEM examples
- `data.csv` - Current report output

---

**Which option do you prefer? Or should we proceed with running the additional queries?** 🚀
