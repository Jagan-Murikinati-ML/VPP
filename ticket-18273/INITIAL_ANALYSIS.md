# Ticket 18273 - Initial Analysis

## 📋 **Ticket Summary**

**Type:** Issue/Bug  
**Priority:** TBD  
**Risk:** TBD  
**Title:** Fabric Missing Telemetry Data Issue

---

## 🎯 **Problem Statement**

**Issue:** 3 TX VPP sites show as offline in Fabric Asset Onboarding Report, but OEM portal shows they're online with telemetry data.

**Impact:** Data discrepancy between OEM and Fabric - potentially missing telemetry ingestion

**Stakeholders:** @Sanjeev Lakkaraju @Naveen Siddalingaswamy @Myungkyoon.Kim @Shuai.Zhang @Kai Xu @Jasper Liu

---

## 📊 **AFFECTED SITES**

| TPO APP ID | Fabric Status | OEM Portal Status | OEM Site ID |
|------------|---------------|-------------------|-------------|
| APPTPO-2505706267 | **Never online** | Online with data | Enphase: 5939292 |
| APPTPO-2503643621 | **Never online** | Online with data | Enphase: 5792277 |
| APPTPO-2410442068 | **Last online: 4/29/26 8:55 PM** | Online with data | Tesla: b392405d-2efc-4042-80e3-068ba6210c36 |

**Pattern:**
- 2 Enphase sites - **Never** showed online in Fabric
- 1 Tesla site - Stopped updating on **April 29, 2026** (19 days ago - current date: May 18, 2026)
- All 3 are TX VPP sites

---

## 🔍 **ROOT CAUSE INVESTIGATION STEPS**

### **Step 1: Check if Sites Exist in Fabric**

**Query to run:**
```kusto
// Check if sites exist in any Fabric tables
goldAdtPropertySites
| where siteId in ("APPTPO-2505706267", "APPTPO-2503643621", "APPTPO-2410442068")
    or accountNumber in ("2505706267", "2503643621", "2410442068")
| project siteId, accountNumber, oemname, siteName, createdAt, updatedAt
```

**Expected outcomes:**
- ✅ Sites exist → Investigate why telemetry is missing
- ❌ Sites don't exist → Sites not onboarded to Fabric

---

### **Step 2: Check Telemetry Tables**

**Query to run:**
```kusto
// Check silverCommDataSite for telemetry
silverCommDataSite
| where siteId in ("APPTPO-2505706267", "APPTPO-2503643621", "APPTPO-2410442068")
    or siteId in ("5939292", "5792277", "b392405d-2efc-4042-80e3-068ba6210c36")
| summarize 
    earliest_telemetry = min(sourceTimestamp),
    latest_telemetry = max(sourceTimestamp),
    record_count = count()
    by siteId, oem
| order by latest_telemetry desc
```

**For Enphase sites specifically:**
```kusto
// Check Enphase sites by OEM site ID
silverCommDataSite
| where siteId in ("5939292", "5792277") and oem == "enphase"
| summarize 
    earliest = min(sourceTimestamp),
    latest = max(sourceTimestamp),
    count = count()
    by siteId
```

**For Tesla site:**
```kusto
// Check Tesla site
silverCommDataSite
| where siteId == "b392405d-2efc-4042-80e3-068ba6210c36" and oem == "tesla"
| summarize 
    earliest = min(sourceTimestamp),
    latest = max(sourceTimestamp),
    count = count()
    by siteId
```

---

### **Step 3: Check Site Mapping**

**Possible issues:**
1. Site registered with different ID (APP ID vs OEM ID mismatch)
2. Site onboarded but OEM ID not mapped correctly
3. Telemetry coming in with wrong site ID

**Query to run:**
```kusto
// Check all possible ID variations
goldAdtPropertySites
| where accountNumber contains "2505706267"
    or accountNumber contains "2503643621"
    or accountNumber contains "2410442068"
    or siteId contains "5939292"
    or siteId contains "5792277"
    or siteId contains "b392405d"
| project siteId, accountNumber, oemname, externalReferenceId, createdAt
```

---

### **Step 4: Check Asset Onboarding Report Query**

**Need to understand:**
- What is the report's data source?
- How does it determine "online" vs "offline"?
- What field does it use for "latest online timestamp"?

**Likely logic:**
```kusto
// Probable report logic (need to verify)
goldAdtPropertySites
| join kind=leftouter (
    silverCommDataSite
    | summarize latest_timestamp = max(sourceTimestamp) by siteId
) on siteId
| extend status = iff(latest_timestamp > ago(1h), "online", "offline")
```

---

## 🎯 **POTENTIAL ROOT CAUSES**

### **Hypothesis 1: Site ID Mismatch** ⚠️ **Most Likely**

