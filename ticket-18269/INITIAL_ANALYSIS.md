# Ticket 18269 - Initial Analysis

## 📋 **Ticket Summary**

**Type:** User Story  
**Priority:** P2  
**Risk:** High (1)  
**Title:** Revisions needed for Fabric Asset Onboarding report

---

## 🎯 **Requirements (from ticket):**

1. **Add Type 1 Asset Information:**
   - Current report only shows `oem_name` and `oem_siteId` for **Type 0** assets
   - Need to add `oem_name` and `oem_siteId` for **Type 1** assets

2. **Add Battery Flag:**
   - Show whether the site has batteries or not

**Stakeholders:** @Sanjeev Lakkaraju @Naveen Siddalingaswamy @Kai Xu @Jasper Liu

---

## 📊 **Current Data Analysis**

### **Dataset Overview:**
- **Total Sites:** 33,510
- **Source:** Fabric Asset Onboarding Report
- **Link:** https://app.fabric.microsoft.com/groups/09c5e73c-a820-4100-aef5-d774ac0395f6/reports/b140bc27-f819-4b74-8ce6-d60b49cc583b/7c30b3e609720e59d7be

### **OEM Distribution:**
```
Qcells:       13,347 sites (40%)
SolarEdge:    10,357 sites (31%)
Tesla:         6,044 sites (18%)
Enphase:       3,759 sites (11%)
```

### **Product Type Distribution:**
```
Inverter:       17,612 records
MicroInverter:   3,904 records
NULL/Missing:   11,994 records (36%)
```

### **Product Sub Type Distribution:**
```
HybridInverter:     17,543 records
BatteryInverter:        69 records
NULL/Missing:       15,898 records (47%)
```

---

## ❓ **KEY QUESTIONS TO CLARIFY**

### **Question 1: What is "Type 0" vs "Type 1" Asset?**

**Current Observation:**
- The data has columns: `productInfo_prodType` and `productInfo_prodSubType`
- Values include: `Inverter`, `MicroInverter`, `HybridInverter`, `BatteryInverter`

**Need to clarify:**
- Does "Type 0" = Solar only (no battery)?
- Does "Type 1" = Battery/Hybrid inverter?
- OR is there a different classification system?
- Is there an `asset_type` field in the source data we're missing?

**Example from data:**
```
Tesla sites: productInfo_prodType = "Inverter", prodSubType = "HybridInverter"
Qcells sites: productInfo_prodType = NULL/NaN
```

---

### **Question 2: Battery Flag Definition**

**Need to clarify:**
- How do we determine if a site "has batteries"?
- Is it based on:
  - Option A: `productInfo_prodSubType = 'HybridInverter' OR 'BatteryInverter'`?
  - Option B: `wMaxRtg > 0` (battery capacity)?
  - Option C: OEM type (e.g., all Tesla = has battery)?
  - Option D: Different field/logic?

**Current data observations:**
```
Sites WITH productInfo data:
  - Tesla: All have "HybridInverter" (likely has battery)
  - wMaxRtg = 11500.0 (11.5 kW battery capacity)

Sites WITHOUT productInfo data:
  - Qcells: Most have NULL product info
  - wMaxRtg = NaN
  - Does this mean NO battery, or missing data?
```

---

### **Question 3: Current Report Structure**

**Need to understand:**
- What fields are currently in the report?
- What is the data source (table/function)?
- Where does `oem_name` and `oem_siteId` come from currently?
- Is there already a "Type 0" vs "Type 1" distinction in the report?

---

### **Question 4: Type 1 Asset - oem_name and oem_siteId**

**Need to clarify:**
- If Type 1 = Battery asset, what is the expected `oem_name`?
  - Same as Type 0 (e.g., Tesla, SolarEdge)?
  - Different (e.g., battery manufacturer)?
- What is the `oem_siteId` for Type 1?
  - Same as main site?
  - Different ID for battery component?
  - Is there a separate battery ID field in the source data?

**Current data:**
```
site_ids: 400061892
oem_siteId: e324135f-d738-4591-bf03-b84bb6b9ac10 (Tesla GUID)
oem_name: Tesla

Is this Type 0 (solar) or includes Type 1 (battery)?
Do we need SEPARATE oem_siteId for the battery component?
```

---

## 🔍 **MISSING INFORMATION**

### **Data Quality Issues:**
1. **36% of sites missing `productInfo_prodType`** (11,994 sites)
2. **47% of sites missing `productInfo_prodSubType`** (15,898 sites)
3. **41% of sites missing `wMaxRtg`** (13,614 sites)

**Question:** Is this expected? Or should we query from a different source?

---

## 📋 **QUESTIONS FOR NAVEEN & SANJEEV**

### **Email/Slack Template:**

```
Hi @Naveen @Sanjeev,

I'm analyzing ticket 18269 (Asset Onboarding Report revisions) and need clarification on a few points:

1. **Type 0 vs Type 1 Definition:**
   - What defines a "Type 0" asset vs "Type 1" asset?
   - Is Type 0 = Solar inverter and Type 1 = Battery/Hybrid inverter?
   - Or is there a different classification?

2. **Battery Flag Logic:**
   - How should we determine if a site "has batteries"?
   - Should we use: productInfo_prodSubType (HybridInverter/BatteryInverter), wMaxRtg > 0, or another field?
   - Many sites have NULL product info (36%) - does this mean no battery or missing data?

3. **Type 1 Asset - oem_name and oem_siteId:**
   - For Type 1 assets, what oem_name should we show?
     - Same as Type 0 (Tesla/SolarEdge) or battery manufacturer?
   - What oem_siteId should we show for Type 1?
     - Same site ID or separate battery component ID?
   - Is there a separate field in the source data for battery OEM info?

4. **Current Report:**
   - What is the current data source (table/function)?
   - Are Type 0/Type 1 already distinguished in the current report?
   - Can you share the current report structure or query?

I've analyzed the exported data (33,510 sites) and can proceed once these are clarified.

Thanks!
Jagan
```

---

## 🎯 **NEXT STEPS**

1. ✅ Exported and analyzed current report data
2. ⏳ Wait for clarification on Type 0 vs Type 1 definition
3. ⏳ Wait for battery flag logic confirmation
4. ⏳ Understand current report structure
5. ⏳ Design solution based on requirements
6. ⏳ Implement changes
7. ⏳ Test and deploy
