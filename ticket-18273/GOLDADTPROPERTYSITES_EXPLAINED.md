# goldAdtPropertySites - Table Information

## 🎯 **What is goldAdtPropertySites?**

`goldAdtPropertySites` is the **master site registry table** in Fabric. It contains all registered sites with their metadata, configuration, and registration information.

**Think of it as:** The "phonebook" of all sites in the VPP system.

---

## 📊 **Key Information It Contains:**

### **1. Site Identification**
- `siteId` - Unique Fabric internal ID (e.g., 400022503)
- `TwinId` - Azure Digital Twin ID (links to twin data)
- `externalReferenceId` - External reference (varies by source)

### **2. OEM Information**
- `oemname` - OEM provider (Tesla, Enphase, SolarEdge, Qcells)
- OEM-specific site ID (stored somewhere in properties)

### **3. Site Details**
- `siteName` - Name of the site
- `siteAddress` - Physical address
- `state` - State (TX, CA, etc.)
- `zipPostalCode` - ZIP code
- `timezone` - Time zone

### **4. Customer Information**
- `customerName` - Site owner name
- `customerEmail` - Contact email
- Customer phone, etc.

### **5. System Configuration**
- `system_size_kw` - Solar system size in kW
- `wMaxRtg` - Battery capacity in watts
- Inverter information
- Product details (inverter type, manufacturer, model)

### **6. Registration Info (JSON Object)**
- `assetRegistrationInfo` - Contains:
  - `accountNumber` - TPO account number (e.g., APPTPO-2505706267)
  - `purchaseDate` - When asset was purchased
  - `ptoDate` - Permission to Operate date
  - `displayName` - Display name for the asset
  - `assetDocuments` - Links to installation photos, permits, etc.
  - `assetAttributes` - Custom attributes

### **7. Program Registration**
- `isTPORegistered` - Enrolled in TPO program
- `isVppRegistered` - Enrolled in VPP program
- `isLeapRegistered` - Enrolled in LEAP program
- `program_name` - Array of program names

### **8. Installer Information**
- `installerName` - Company that installed the system
- Installer contact info

### **9. Timestamps**
- `createdAt` - When site was created in Fabric
- `updatedAt` - Last update timestamp

### **10. Status Information**
- `system_status_1h_online` - Online/offline status
- `last_data_timestamp` - Last telemetry timestamp
- Site active/inactive status

---

## 🔍 **What We Found for Your 3 Sites:**

From `goldadtproperties_query_data.csv`:

### **Site 1: Tesla Site**
```
siteId: 400022503
accountNumber: APPTPO-2410442068
purchaseDate: 2024-12-06
ptoDate: 2024-12-06
```

### **Site 2: Enphase Site**
```
siteId: 400042885
accountNumber: APPTPO-2505706267
purchaseDate: 2025-10-16
ptoDate: 2025-08-15
```

### **Site 3: Enphase Site**
```
siteId: 400048668
accountNumber: APPTPO-2503643621
purchaseDate: 2025-11-15
ptoDate: 2025-11-05
```

---

## 🎯 **Key Observations:**

### **What's MISSING from goldAdtPropertySites:**

❌ **No OEM site IDs visible!**

The ticket mentions:
- Enphase: 5939292
- Enphase: 5792277
- Tesla: b392405d-2efc-4042-80e3-068ba6210c36

**These OEM IDs are NOT in the `assetRegistrationInfo` JSON we saw!**

---

## 🔍 **WHERE ARE THE OEM SITE IDs?**

OEM site IDs might be stored in:

### **Option 1: Different property/column**
```kusto
database("eventhouse").goldAdtPropertySites
| where siteId in ("400022503", "400042885", "400048668")
| project siteId, oemname, externalReferenceId, TwinId
```

### **Option 2: Azure Digital Twin properties**
```kusto
database("eventhouse").goldAdtTwinEventsLatestV2
| where TwinId in ("400022503", "400042885", "400048668")
| project TwinId, propertyName, propertyValue
| where propertyName contains "oem" or propertyName contains "site"
```

### **Option 3: Separate mapping table**
```kusto
// Check if there's a mapping table
.show tables
| where TableName contains "mapping" or TableName contains "oem"
```

---

## 🎯 **CRITICAL QUESTION:**

**How do we map Fabric Site IDs to OEM Site IDs?**

| Fabric Site ID | Account Number | OEM | OEM Site ID (from ticket) |
|----------------|----------------|-----|---------------------------|
| 400022503 | APPTPO-2410442068 | Tesla | b392405d-2efc-4042-80e3-068ba6210c36 |
| 400042885 | APPTPO-2505706267 | Enphase | 5939292 |
| 400048668 | APPTPO-2503643621 | Enphase | 5792277 |

**We need to find where this mapping is stored!**

---

## 📋 **QUERIES TO RUN:**

### **Query 1: Check all columns for site 400022503**
```kusto
database("eventhouse").goldAdtPropertySites
| where siteId == "400022503"
| project *  // Get ALL columns
```

### **Query 2: Search for OEM IDs in twin properties**
```kusto
database("eventhouse").goldAdtTwinEventsLatestV2
| where TwinId == "400022503"
| project TwinId, propertyName, propertyValue
| where propertyValue contains "b392405d" 
    or propertyValue contains "2410442068"
    or propertyName contains "oem"
```

### **Query 3: Search for OEM site ID pattern**
```kusto
database("eventhouse").goldAdtTwinEventsLatestV2
| where TwinId in ("400022503", "400042885", "400048668")
| project TwinId, propertyName, propertyValue
| where propertyName in ("oemSiteId", "oem_site_id", "externalSiteId", "siteid")
```

---

## 🎯 **WHY THIS MATTERS:**

**If we can find the OEM site IDs stored in Fabric:**
1. We can verify they match what the ticket says (5939292, b392405d...)
2. We can check if telemetry is coming in with those OEM IDs
3. We can understand the correct ID mapping for the report

**If OEM site IDs are NOT stored in Fabric:**
- That's a problem! We need OEM IDs to query OEM APIs
- Sites might have been onboarded without proper OEM configuration
- This explains why no telemetry is being synced

---

## ✅ **NEXT STEP:**

**Run Query 1 to see ALL columns for one site:**

```kusto
database("eventhouse").goldAdtPropertySites
| where siteId == "400022503"
| project *
```

This will show us if OEM site ID is stored somewhere we haven't checked yet!

---

**Want to run this query and see what we find?** 🔍😊