**Symptoms:**
- Sites exist in Fabric but with different IDs
- Telemetry coming in with OEM site ID (5939292, 5792277, b392405d...)
- Report looking for APP ID (APPTPO-2505706267, ...)
- No mapping between the two

**Fix:** Update site mapping or report query to use correct ID

---

### **Hypothesis 2: Telemetry Not Ingested**

**Symptoms:**
- Sites exist in Fabric
- No telemetry data in silverCommDataSite
- OEM portal shows data, but not reaching Fabric

**Possible causes:**
- OEM API integration issue
- Site not added to telemetry sync list
- Authentication/credentials issue

**Fix:** Investigate OEM data ingestion pipeline

---

### **Hypothesis 3: Recent Onboarding - Telemetry Lag**

**Symptoms:**
- Enphase sites: "Never online" → Might be newly onboarded
- Tesla site: Stopped 4/29 → Possible configuration change

**Check:**
- When were these sites onboarded to Fabric?
- Any recent changes to site configuration?

---

### **Hypothesis 4: Report Query Bug**

**Symptoms:**
- Data exists but report query has wrong filter/join

**Check:**
- Review Asset Onboarding Report query
- Verify join conditions and filters

---

## 📋 **INVESTIGATION CHECKLIST**

### **Phase 1: Data Verification** (15 min)

- [ ] Check if sites exist in `goldAdtPropertySites`
- [ ] Note down actual site IDs used in Fabric
- [ ] Check if telemetry exists in `silverCommDataSite`
- [ ] Check both APP ID and OEM ID variations

### **Phase 2: Root Cause Analysis** (30 min)

- [ ] Verify site ID mapping (APP ID ↔ OEM ID)
- [ ] Check telemetry data volume and timestamps
- [ ] Compare with working TX VPP sites
- [ ] Review Asset Onboarding Report query

### **Phase 3: OEM Verification** (if needed)

- [ ] Check Enphase API logs for sites 5939292, 5792277
- [ ] Check Tesla API logs for site b392405d-2efc-4042-80e3-068ba6210c36
- [ ] Verify sites are in OEM sync configuration

---

## 🎯 **IMMEDIATE ACTIONS**

### **Action 1: Run Diagnostic Queries**

Create a comprehensive diagnostic query to check all aspects:

```kusto
// Site existence and mapping
let target_app_ids = dynamic(["APPTPO-2505706267", "APPTPO-2503643621", "APPTPO-2410442068"]);
let target_oem_ids = dynamic(["5939292", "5792277", "b392405d-2efc-4042-80e3-068ba6210c36"]);

// Check site registration
let site_check = 
    goldAdtPropertySites
    | where siteId in (target_app_ids) or siteId in (target_oem_ids)
        or accountNumber in ("2505706267", "2503643621", "2410442068")
    | project siteId, accountNumber, oemname, siteName, status = "Site Exists"
;

// Check telemetry with APP IDs
let telemetry_app = 
    silverCommDataSite
    | where siteId in (target_app_ids)
    | summarize latest = max(sourceTimestamp), count = count() by siteId, oem
    | project siteId, oem, latest, count, id_type = "APP_ID"
;

// Check telemetry with OEM IDs
let telemetry_oem = 
    silverCommDataSite
    | where siteId in (target_oem_ids)
    | summarize latest = max(sourceTimestamp), count = count() by siteId, oem
    | project siteId, oem, latest, count, id_type = "OEM_ID"
;

// Combine results
site_check
| join kind=fullouter telemetry_app on siteId
| join kind=fullouter telemetry_oem on siteId
```

---

## 📧 **QUESTIONS FOR TEAM**

### **For Naveen/Sanjeev:**

1. **Asset Onboarding Report:**
   - What is the data source (table/function)?
   - How is "online/offline" status determined?
   - What field is used for "latest online timestamp"?

2. **Site ID Mapping:**
   - Should sites use APP ID (APPTPO-xxx) or OEM ID (5939292, b392405d...)?
   - Is there a mapping table between APP ID and OEM ID?

3. **Known Issues:**
   - Any known issues with TX VPP sites?
   - Recent changes to telemetry ingestion?

### **For Shuai/Kai:**

1. **OEM Portal Verification:**
   - Can you confirm these sites show online in OEM portals?
   - What's the latest telemetry timestamp in OEM portal for each site?

2. **Site Details:**
   - When were these sites onboarded?
   - Any recent configuration changes?

---

## 🎯 **NEXT STEPS**

1. ✅ Document initial analysis
2. ⏳ Run diagnostic queries in Fabric
3. ⏳ Identify which hypothesis is correct
4. ⏳ Implement fix based on root cause
5. ⏳ Verify fix with stakeholders
6. ⏳ Document solution for future reference

---

**Estimated Time to Resolve:** 1-2 hours (if data access is available)
