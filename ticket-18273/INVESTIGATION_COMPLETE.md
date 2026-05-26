# Ticket 18273 - Investigation Complete (Data Engineering)

**Ticket:** https://dev.azure.com/qcellsces/Helios/_workitems/edit/18273  
**Investigator:** Jagan Murikinati  
**Date Completed:** May 19, 2026  
**Status:** Investigation Complete - Waiting on External Teams

---

## ✅ INVESTIGATION SUMMARY

**Issue:** 3 TX VPP sites show offline in Fabric, but online in OEM portal

**Result:** NO telemetry data exists in Fabric for these sites

---

## 🔍 ROOT CAUSES IDENTIFIED

### **Enphase Site 5939292 (APPTPO-2505706267)**

**Problem:** Enrolled in wrong Enphase Grid Services program

**Details:**
- Currently enrolled in: **"Gexa Battery Benefits Plan"** (program ID: 625e4aabf88e9b580c7926b0)
- Should be enrolled in: **"ERS_ERCOT_TX"**
- Error when attempting to enroll: "Site is already enrolled in program Gexa Battery Benefits Plan"

**Impact:** Telemetry flows to "Gexa" program, not accessible to Fabric "ERS_ERCOT_TX" connector

**Fix Required:** Enphase must move site from "Gexa" to "ERS_ERCOT_TX"

**Owner:** Shuai Zhang (coordinate with Enphase)

---

### **Enphase Site 5792277 (APPTPO-2503643621)**

**Problem:** Not authorized to enroll in program

**Details:**
- Error when attempting to enroll: **"403 Forbidden - Not authorized to enroll this site"**
- Cannot access site in Enphase Grid Services

**Impact:** No telemetry accessible to Fabric

**Fix Required:** Enphase must grant authorization for this site

**Owner:** Shuai Zhang (coordinate with Enphase)

---

### **Tesla Site 400022503 (APPTPO-2410442068)**

**Problem:** Wrong OEM Site ID in Asset Registry

**Details:**
- AR has: **b392405d-2efc-4042-80e3-068ba6210c36** ❌
- Should be: **c3f04cd8-b506-49be-a122-7bc97b14ae20** ✅
- Duplicate registration issue causing connector to skip this site

**Impact:** Telemetry exists but not linked to correct Fabric site ID

**Fix Required:** AR team must update OEM Site ID

**Owner:** Shuai Zhang (coordinate with AR team)

---

## 📊 VERIFICATION QUERIES

### **After Fixes Applied - Run This to Verify:**

```kusto
// Check if telemetry is now flowing
database("eventhouse").silverCommDataSite
| where siteId in ("400022503", "400042885", "400048668")  // Fabric site IDs
    or siteId in ("5939292", "5792277", "c3f04cd8-b506-49be-a122-7bc97b14ae20")  // OEM site IDs
| summarize 
    latest = max(sourceTimestamp),
    count = count()
    by siteId, oem
| extend status = iff(latest > ago(1h), "✅ ONLINE", "❌ OFFLINE")
| order by latest desc
```

**Expected Result After Fixes:**
- All 3 sites should show **"✅ ONLINE"** with recent timestamps
- Asset Onboarding Report will automatically show them as online

---

## 📋 HANDOFF CHECKLIST

### **For Shuai Zhang:**

**Enphase Sites:**
- [ ] Contact Enphase support to move site 5939292 from "Gexa" to "ERS_ERCOT_TX"
- [ ] Contact Enphase support to authorize site 5792277 for enrollment
- [ ] Retry onboarding once Enphase confirms fixes

**Tesla Site:**
- [ ] Submit AR correction request for site 400022503
- [ ] Update OEM Site ID to: c3f04cd8-b506-49be-a122-7bc97b14ae20

**Verification:**
- [ ] Run verification query after fixes
- [ ] Confirm Asset Onboarding Report shows sites as online
- [ ] Close ticket

---

## 🎯 TIMELINE

| Date | Event |
|------|-------|
| May 18, 2026 | Ticket created by Shuai Zhang |
| May 18, 2026 | Jagan investigated - No telemetry found |
| May 18, 2026 | Discussion with Robin - Root causes identified |
| May 19, 2026 | Sachin attempted onboarding - Errors confirmed |
| May 19, 2026 | **Investigation complete - Handed off to Shuai** |

---

## 📧 KEY CONTACTS

- **Shuai Zhang** - Owner, coordinate external fixes
- **Robin (Myungkyoon)** - OEM Connector team
- **Naveen Swamy** - Data Engineering manager
- **Sachin Ingale** - Onboarding attempts

---

## 📁 RELATED FILES

- `FINDINGS.md` - Detailed findings from investigation
- `DIAGNOSTIC_QUERIES.kql` - Queries used to investigate
- `INITIAL_ANALYSIS.md` - Initial hypothesis and analysis
- `README.md` - Quick reference guide

---

**Investigation Status:** ✅ **COMPLETE**  
**Data Engineering Actions:** ✅ **NONE REMAINING**  
**Next Steps:** ⏳ **Waiting on Enphase + AR Team**

---

**Prepared by:** Jagan Murikinati  
**Date:** May 19, 2026
