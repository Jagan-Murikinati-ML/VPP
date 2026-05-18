# Ticket 13080 - GetSiteTelemetry15Min Function

**Status:** ✅ Implementation Complete - Awaiting Final Confirmation  
**Author:** Jagan Murikinati  
**Date:** 2026-03-31

---

## 📋 OVERVIEW

Created a Fabric (KQL) function to retrieve site telemetry data for a program within a specified time range, aggregated in 15-minute intervals.

---

## 🎯 REQUIREMENTS (From Ticket)

**Input Parameters:**
- Program Name
- Site List
- Start Time
- End Time
- Time Zone

**Output Fields (15-min intervals):**
- Site ID
- Interval Start (UTC)
- Interval End (UTC)
- Site Load (kW)
- PV Generation (kW)
- Battery Power (kW)
- Battery State of Charge (SoC %)

---

## ✅ IMPLEMENTATION SUMMARY

### **Function Name:** `GetSiteTelemetry15Min`

### **Database:** EventHouse

### **Data Source:** `silverCommDataSite` table

### **Implementation Details:**

1. **Timezone Handling (Confirmed by Ayub):**
   - Input times in program timezone
   - Automatic conversion to UTC
   - Supports: Central, Eastern, Pacific, Mountain, IST, UTC

2. **Aggregation (Based on API reference):**
   - Uses `rollup=avg` pattern
   - Applies `avg()` to all power metrics
   - Applies `avg()` to SoC (pending Naveen's confirmation)

3. **Column Mapping (From Ayub's API reference):**
   - Site Load ← `load_200_W`
   - PV Generation ← `pv_200_W`
   - Battery Power ← `battery_200_W`
   - Battery SoC ← `battery_713_SoC`

4. **Unit Conversion:**
   - Watts → Kilowatts (÷ 1000)

---

## 📁 FILES IN THIS FOLDER

| File | Purpose |
|------|---------|
| `getSiteTelemetryDataByProgram.kql` | Main function code |
| `test_queries.kql` | Complete test suite (10 tests) |
| `TEST_PLAN.md` | Detailed testing strategy |
| `DEPLOYMENT_GUIDE.md` | Step-by-step deployment instructions |
| `README.md` | This file - overview and quick start |

---

## 🚀 QUICK START

### 1. Deploy the Function

```kql
// Copy and execute the code from getSiteTelemetryDataByProgram.kql
.create-or-alter function GetSiteTelemetry15Min(...)
```

### 2. Run a Test Query

```kql
GetSiteTelemetry15Min(
    "TestProgram",
    dynamic(["100001646", "100001737"]),
    datetime(2026-03-05 06:00:00),
    datetime(2026-03-05 07:00:00),
    "UTC"
)
```

### 3. Verify Output

Expected columns:
- `Site_ID`
- `Interval_Start_UTC`
- `Interval_End_UTC`
- `Site_Load_kW`
- `PV_Generation_kW`
- `Battery_Power_kW`
- `Battery_SoC_Percent`
- `Reading_Count`

---

## 📊 EXAMPLE USAGE

### Example 1: Central Timezone Program
```kql
GetSiteTelemetry15Min(
    "IL Program",
    dynamic(["400005226", "400002331"]),
    datetime(2026-03-05 08:00:00),  // 8 AM Central
    datetime(2026-03-05 10:00:00),  // 10 AM Central
    "Central"
)
```
Function automatically converts 08:00-10:00 Central → 14:00-16:00 UTC

### Example 2: Pacific Timezone Program
```kql
GetSiteTelemetry15Min(
    "California Program",
    dynamic(["100001646"]),
    datetime(2026-03-05 09:00:00),  // 9 AM Pacific
    datetime(2026-03-05 17:00:00),  // 5 PM Pacific
    "America/Los_Angeles"
)
```

---

## ⏳ PENDING ITEMS

### Awaiting Confirmation from Naveen:

**Battery SoC Aggregation Method:**
- Current: `avg(battery_713_SoC)` - Average SoC over interval
- Alternative: `arg_max(sourceTimestamp, battery_713_SoC)` - Latest SoC

Once confirmed, may need minor adjustment (1-line change).

---

## ✅ TESTING STATUS

| Test Category | Status | Details |
|---------------|--------|---------|
| Timezone Conversion | ✅ Ready | Tests in `test_queries.kql` |
| Single Site Query | ✅ Ready | Test 1 |
| Multiple Sites | ✅ Ready | Test 3 |
| Aggregation Logic | ✅ Ready | Test 4 (manual comparison) |
| Edge Cases | ✅ Ready | Tests 5, 6 |
| Output Schema | ✅ Ready | Test 7 |
| Performance | ✅ Ready | Test 10 |

**All tests documented in:** `test_queries.kql`

---

## 📞 STAKEHOLDERS

- **Product:** Ayub Shirgaonkar (confirmed timezone handling + API reference)
- **Engineering:** Juan Pablo Culebro (code review)
- **Validation:** Naveen Siddalingaswamy (pending SoC confirmation)

---

## 📝 NEXT STEPS

1. ✅ Function code complete
2. ⏳ Await Naveen's confirmation on SoC aggregation
3. ⏳ Deploy to Fabric environment
4. ⏳ Execute test suite (`test_queries.kql`)
5. ⏳ Validate results
6. ⏳ Close ticket 13080

---

## 🔗 RELATED TICKETS

- Ticket 13080 (this ticket)
- Reference API: `/monitoring/v1/time-aggregation` (rollup=avg)

---

**For detailed deployment instructions, see:** `DEPLOYMENT_GUIDE.md`  
**For comprehensive testing, see:** `TEST_PLAN.md` and `test_queries.kql`

