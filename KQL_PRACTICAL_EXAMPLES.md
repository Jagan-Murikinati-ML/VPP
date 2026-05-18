# KQL Practical Examples - From Your Real Work

**Examples from:** VPP Project (sqTelemetry, silverCommDataSite, etc.)

---

## 📋 **Table of Contents**

1. [Data Copy Operations](#data-copy-operations)
2. [Data Deletion](#data-deletion)
3. [Date Filtering](#date-filtering)
4. [Aggregations](#aggregations)
5. [Cross-Database Queries](#cross-database-queries)
6. [Data Validation](#data-validation)

---

## 1️⃣ **Data Copy Operations**

### **Copy Yesterday's Data (Your Nightly Job):**

```kql
.set-or-append sqTelemetry <|
database("eventHouse").silverCommDataSite
| where sourceTimestamp >= startofday(ago(1d))
  and sourceTimestamp < startofday(now())
| project 
    siteId, assetId, oem, sourceTimestamp,
    battery_200_DailyWhExp, battery_200_DailyWhExp_dl = "",
    battery_200_DailyWhImp, battery_200_DailyWhImp_dl = "",
    // ... more fields
```

**What it does:**
- Runs daily at 2 AM UTC
- Copies previous full day (00:00 to 23:59 UTC)
- Adds empty data label fields

---

### **Copy Last 14 Days (Bi-weekly Update):**

```kql
.set-or-append sqTelemetry <|
database("eventHouse").silverCommDataSite
| where sourceTimestamp >= startofday(ago(14d))
  and sourceTimestamp < startofday(now())
| project siteId, assetId, oem, sourceTimestamp, ...
```

**What it does:**
- Runs 1st and 15th of month
- Re-copies last 14 days to catch OEM corrections

---

### **Copy Specific Date Range:**

```kql
.set-or-append sqTelemetry <|
database("eventHouse").silverCommDataSite
| where sourceTimestamp >= datetime(2026-04-01T00:00:00)
  and sourceTimestamp < datetime(2026-04-02T00:00:00)
| project ...
```

**What it does:**
- Copies April 1, 2026 data only
- Useful for backfilling specific dates

---

## 2️⃣ **Data Deletion**

### **Delete Specific Date:**

```kql
.delete table sqTelemetry records <|
sqTelemetry
| where sourceTimestamp >= datetime(2026-04-26T00:00:00)
  and sourceTimestamp < datetime(2026-04-27T00:00:00)
```

**What it does:**
- Deletes April 26, 2026 data
- Useful for cleaning up before re-insert

---

### **Delete Last 14 Days (Before Bi-weekly Update):**

```kql
.delete table sqTelemetry records <|
sqTelemetry
| where sourceTimestamp >= startofday(ago(14d))
  and sourceTimestamp < startofday(now())
```

**What it does:**
- Deletes last 14 days
- Run before bi-weekly re-copy to avoid duplicates

---

### **Delete All Data:**

```kql
.clear table sqTelemetry data
```

**What it does:**
- Removes ALL data from table
- Table structure remains

---

## 3️⃣ **Date Filtering**

### **Get Yesterday's Data:**

```kql
sqTelemetry
| where sourceTimestamp >= startofday(ago(1d))
  and sourceTimestamp < startofday(now())
```

---

### **Get Today's Data:**

```kql
sqTelemetry
| where sourceTimestamp >= startofday(now())
```

---

### **Get Last 7 Days:**

```kql
sqTelemetry
| where sourceTimestamp >= startofday(ago(7d))
```

---

### **Get Specific Month (April 2026):**

```kql
sqTelemetry
| where sourceTimestamp >= datetime(2026-04-01)
  and sourceTimestamp < datetime(2026-05-01)
```

---

### **Get Data Between Two Dates:**

```kql
sqTelemetry
| where sourceTimestamp >= datetime(2026-04-01T00:00:00)
  and sourceTimestamp < datetime(2026-04-30T23:59:59)
```

---

## 4️⃣ **Aggregations**

### **Count Total Rows:**

```kql
sqTelemetry
| count
```

---

### **Count Yesterday's Rows:**

```kql
sqTelemetry
| where sourceTimestamp >= startofday(ago(1d))
  and sourceTimestamp < startofday(now())
| count
```

---

### **Daily Row Counts (Last 7 Days):**

```kql
sqTelemetry
| where sourceTimestamp >= ago(7d)
| summarize RowCount = count() by Day = startofday(sourceTimestamp)
| order by Day desc
```

**Output:**
```
Day                      RowCount
2026-04-28 00:00:00     12,345
2026-04-27 00:00:00     12,567
2026-04-26 00:00:00     12,234
...
```

---

### **Count by OEM:**

```kql
sqTelemetry
| summarize SiteCount = dcount(siteId), RowCount = count() by oem
| order by RowCount desc
```

**Output:**
```
oem       SiteCount   RowCount
Tesla     245         345,678
Enphase   189         234,567
SolarEdge 156         198,234
```

---

### **Summary Statistics:**

```kql
sqTelemetry
| where sourceTimestamp >= startofday(ago(1d))
| summarize 
    RowCount = count(),
    MinTime = min(sourceTimestamp),
    MaxTime = max(sourceTimestamp),
    UniqueSites = dcount(siteId),
    UniqueOEMs = dcount(oem),
    AvgBatterySOC = avg(battery_713_SoC),
    MaxBatterySOC = max(battery_713_SoC)
```

---

## 5️⃣ **Cross-Database Queries**

### **Query from Another Database:**

```kql
database("eventHouse").silverCommDataSite
| where sourceTimestamp >= ago(1d)
| take 10
```

---

### **Join Across Databases:**

```kql
sqTelemetry
| join kind=inner (
    database("eventHouse").silverCommDataSite
) on siteId, sourceTimestamp
```

---

### **Compare Two Databases:**

```kql
// Count in source
database("eventHouse").silverCommDataSite
| where sourceTimestamp >= datetime(2026-04-01)
| count

// Count in destination
sqTelemetry
| where sourceTimestamp >= datetime(2026-04-01)
| count
```

---

## 6️⃣ **Data Validation**

### **Check for Missing Data (Gaps):**

```kql
sqTelemetry
| summarize DayCount = count() by Day = startofday(sourceTimestamp)
| order by Day asc
| where DayCount == 0  // Find days with no data
```

---

### **Verify Data Copied Correctly:**

```kql
// Source count
let sourceCount = database("eventHouse").silverCommDataSite
| where sourceTimestamp >= datetime(2026-04-01)
  and sourceTimestamp < datetime(2026-04-02)
| count;

// Destination count
let destCount = sqTelemetry
| where sourceTimestamp >= datetime(2026-04-01)
  and sourceTimestamp < datetime(2026-04-02)
| count;

// Compare
print SourceCount = sourceCount, DestCount = destCount, Match = (sourceCount == destCount)
```

---

### **Check Data Labels are NULL:**

```kql
sqTelemetry
| take 10
| project 
    siteId,
    battery_200_DailyWhExp,
    battery_200_DailyWhExp_dl,  // Should be empty
    grid_200_IncWhExp,
    grid_200_IncWhExp_dl        // Should be empty
```

---

### **Find Duplicate Records:**

```kql
sqTelemetry
| summarize Count = count() by siteId, sourceTimestamp
| where Count > 1
```

---

### **Check Table Size Growth:**

```kql
sqTelemetry
| summarize 
    TotalRows = count(),
    EarliestData = min(sourceTimestamp),
    LatestData = max(sourceTimestamp),
    DaysOfData = datetime_diff('day', max(sourceTimestamp), min(sourceTimestamp))
```

---

### **Verify Specific Site Data:**

```kql
sqTelemetry
| where siteId == "400001859"
| where sourceTimestamp >= ago(7d)
| project sourceTimestamp, oem, battery_713_SoC, grid_200_W
| order by sourceTimestamp desc
```

---

## 🎯 **Real-World Scenarios**

### **Scenario 1: Pipeline Failed - Need to Re-run Yesterday**

```kql
// Step 1: Delete yesterday's partial data
.delete table sqTelemetry records <|
sqTelemetry
| where sourceTimestamp >= startofday(ago(1d))
  and sourceTimestamp < startofday(now())

// Step 2: Re-copy yesterday's data
.set-or-append sqTelemetry <|
database("eventHouse").silverCommDataSite
| where sourceTimestamp >= startofday(ago(1d))
  and sourceTimestamp < startofday(now())
| project ...
```

---

### **Scenario 2: Backfill Missing Week**

```kql
.set-or-append sqTelemetry <|
database("eventHouse").silverCommDataSite
| where sourceTimestamp >= datetime(2026-04-15T00:00:00)
  and sourceTimestamp < datetime(2026-04-22T00:00:00)
| project ...
```

---

### **Scenario 3: Daily Health Check**

```kql
// Run every morning to verify yesterday's data
sqTelemetry
| where sourceTimestamp >= startofday(ago(1d))
  and sourceTimestamp < startofday(now())
| summarize 
    RowCount = count(),
    Sites = dcount(siteId),
    OEMs = dcount(oem),
    MinTime = min(sourceTimestamp),
    MaxTime = max(sourceTimestamp)
| extend 
    ExpectedMin = startofday(ago(1d)),
    ExpectedMax = endofday(ago(1d)),
    TimeRangeOK = (MinTime == ExpectedMin and MaxTime <= ExpectedMax)
```

---

**These examples are from your actual VPP work!** 🚀
