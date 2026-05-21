# Ticket 18269 - Next Steps

## ✅ **What We've Done So Far**

1. **Understood the Ticket Requirements:**
   - Add Type 1 asset `oem_name` and `oem_siteId` to the report
   - Add battery flag

2. **Clarified Type 0 vs Type 1:**
   - Type 0 = `oemInfo.0` (first OEM - typically solar/inverter)
   - Type 1 = `oemInfo.1` (second OEM - typically battery, if different)

3. **Understood Asset Registry Structure:**
   - `goldAdtPropertyMinMaxLatestViewV2` - Properties (Key-Value pairs)
   - `goldAdtAllRelationshipsLatestView` - Relationships
   - `goldAdtTwinEventsLatestV2` - Twin existence

4. **Created Test Queries:**
   - `test_sites_query.kql` - Find sites with Type 1 OEM data

---

## 🔄 **What We Need to Do Next**

### **Step 1: Run Test Queries** ⏭️

Execute `test_sites_query.kql` to:
1. Find sites with Type 1 OEM information
2. Check OEM combinations (e.g., Enphase + Qcells)
3. Identify battery devices
4. Compare battery detection methods

**Action:** Run the KQL queries in Azure Data Explorer or Fabric

---

### **Step 2: Analyze Test Sites** ⏭️

Pick 3-5 test sites:
1. **Site with Type 1 OEM** (e.g., Solar from Enphase, Battery from Tesla)
2. **Site with only Type 0** (e.g., Qcells solar only)
3. **Site with battery** (e.g., Tesla Powerwall)
4. **Site without battery** (e.g., Qcells solar only)

For each site:
- Note current report output (from `data.csv`)
- Query Asset Registry for full details
- Document what SHOULD be in the report

---

### **Step 3: Compare with Current Report** ⏭️

Create a comparison table:

| Site ID | Current Type 0 OEM | Current Type 1 OEM | Expected Type 1 OEM | Has Battery (Expected) |
|---------|-------------------|-------------------|--------------------|-----------------------|
| 400061892 | Tesla | NULL | ??? | Yes (HybridInverter) |
| 100001549 | Qcells | NULL | ??? | No (prodSubType=NULL, wMaxRtg=0) |

---

### **Step 4: Ask Shuai for Clarification (if needed)** ⏭️

Questions to ask:
1. For sites with Type 1 OEM, what should we show?
   - Example: If solar is from Enphase and battery is from Qcells, should we show both?
2. For battery flag, which logic should we use?
   - Option A: `prodSubType in ('HybridInverter', 'BatteryInverter')`
   - Option B: `wMaxRtg > 0`
   - Option C: Check for battery device in relationships
3. Should we add Type 2, Type 3, Type 4 OEM as well? (we found up to `oemInfo.4`)

---

### **Step 5: Identify Current Report Data Source** ⏭️

We need to find:
- Is there a KQL function that generates the current report?
- Is it a materialized view?
- Is it a Power BI dataset?
- Where is the current `data.csv` coming from?

**Possible locations:**
- Look for functions with names like `getAssetOnboardingReport` or `getSiteList`
- Check for materialized views
- Look in the Fabric workspace

---

### **Step 6: Implement the Solution** ⏭️

Once we have clarity:
1. Modify the report query/function to include:
   - `type1_oem_name` (from `oemInfo.1.oemName`)
   - `type1_oem_siteId` (from `oemInfo.1.oemSiteId`)
   - `has_battery` (boolean flag)

2. Test with our test sites

3. Validate output matches expected results

---

## 📋 **Immediate Action Items**

1. **RUN** `test_sites_query.kql` in Fabric/Azure Data Explorer
2. **EXPORT** results to CSV for analysis
3. **PICK** 3-5 test sites for detailed comparison
4. **FIND** the current report data source (function/view/dataset)
5. **ASK** Shuai for clarification on expected output

---

## 📂 **Files Created**

- ✅ `UNDERSTANDING.md` - Detailed understanding of requirements
- ✅ `test_sites_query.kql` - Test queries to find sites
- ✅ `NEXT_STEPS.md` - This file

---

**Ready to proceed with Step 1: Run test queries** 🚀

Let me know when you've run the queries and we can analyze the results together!
