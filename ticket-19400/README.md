# Ticket 19400 - DSGS Site List Validation Against Asset Registry

**Task:** Validate that all 8,188 enrolled DSGS sites (May 2026) have Leap Contracts in Asset Registry

**Date:** 2026-05-29  
**Author:** Jagan Murikinati

---

## 📋 **BACKGROUND**

From Shuai Zhang's comment:
> "To prepare for extracting the April and May interval data required for the 8,188 DSGS sites enrolled in May, could you please start by validating the site list generated from your scripts (sites with "Leap Contracts" in AR) against the actual enrolled DSGS site list attached to this ticket?"

**Key Requirements:**
1. Compare enrolled site list (CSV) against Asset Registry Leap Contracts
2. Identify sites MISSING Leap Contracts in AR
3. Report missing sites to AR team (@Ashok Bhaskar @Chanhyup.Kim)
4. After AR updates, re-validate before extracting April & May 2026 data

---

## 📁 **FILES IN THIS FOLDER**

### **Input Files:**
1. **`leap_meters_export_05282026.csv`** - Enrolled DSGS sites from Shuai
   - 8,189 rows (including header)
   - 8,188 unique enrolled sites
   - Column: `Asset Registry Site ID (partner_reference)`
   - Sites: 7,990 in 400-series, 196 in 100-series, 2 other series

### **Generated Files:**
2. **`parse_enrolled_sites.py`** - Extracts site IDs from CSV
   - Outputs: `enrolled_sites_kql_array.txt` (KQL dynamic array format)
   - Outputs: Summary statistics

3. **`enrolled_sites_kql_array.txt`** - KQL dynamic array of site IDs
   - Ready to copy-paste into KQL queries
   - Format: 10 site IDs per line

4. **`generate_validation_query.py`** - Generates complete KQL query
   - Embeds all 8,188 site IDs directly in the query
   - Outputs: `DSGS_LeapContract_Validation_READY.kql`

5. **`DSGS_LeapContract_Validation_READY.kql`** ⭐ **PRIMARY QUERY**
   - Complete validation query (1,741 lines)
   - Contains all 8,188 enrolled site IDs
   - Ready to execute in Fabric/Eventhouse
   - NO DATE FILTER (checks current AR state)

6. **`DSGS_LeapContract_Validation.kql`** - Template query
   - Manual template (requires pasting site IDs)
   - Use `DSGS_LeapContract_Validation_READY.kql` instead

### **Documentation:**
7. **`README.md`** (this file) - Complete guide

---

## 🚀 **QUICK START - RUN VALIDATION**

### **Option 1: Run Ready-Made Query (Recommended)**

1. Open **`DSGS_LeapContract_Validation_READY.kql`** in Fabric/Eventhouse
2. Execute the entire query
3. Review output:
   - Summary statistics (total, matched, missing)
   - Full validation results (all sites with status)
   - List of sites missing Leap Contracts

4. Export **"SITES MISSING LEAP CONTRACTS"** table to CSV
5. Share with AR team (@Ashok Bhaskar @Chanhyup.Kim)

### **Option 2: Regenerate Query (if CSV updated)**

```powershell
# Navigate to ticket folder
cd ticket-19400

# Regenerate the query
python generate_validation_query.py

# Output: DSGS_LeapContract_Validation_READY.kql (refreshed)
```

---

## 📊 **WHAT THE VALIDATION QUERY DOES**

### **Step 1: Load Enrolled Site List**
- Loads 8,188 site IDs from embedded datatable
- Source: `leap_meters_export_05282026.csv`

### **Step 2: Fetch Sites with Leap Contracts from AR**
```kql
goldAdtPropertyMinMaxLatestViewV2
| where Key == 'meterId' 
  and ModelId startswith 'dtmi:qcells:contract:leapContract'
  and tolower(actionMax) != 'delete'
| join kind=inner (goldAdtAllRelationshipsLatestView ...) 
| distinct siteId, meterId
```

### **Step 3: Compare & Identify Missing Sites**
- LEFT OUTER JOIN: Enrolled sites vs AR sites
- Flag each site: "Has Leap Contract" or "Missing Leap Contract"

### **Step 4: Generate Report**
- **Summary:** Total, matched, missing (with percentages)
- **Full Results:** All 8,188 sites with status
- **Action List:** Sites missing Leap Contracts (for AR team)

---

## 📈 **EXPECTED OUTPUTS**

### **Summary Statistics**
```
VALIDATION SUMMARY
------------------------------------------
Total Enrolled DSGS Sites:        8,188
Sites WITH Leap Contract:         ???  (??%)
Sites MISSING Leap Contract:      ???  (??%)
```

### **Sites Missing Leap Contracts**
```
siteId
-----------
100003023
400001234
400005678
...
```

---

## 🔄 **WORKFLOW**

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Run DSGS_LeapContract_Validation_READY.kql             │
│    ↓                                                        │
│ 2. Export "SITES MISSING LEAP CONTRACTS" to CSV            │
│    ↓                                                        │
│ 3. Share CSV with AR Team (@Ashok @Chanhyup)              │
│    ↓                                                        │
│ 4. AR Team adds Leap Contracts for missing sites           │
│    ↓                                                        │
│ 5. Re-run validation query (confirm all sites matched)     │
│    ↓                                                        │
│ 6. Proceed with April & May 2026 data extraction           │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚠️ **IMPORTANT NOTES**

### **No Date Filter**
- This query checks **current state** of Asset Registry
- Leap Contract = enrollment record (not time-series data)
- A site either has a Leap Contract twin or doesn't

### **ModelId Filter**
- Uses `startswith 'dtmi:qcells:contract:leapContract'`
- Handles version suffixes (`;1`, `;2`, etc.) automatically
- Based on verification: `dtmi:qcells:contract:leapContract;1` exists

### **Future Data Extraction**
- Once validation complete → Extract telemetry data
- Date range: April 1-30, 2026 + May 1-31, 2026
- For all 8,188 validated sites
- 15-minute interval battery data

---

## 📞 **CONTACTS**

**For validation results & missing sites:**
- @Ashok Bhaskar (Asset Registry Team)
- @Chanhyup.Kim (Asset Registry Team)

**For questions:**
- Shuai Zhang (requested validation)
- Juan Culebro, Kai Xu, Sanjeev Lakkaraju (cc'd)

---

## ✅ **CHECKLIST**

- [x] Parse CSV and extract 8,188 site IDs
- [x] Generate KQL dynamic array
- [x] Create validation query
- [x] Embed all site IDs in query
- [x] Document validation process
- [ ] **Run validation query in Fabric**
- [ ] Export missing sites to CSV
- [ ] Share with AR team
- [ ] Re-validate after AR updates
- [ ] Proceed with data extraction

---

**Ready to execute!** 🚀
