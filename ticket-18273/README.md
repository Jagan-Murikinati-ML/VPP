# Ticket 18273 - Missing Telemetry Investigation

## 🎯 Quick Summary

**Problem:** 3 TX VPP sites show offline in Fabric but online in OEM portal

**Sites:**
1. APPTPO-2505706267 (Enphase: 5939292) - Never online
2. APPTPO-2503643621 (Enphase: 5792277) - Never online
3. APPTPO-2410442068 (Tesla: b392405d...) - Last online 4/29/26

---

## 📋 Files in This Ticket

- `ticket.md` - Original ticket description
- `INITIAL_ANALYSIS.md` - Detailed root cause hypotheses
- `DIAGNOSTIC_QUERIES.kql` - Ready-to-run Kusto queries
- `README.md` - This file

---

## 🚀 Quick Start - Run These Queries

### **Step 1: Check Site Registration**
```kusto
// Are sites in Fabric?
goldAdtPropertySites
| where siteId in ("APPTPO-2505706267", "APPTPO-2503643621", "APPTPO-2410442068")
    or accountNumber in ("2505706267", "2503643621", "2410442068")
| project siteId, accountNumber, oemname, siteName
```

### **Step 2: Check Telemetry (APP ID)**
```kusto
// Any telemetry with APP IDs?
silverCommDataSite
| where siteId in ("APPTPO-2505706267", "APPTPO-2503643621", "APPTPO-2410442068")
| summarize latest = max(sourceTimestamp), count = count() by siteId, oem
```

### **Step 3: Check Telemetry (OEM ID)**
```kusto
// Any telemetry with OEM IDs?
silverCommDataSite
| where siteId in ("5939292", "5792277", "b392405d-2efc-4042-80e3-068ba6210c36")
| summarize latest = max(sourceTimestamp), count = count() by siteId, oem
```

---

## 🔍 Most Likely Root Causes

### **#1: Site ID Mismatch** (80% probability)
- Telemetry coming in with OEM ID (5939292, 5792277, b392405d...)
- Report looking for APP ID (APPTPO-2505706267, ...)
- **Fix:** Update site mapping or report query

### **#2: Telemetry Not Ingested** (15% probability)
- Sites exist but no data in Fabric
- OEM API integration issue
- **Fix:** Investigate OEM data pipeline

### **#3: Report Query Bug** (5% probability)
- Data exists but report has wrong filter
- **Fix:** Update report query

---

## 📧 Questions to Ask

### **For Naveen/Sanjeev:**
1. What table does Asset Onboarding Report use?
2. How is "online/offline" determined?
3. Should sites use APP ID or OEM ID?

### **For Shuai/Kai:**
1. Confirm sites are online in OEM portal?
2. Latest timestamp in OEM portal for each site?
3. When were sites onboarded?

---

## ✅ Investigation Checklist

- [ ] Run diagnostic queries (DIAGNOSTIC_QUERIES.kql)
- [ ] Identify which ID format has telemetry (APP vs OEM)
- [ ] Check if site ID mapping exists
- [ ] Review Asset Onboarding Report query
- [ ] Determine root cause
- [ ] Implement fix
- [ ] Verify with team

---

## 🎯 Next Steps

1. Run queries in `DIAGNOSTIC_QUERIES.kql`
2. Document findings
3. Identify root cause
4. Propose solution
5. Get approval
6. Implement fix
7. Verify and close ticket

**Estimated Resolution Time:** 1-2 hours
