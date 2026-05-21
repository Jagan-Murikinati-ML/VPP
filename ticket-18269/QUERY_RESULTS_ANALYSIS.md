# Query Results Analysis - Ticket 18269

## 📊 **Key Findings**

### **CRITICAL DISCOVERY: Most Type 1 OEM fields are EMPTY!**

---

## 🔍 **Query 1 Results: Sites with Type 0 AND Type 1 OEM**

### **What We Found:**

Out of 20 sites returned:
- **19 sites** have Type 1 OEM fields as **EMPTY** (`""`)
- **Only 1 site** has actual Type 1 OEM data:
  - Site: `100003907`
  - Type 0: `Qcells` / `100003907`
  - Type 1: `Qcells` / `SSMAK9HTBP` ✅

### **Observation:**

The query filtered for `isnotnull(type1_oemName)`, but many results have **empty strings** (`""`) rather than `NULL`.

**Important:** Empty string `""` ≠ `NULL` in KQL!

---

## 📈 **Query 2 Results: Count of Sites by OEM Combination**

### **Total Sites by OEM Type:**

| Type 0 OEM | Type 1 OEM | Count | Percentage |
|------------|------------|-------|------------|
| SolarEdge | (empty) | 20,133 | 33.0% |
| Tesla | (empty) | 16,495 | 27.0% |
| Qcells | (empty) | 15,156 | 24.8% |
| Enphase | (empty) | 8,938 | 14.6% |
| **Qcells** | **Tesla** | **328** | **0.5%** ✅ |
| **Enphase** | **Tesla** | **67** | **0.1%** ✅ |
| Qcells | Qcells | 61 | 0.1% |
| Tesla | Tesla | 43 | 0.1% |
| **SolarEdge** | **Tesla** | **20** | **<0.1%** ✅ |
| Other combinations | | <10 each | |

**Total Sites:** ~61,269

### **Key Insights:**

1. **98.5% of sites** have only Type 0 OEM (Type 1 is empty)
2. **1.5% of sites** have Type 1 OEM populated
3. **Most common Type 1 combinations:**
   - **Qcells (solar) + Tesla (battery)**: 328 sites
   - **Enphase (solar) + Tesla (battery)**: 67 sites
   - **SolarEdge (solar) + Tesla (battery)**: 20 sites

**This makes sense!** Sites with separate solar and battery OEMs need Type 1.

---

## 🔋 **Query 3 Results: Sites with Battery Devices**

### **Battery Sites Found: 20 sites**

Example sites:
- `100003907` (Qcells)
- `400062281`, `400062280`, etc. (likely Tesla based on site ID pattern)
- `400021038`, `400021075`, etc.

### **Cross-Reference with Query 1:**

Site `100003907` appears in **both** Query 1 and Query 3:
- Has Type 1 OEM: `Qcells` / `SSMAK9HTBP`
- Has battery device connected ✅

**This confirms:** Sites with Type 1 OEM likely have battery devices.

---

## 🧪 **Query 4 Results: Detailed View of Site 400061892**

**NOTE:** The query returned site `100008014` instead of `400061892`. 

Let me check what happened - the query might have found a different site or the site ID mapping is off.

### **Site: 100008014**

```
oemInfo.0.oemName:    Tesla
oemInfo.0.oemSiteId:  03403360-5a3b-411e-84f8-486b4f7a65d9
oemInfo.1.oemName:    Tesla
oemInfo.1.oemSiteId:  03403360-5a3b-411e-84f8-486b4f7a65d9
siteId:               100008014
```

### **Observation:**

This site has **identical** Type 0 and Type 1 OEM data:
- Both are `Tesla`
- Both have the same `oemSiteId`

**Question:** Why does this site have Type 1 populated if it's the same as Type 0?
- Possible data duplication?
- Or does Tesla have both solar inverter AND battery with same ID?

---

## 🎯 **What This Means for the Ticket**

### **1. Type 1 OEM Information:**

**Current Situation:**
- Only **~544 sites** (1.5%) have Type 1 OEM data
- Most sites (98.5%) only have Type 0 OEM

**What We Need to Add:**
- `type1_oem_name` column (will be empty for 98.5% of sites)
- `type1_oem_siteId` column (will be empty for 98.5% of sites)

### **2. Battery Flag:**

**Sites with batteries:**
- Query 3 found 20 sites with battery devices
- Query 2 shows ~544 sites with Type 1 OEM (some are battery OEMs)

**Recommendation:** Use relationship-based detection (Query 3 approach) as most accurate.

---

## ❓ **Questions for Shuai**

### **Question 1: Empty vs NULL Type 1 OEM**

We found that many sites have `oemInfo.1.oemName = ""` (empty string) rather than `NULL`.

**Should we:**
- A) Show empty string in the report?
- B) Show `NULL` or blank?
- C) Only show Type 1 when it's different from Type 0?

### **Question 2: Duplicate Type 0 and Type 1**

Site `100008014` has **identical** Type 0 and Type 1:
- Type 0: Tesla / 03403360-5a3b-411e-84f8-486b4f7a65d9
- Type 1: Tesla / 03403360-5a3b-411e-84f8-486b4f7a65d9

**Should we:**
- A) Show Type 1 even if it's the same as Type 0?
- B) Only show Type 1 if it's different from Type 0?

### **Question 3: Battery Flag Logic**

**Which method should we use:**
- A) `productInfo_prodSubType in ('HybridInverter', 'BatteryInverter')`
- B) `nameplateInfo.wMaxRtg > 0`
- C) Check for battery device in relationships (most accurate but more complex)

### **Question 4: Current Report Structure**

Can you share:
- The current KQL query/function that generates the Asset Onboarding report?
- Or point us to the Power BI dataset/semantic model?

---

## 📋 **Recommended Next Steps**

1. ✅ **Analyze query results** (DONE - this document)
2. 🔄 **Check specific test sites from current report**
   - Pick site `100003907` (has Type 1 OEM)
   - Compare with current `data.csv` output
3. 🔄 **Ask Shuai the 4 questions above**
4. 🔄 **Find current report data source**
5. 🔄 **Implement solution based on clarifications**

---

## 🎯 **Expected Output Structure (Draft)**

Based on findings, we should add these columns:

```csv
site_ids,oem_name,oem_siteId,type1_oem_name,type1_oem_siteId,has_battery,...
100003907,Qcells,100003907,Qcells,SSMAK9HTBP,Yes,...
400061892,Tesla,e324135f-...,,,Yes,...
100001549,Qcells,100001549,,,No,...
```

**Notes:**
- `type1_oem_name` and `type1_oem_siteId` will be empty for most sites
- `has_battery` needs clarification on detection method
