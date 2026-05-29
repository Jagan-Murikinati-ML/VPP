# Ticket 19400 - Validation Script Summary

**Status:** ✅ **READY TO EXECUTE**  
**Date:** 2026-05-29  
**Author:** Jagan Murikinati

---

## 🎯 **WHAT WAS CREATED**

### **Primary Deliverable:**
**`DSGS_LeapContract_Validation_READY.kql`** - Complete validation query (1,741 lines)

This query:
- ✅ Contains all 8,188 enrolled DSGS site IDs (embedded in datatable)
- ✅ Queries Asset Registry for sites with Leap Contracts
- ✅ Compares enrolled list vs AR and identifies missing sites
- ✅ Generates summary statistics and detailed reports
- ✅ Ready to run in Fabric/Eventhouse (NO manual edits needed)

---

## 📊 **VALIDATION LOGIC**

### **Data Sources:**

1. **Enrolled Site List** (8,188 sites)
   - Source: `leap_meters_export_05282026.csv` (provided by Shuai)
   - Format: CSV with column "Asset Registry Site ID (partner_reference)"
   - Breakdown: 7,990 sites (400-series), 196 sites (100-series), 2 other

2. **Asset Registry Leap Contracts**
   - Table: `goldAdtPropertyMinMaxLatestViewV2`
   - Filter: `Key == 'meterId'` AND `ModelId startswith 'dtmi:qcells:contract:leapContract'`
   - Join: `goldAdtAllRelationshipsLatestView` to get linked siteIds
   - No date filter (checks current registry state)

### **Comparison:**
- LEFT OUTER JOIN: Enrolled sites → AR sites with Leap Contracts
- Output: Each enrolled site flagged as "Has" or "Missing" Leap Contract

---

## 📈 **QUERY OUTPUTS**

### **1. Summary Statistics**
```
Metric                          | Value  | Percentage
--------------------------------|--------|------------
Total Enrolled DSGS Sites       | 8,188  | 100%
Sites WITH Leap Contract        | ???    | ???%
Sites MISSING Leap Contract     | ???    | ???%
```

### **2. Full Validation Results**
- Table with all 8,188 sites
- Columns: `siteId`, `meterId`, `leap_contract_status`
- Sorted by status, then siteId

### **3. Sites Missing Leap Contracts**
- Filtered list of sites WITHOUT Leap Contracts in AR
- This is the **action list** to share with AR team
- Export to CSV and send to @Ashok Bhaskar, @Chanhyup.Kim

---

## 🔧 **SUPPORTING FILES**

| File | Purpose | Status |
|------|---------|--------|
| `parse_enrolled_sites.py` | Extract site IDs from CSV | ✅ Complete |
| `enrolled_sites_kql_array.txt` | KQL dynamic array of site IDs | ✅ Generated |
| `generate_validation_query.py` | Generate complete KQL query | ✅ Complete |
| `DSGS_LeapContract_Validation_READY.kql` | **Primary query** | ✅ Ready to run |
| `README.md` | Comprehensive documentation | ✅ Complete |
| `VALIDATION_SUMMARY.md` | This file | ✅ Complete |

---

## 🚀 **HOW TO RUN**

### **Step 1: Execute Query**
1. Open Fabric/Eventhouse
2. Load: `ticket-19400/DSGS_LeapContract_Validation_READY.kql`
3. Click "Run" (entire query)
4. Wait for results (~30-60 seconds)

### **Step 2: Review Results**
- Check summary statistics
- Identify count of missing sites
- Review "SITES MISSING LEAP CONTRACTS" table

### **Step 3: Export Missing Sites**
- Click on "SITES MISSING LEAP CONTRACTS" table
- Export to CSV
- Save as: `dsgs_sites_missing_leap_contracts_YYYYMMDD.csv`

### **Step 4: Report to AR Team**
- Email CSV to @Ashok Bhaskar, @Chanhyup.Kim
- CC: @Shuai Zhang, @Juan Culebro, @Kai Xu, @Sanjeev Lakkaraju
- Subject: "DSGS Sites Missing Leap Contracts in Asset Registry - Action Required"
- Template message below ⬇️

---

## 📧 **EMAIL TEMPLATE FOR AR TEAM**

```
Subject: DSGS Sites Missing Leap Contracts in Asset Registry - Action Required

Hi Ashok and Chanhyup,

As per Shuai's request (Ticket 19400), I've validated the enrolled DSGS site list 
against Asset Registry Leap Contracts.

VALIDATION RESULTS:
- Total enrolled DSGS sites: 8,188
- Sites WITH Leap Contract in AR: [INSERT COUNT]
- Sites MISSING Leap Contract in AR: [INSERT COUNT]

ATTACHED:
CSV file containing site IDs that are missing Leap Contracts in Asset Registry.

REQUEST:
Could you please add Leap Contracts in AR for these missing sites as soon as possible?
We need all 8,188 sites to have Leap Contracts before we can extract April & May 2026 
interval data for DSGS reporting.

Once completed, please let me know so I can re-run the validation and proceed with 
the data extraction.

Thank you!

Best regards,
Jagan Murikinati

CC: Shuai Zhang, Juan Culebro, Kai Xu, Sanjeev Lakkaraju, Jasper Liu
```

---

## 🔄 **NEXT STEPS AFTER AR UPDATE**

1. **Wait for AR team confirmation** (Leap Contracts added)
2. **Re-run validation query** (`DSGS_LeapContract_Validation_READY.kql`)
3. **Verify 100% match** (all 8,188 sites have Leap Contracts)
4. **Proceed with data extraction:**
   - April 2026: 2026-04-01 to 2026-04-30
   - May 2026: 2026-05-01 to 2026-05-31
   - All 8,188 DSGS sites
   - 15-minute battery interval data

---

## ⚙️ **TECHNICAL DETAILS**

### **Why No Date Filter?**
- Leap Contracts are **enrollment records** in Asset Registry
- They represent a relationship between a site and a contract twin
- Either the relationship exists or it doesn't (current state)
- NOT time-series data (no temporal changes to validate)

### **ModelId Verification:**
From previous analysis (ticket-13204):
```kql
goldAdtPropertyMinMaxLatestViewV2
| distinct ModelId
```
Result: `dtmi:qcells:contract:leapContract;1`

Therefore, using `startswith 'dtmi:qcells:contract:leapContract'` handles versioning.

### **Site ID Format:**
- 400-series: Standard VPP sites (7,990 sites)
- 100-series: Legacy/older sites (196 sites)  
- Other: 106019767, 233130499 (2 sites)
- All formats supported by AR

---

## ✅ **VALIDATION CHECKLIST**

- [x] CSV parsed successfully (8,188 unique sites)
- [x] Site IDs extracted to KQL array format
- [x] Validation query generated with embedded site IDs
- [x] Query logic verified against known AR patterns
- [x] Documentation created (README + Summary)
- [x] Email template prepared
- [ ] **NEXT: Execute validation query in Fabric**
- [ ] Export missing sites CSV
- [ ] Send to AR team
- [ ] Track AR team progress
- [ ] Re-validate after AR updates
- [ ] Confirm 100% match
- [ ] Begin data extraction

---

**🎉 Script preparation complete! Ready to execute validation.** 🚀
