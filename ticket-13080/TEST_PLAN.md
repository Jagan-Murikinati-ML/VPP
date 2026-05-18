# Test Plan - GetSiteTelemetry15Min Function
**Ticket:** 13080  
**Author:** Jagan Murikinati  
**Date:** 2026-03-31

---

## 🎯 TESTING STRATEGY

We'll test in 3 phases:
1. **Unit Tests** - Verify timezone conversion logic
2. **Integration Tests** - Query actual data from silverCommDataSite
3. **Validation Tests** - Compare with expected business logic

---

## 📊 TEST DATA

From `silverCommdatasite-sampledata.csv`:
- **Available Sites:** 100001646, 100001737, 100000738, 100001586, 100001574
- **Timestamp:** 2026-03-05 06:18:xx (UTC)
- **Columns:** load_200_W, pv_200_W, battery_200_W, battery_713_SoC

---

## ✅ PHASE 1: UNIT TESTS - TIMEZONE CONVERSION

### Test 1.1: Central Timezone Conversion
```kql
// Input: 06:00 Central → Should query from 12:00 UTC
GetSiteTelemetry15Min(
    "Test",
    dynamic(["100001646"]),
    datetime(2026-03-05 00:18:00),  // 12:18 AM Central
    datetime(2026-03-05 01:18:00),  // 1:18 AM Central
    "Central"
)
```
**Expected:** Query silverCommDataSite from 06:18 UTC to 07:18 UTC ✅

### Test 1.2: Pacific Timezone Conversion
```kql
GetSiteTelemetry15Min(
    "Test",
    dynamic(["100001646"]),
    datetime(2026-03-04 22:18:00),  // 10:18 PM Pacific (previous day)
    datetime(2026-03-04 23:18:00),  // 11:18 PM Pacific
    "Pacific"
)
```
**Expected:** Query from 06:18 UTC to 07:18 UTC ✅

### Test 1.3: IST Timezone Conversion
```kql
GetSiteTelemetry15Min(
    "Test",
    dynamic(["100001646"]),
    datetime(2026-03-05 11:48:00),  // 11:48 AM IST
    datetime(2026-03-05 12:48:00),  // 12:48 PM IST
    "IST"
)
```
**Expected:** Query from 06:18 UTC to 07:18 UTC (IST is UTC+5:30) ✅

### Test 1.4: UTC (No Conversion)
```kql
GetSiteTelemetry15Min(
    "Test",
    dynamic(["100001646"]),
    datetime(2026-03-05 06:18:00),
    datetime(2026-03-05 07:18:00),
    "UTC"
)
```
**Expected:** Query from 06:18 UTC to 07:18 UTC (no conversion) ✅

---

## ✅ PHASE 2: INTEGRATION TESTS - ACTUAL DATA

### Test 2.1: Single Site, Single Interval
```kql
GetSiteTelemetry15Min(
    "SingleSiteTest",
    dynamic(["100001646"]),
    datetime(2026-03-05 06:15:00),  // UTC
    datetime(2026-03-05 06:30:00),  // UTC (15 min)
    "UTC"
)
```
**Expected:**
- 1 row returned
- Site_ID = 100001646
- Interval_Start_UTC = 2026-03-05 06:15:00
- Interval_End_UTC = 2026-03-05 06:30:00
- Reading_Count >= 1

### Test 2.2: Multiple Sites, Single Interval
```kql
GetSiteTelemetry15Min(
    "MultiSiteTest",
    dynamic(["100001646", "100001737", "100000738"]),
    datetime(2026-03-05 06:15:00),
    datetime(2026-03-05 06:30:00),
    "UTC"
)
```
**Expected:**
- 3 rows (one per site)
- All intervals: 06:15 - 06:30 UTC

### Test 2.3: Single Site, Multiple Intervals
```kql
GetSiteTelemetry15Min(
    "MultiIntervalTest",
    dynamic(["100001646"]),
    datetime(2026-03-05 06:00:00),
    datetime(2026-03-05 07:00:00),  // 1 hour = 4 intervals
    "UTC"
)
```
**Expected:**
- Up to 4 rows (06:00, 06:15, 06:30, 06:45)
- All for Site_ID = 100001646

### Test 2.4: Multiple Sites, Multiple Intervals
```kql
GetSiteTelemetry15Min(
    "FullTest",
    dynamic(["100001646", "100001737"]),
    datetime(2026-03-05 06:00:00),
    datetime(2026-03-05 07:00:00),
    "UTC"
)
```
**Expected:**
- Up to 8 rows (2 sites × 4 intervals)
- Ordered by Site_ID, then Interval_Start_UTC

---

## ✅ PHASE 3: VALIDATION TESTS

### Test 3.1: Verify Unit Conversion (Watts → kW)
```kql
// Check if values are properly divided by 1000
GetSiteTelemetry15Min(
    "UnitTest",
    dynamic(["100001646"]),
    datetime(2026-03-05 06:15:00),
    datetime(2026-03-05 06:30:00),
    "UTC"
)
```
**Manual Check:**
- Site_Load_kW should be reasonable (typically 0-10 kW for residential)
- Values should be in kW, not W

### Test 3.2: Verify Aggregation (avg)
```kql
// Compare function output with manual calculation
GetSiteTelemetry15Min(
    "AggTest",
    dynamic(["100001646"]),
    datetime(2026-03-05 06:15:00),
    datetime(2026-03-05 06:30:00),
    "UTC"
)

// Compare with raw data:
database('EventHouse').table('silverCommDataSite')
| where siteId == "100001646"
    and sourceTimestamp >= datetime(2026-03-05 06:15:00)
    and sourceTimestamp < datetime(2026-03-05 06:30:00)
| summarize 
    manual_avg_load = avg(load_200_W) / 1000,
    manual_avg_pv = avg(pv_200_W) / 1000,
    manual_count = count()
```
**Expected:** Function output matches manual calculation ✅

---

## 🚀 EXECUTION CHECKLIST

- [ ] Deploy function to Fabric/Kusto
- [ ] Run Test 1.1 - Central timezone
- [ ] Run Test 1.4 - UTC (no conversion)
- [ ] Run Test 2.1 - Single site
- [ ] Run Test 2.4 - Full test
- [ ] Run Test 3.2 - Verify aggregation
- [ ] Document any issues found
- [ ] Get Naveen's confirmation on SoC aggregation
- [ ] Adjust if needed and re-test

---

## 📝 TEST RESULTS TEMPLATE

```
Test: [Test ID - Description]
Status: [ ] PASS  [ ] FAIL
Query: [Copy query here]
Result: [Describe outcome]
Notes: [Any observations]
```

