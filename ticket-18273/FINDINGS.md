# Ticket 18273 - Investigation Findings

## ✅ **SITES ARE REGISTERED IN FABRIC!**

All 3 sites exist in `goldAdtPropertySites`:

| APP ID (Ticket) | Fabric Site ID | Account Number | Status |
|-----------------|----------------|----------------|--------|
| APPTPO-2410442068 | **400022503** | APPTPO-2410442068 | ✅ Registered |
| APPTPO-2505706267 | **400042885** | APPTPO-2505706267 | ✅ Registered |
| APPTPO-2503643621 | **400048668** | APPTPO-2503643621 | ✅ Registered |

---

## 📊 **KEY FINDINGS:**

### **Finding 1: Sites Use Internal Fabric IDs**

**Ticket says:** APPTPO-2410442068  
**Fabric uses:** siteId = **400022503**

**This is the ID mismatch!** ⚠️

---

### **Finding 2: Sites Have Purchase/PTO Dates**

| Site ID | Purchase Date | PTO Date |
|---------|--------------|----------|
| 400022503 (Tesla) | 2024-12-06 | 2024-12-06 |
| 400042885 (Enphase) | 2025-10-16 | 2025-08-15 |
| 400048668 (Enphase) | 2025-11-15 | 2025-11-05 |

**All sites are OLD** (6+ months) → Not a recent onboarding issue

---

## 🔍 **NEXT CRITICAL QUERY:**

### **Check telemetry with FABRIC SITE IDs (not APP IDs):**

```kusto
database("eventhouse").silverCommDataSite
| where siteId in ("400022503", "400042885", "400048668")
| summarize 
    earliest = min(sourceTimestamp),
    latest = max(sourceTimestamp),
    record_count = count()
    by siteId, oem
| extend 
    days_since_last = datetime_diff('day', now(), latest),
    status = iff(latest > ago(1h), "online", "offline")
| order by latest desc
```

---

## 🎯 **UPDATED HYPOTHESIS:**

### **Most Likely: Telemetry Uses Fabric Site IDs** (95%)

**Theory:**
- Fabric registered sites with internal IDs: 400022503, 400042885, 400048668
- Telemetry is stored using these Fabric IDs (not APP IDs)
- Asset Onboarding Report is looking for APP IDs (APPTPO-xxx) ❌
- **Result:** Report can't find the data!

**This explains:**
- ✅ Why OEM portal shows online (data exists)
- ✅ Why Fabric report shows offline (looking for wrong ID)
- ✅ Why we found no telemetry with APP IDs

---

## 🔍 **ADDITIONAL QUERIES TO RUN:**

### **Query 1: Check telemetry with Fabric Site IDs**
```kusto
database("eventhouse").silverCommDataSite
| where siteId in ("400022503", "400042885", "400048668")
| summarize latest = max(sourceTimestamp), count = count() by siteId, oem
```

### **Query 2: Check OEM site IDs in site details**
```kusto
database("eventhouse").goldAdtPropertySites
| where siteId in ("400022503", "400042885", "400048668")
| project 
    fabric_siteId = siteId,
    account_number = assetRegistrationInfo.accountNumber,
    oemname,
    externalReferenceId,
    // Look for OEM-specific IDs
    twinId = TwinId,
    createdAt
```

### **Query 3: Search for OEM site IDs in site properties**
```kusto
database("eventhouse").goldAdtTwinEventsLatestV2
| where TwinId in ("400022503", "400042885", "400048668")
| project TwinId, propertyName, propertyValue
| where propertyName contains "oem" or propertyName contains "site" or propertyName contains "id"
```

---

## 🎯 **ROOT CAUSE SUMMARY:**

### **Problem:** ID Mismatch in Asset Onboarding Report

**What's Happening:**
1. Sites registered in Fabric with IDs: 400022503, 400042885, 400048668 ✅
2. Telemetry stored with these Fabric IDs (hypothesis - need to verify) ❓
3. Asset Onboarding Report queries using APP IDs (APPTPO-xxx) ❌
4. Report finds no data → Shows "offline" ❌

**Solution Options:**

### **Option A: Fix Report Query** (Recommended)
Update Asset Onboarding Report to use Fabric site IDs instead of APP IDs

### **Option B: Add ID Mapping**
Ensure report has mapping: APPTPO-xxx → 400022503

### **Option C: Update Telemetry Storage**
Store telemetry with both IDs (less likely to change)

---

## 📋 **IMMEDIATE NEXT STEP:**

**RUN THIS QUERY TO CONFIRM:**

```kusto
database("eventhouse").silverCommDataSite
| where siteId in ("400022503", "400042885", "400048668")
| summarize latest = max(sourceTimestamp), count = count() by siteId, oem
```

**Expected Result:**
- ✅ **If data is found:** Root cause confirmed! Report is using wrong IDs
- ❌ **If no data found:** Telemetry truly missing, need to investigate further

---

## 🎯 **STATUS:**

- ✅ Sites exist in Fabric
- ✅ Sites have Fabric IDs: 400022503, 400042885, 400048668
- ⏳ **NEED TO VERIFY:** Does telemetry exist with these Fabric IDs?
- ⏳ **NEED TO CHECK:** What ID does Asset Onboarding Report use?

**Run the query above and share results!** 🚀
