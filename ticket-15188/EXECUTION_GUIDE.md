# Ticket 15188: sqTelemetry Table Creation - Execution Guide

**Author:** Jagan Murikinati  
**Date:** 2026-04-20  
**Ticket:** #15188  

---

## 📋 Task Summary

1. Create `sqTelemetry` table in **eventhouseVPP** database
2. Table has **56 columns** (4 base + 26 metrics + 26 data labels)
3. Copy 1 day's data (April 1, 2026) from `silverCommDataSite` to `sqTelemetry`

---

## 🎯 Step-by-Step Execution

### **Step 1: Open Fabric Workspace**

1. Go to your Fabric workspace
2. Navigate to **eventhouseVPP** (NOT eventhouse)
3. Click **"+ New"** → **"KQL Queryset"**
4. Name it: `sqTelemetry_Setup`
5. Connect it to **eventhouseVPP** database

---

### **Step 2: Verify Database Connection**

Run this to confirm you're in the right database:

```kql
.show database
```

Expected output: Database name should be from **eventhouseVPP**

---

### **Step 3: Create sqTelemetry Table**

**File:** `create_sqTelemetry_table.kql`

1. Open the file `create_sqTelemetry_table.kql`
2. Copy the `.create table sqTelemetry (...)` command
3. Paste into KQL Queryset
4. Click **Run** ▶️

**Expected Output:**
```
Command completed successfully
```

---

### **Step 4: Verify Table Created**

Run these verification queries:

```kql
// Check table exists
.show tables | where TableName == "sqTelemetry"

// Check schema
sqTelemetry
| getschema

// Count columns (should be 56)
sqTelemetry
| getschema
| count
```

**Expected:**
- Table `sqTelemetry` exists ✅
- Column count = **56** ✅

---

### **Step 5: Prepare Cross-Database Query**

Before running the insert, you need to know:

**Question to ask:** What is the exact database name in eventhouse where `silverCommDataSite` is located?

Check by running this in **eventhouse** (not eventhouseVPP):
```kql
.show database
```

Update the insert script with the correct cluster/database name.

---

### **Step 6: Insert Sample Data (April 1, 2026)**

**IMPORTANT:** There are two ways to do this:

#### **Option A: If eventhouse and eventhouseVPP are in the same cluster**

```kql
.set sqTelemetry <|
database('eventhouse_db_name').silverCommDataSite
| where sourceTimestamp >= datetime(2026-04-01 00:00:00)
| where sourceTimestamp < datetime(2026-04-02 00:00:00)
| project 
    siteId, assetId, oem, sourceTimestamp,
    battery_200_DailyWhExp = todouble(battery_200_DailyWhExp),
    battery_200_DailyWhExp_dl = "VALID",
    // ... (see insert_sample_data.kql for full script)
```

#### **Option B: If they are in different clusters**

```kql
.set sqTelemetry <|
cluster('eventhouse_cluster_url').database('eventhouse_db_name').silverCommDataSite
| where sourceTimestamp >= datetime(2026-04-01 00:00:00)
| where sourceTimestamp < datetime(2026-04-02 00:00:00)
| project ...
```

**Use the file:** `insert_sample_data.kql` (update the cluster/database name first)

---

### **Step 7: Verify Data Inserted**

Run these queries:

```kql
// Check row count
sqTelemetry
| count

// Check date range
sqTelemetry
| summarize 
    MinTimestamp = min(sourceTimestamp),
    MaxTimestamp = max(sourceTimestamp),
    RowCount = count(),
    UniqueSites = dcount(siteId),
    UniqueOEMs = dcount(oem)

// View sample records
sqTelemetry
| take 10

// Check data labels are populated
sqTelemetry
| summarize by battery_200_DailyWhExp_dl, grid_200_IncWhExp_dl
```

**Expected:**
- Row count > 0 ✅
- Date range: April 1, 2026 (00:00 to 23:59) ✅
- All `_dl` fields = "VALID" ✅

---

## 📊 Table Structure Summary

### **Total Columns: 56**

| Category | Count | Example |
|----------|-------|---------|
| Base Fields | 4 | siteId, assetId, oem, sourceTimestamp |
| Battery Metrics | 9 × 2 = 18 | battery_200_DailyWhExp, battery_200_DailyWhExp_dl |
| Grid Metrics | 7 × 2 = 14 | grid_200_IncWhExp, grid_200_IncWhExp_dl |
| Load Metrics | 5 × 2 = 10 | load_200_W, load_200_W_dl |
| PV Metrics | 6 × 2 = 12 | pv_200_TotWhExp, pv_200_TotWhExp_dl |

---

## ⚠️ Important Notes

1. **Database Location:**
   - Source: `silverCommDataSite` in **eventhouse**
   - Target: `sqTelemetry` in **eventhouseVPP**
   - You're creating in a DIFFERENT database!

2. **Data Labels:**
   - All `_dl` fields default to "VALID" for sample data
   - In production, these would be calculated based on data quality rules

3. **Date:**
   - Sample data is April 1, 2026
   - Adjust if needed: `datetime(2026-04-01 00:00:00)`

4. **Cross-Database Query:**
   - You may need permissions to query across databases
   - If you get permission errors, ask Naveen for access

---

## ✅ Success Criteria

- [x] Table `sqTelemetry` created in **eventhouseVPP**
- [x] Table has exactly **56 columns**
- [x] Schema matches ticket requirements
- [x] April 1, 2026 data copied successfully
- [x] All `_dl` fields populated with "VALID"
- [x] Row count > 0

---

## 🚨 Troubleshooting

### **Error: "Table already exists"**
```kql
.drop table sqTelemetry
```
Then re-run create script.

### **Error: "Cross-database query not allowed"**
Ask Naveen for permissions, or export/import data manually.

### **Error: "Column not found in silverCommDataSite"**
Some fields might not exist. Check:
```kql
database('eventhouse_db').silverCommDataSite
| getschema
| where ColumnName startswith "battery_" or ColumnName startswith "grid_"
```

---

## 📝 Update Ticket

Once complete, add this comment to ADO ticket:

```
✅ Task Completed

Created sqTelemetry table in eventhouseVPP database with 56 columns:
- 4 base fields (siteId, assetId, oem, sourceTimestamp)
- 26 telemetry metrics
- 26 data label fields (_dl suffix)

Sample data from April 1, 2026 copied successfully.
Table verified and ready for use.
```

---

**Good luck!** 🚀
