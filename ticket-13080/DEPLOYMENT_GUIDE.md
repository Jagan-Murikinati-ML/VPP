# Deployment Guide - GetSiteTelemetry15Min Function
**Ticket:** 13080  
**Author:** Jagan Murikinati  
**Date:** 2026-03-31

---

## 🎯 PRE-DEPLOYMENT CHECKLIST

- [x] Function code reviewed and approved
- [x] Based on confirmed API reference from Ayub
- [x] Timezone conversion logic implemented
- [ ] Naveen confirms SoC aggregation method
- [ ] Test plan executed successfully
- [ ] Stakeholder approval obtained

---

## 📋 DEPLOYMENT STEPS

### Step 1: Access Fabric/Kusto Environment

**Option A: Microsoft Fabric Portal**
1. Navigate to https://fabric.microsoft.com
2. Open your workspace
3. Select KQL Database: `eventhouse` or `eventhousevpp`

**Option B: Kusto Web Explorer**
1. Navigate to https://dataexplorer.azure.com
2. Connect to your cluster
3. Select database: `EventHouse`

---

### Step 2: Deploy the Function

1. **Open Query Editor**
2. **Copy the function code** from `getSiteTelemetryDataByProgram.kql`
3. **Execute the `.create-or-alter function` statement**

```kql
.create-or-alter function GetSiteTelemetry15Min(
    programName: string,
    siteList: dynamic,
    startTime: datetime,
    endTime: datetime,
    timeZone: string
)
{
    // [Full function code here]
}
```

4. **Verify deployment:**
```kql
.show functions | where Name == "GetSiteTelemetry15Min"
```

Expected output: Function details displayed ✅

---

### Step 3: Test the Deployed Function

**Quick Smoke Test:**
```kql
GetSiteTelemetry15Min(
    "TestProgram",
    dynamic(["100001646"]),
    datetime(2026-03-05 06:15:00),
    datetime(2026-03-05 06:30:00),
    "UTC"
)
```

**Expected:** Returns data with 8 columns, no errors ✅

---

### Step 4: Run Test Suite

Execute tests from `TEST_PLAN.md`:
1. Timezone conversion tests
2. Integration tests with actual data
3. Validation tests

Document results in test log.

---

### Step 5: Post-Deployment Validation

**Verify output schema:**
```kql
GetSiteTelemetry15Min(
    "Schema",
    dynamic(["100001646"]),
    datetime(2026-03-05 06:00:00),
    datetime(2026-03-05 07:00:00),
    "UTC"
)
| getschema
```

**Expected columns:**
- Site_ID (string)
- Interval_Start_UTC (datetime)
- Interval_End_UTC (datetime)
- Site_Load_kW (real)
- PV_Generation_kW (real)
- Battery_Power_kW (real)
- Battery_SoC_Percent (real)
- Reading_Count (long)

---

## 🔄 IF NAVEEN REQUESTS SoC CHANGE

If Naveen confirms to use **latest SoC** instead of average:

**Update Line 66:**

**FROM:**
```kql
avg_soc = avg(battery_713_SoC),
```

**TO:**
```kql
latest_soc = arg_max(sourceTimestamp, battery_713_SoC),
```

**Update Line 78:**

**FROM:**
```kql
Battery_SoC_Percent = round(avg_soc, 2)
```

**TO:**
```kql
Battery_SoC_Percent = round(latest_soc, 2)
```

Then re-deploy using `.create-or-alter function` and re-test.

---

## 📊 ROLLBACK PLAN

If issues are discovered after deployment:

**Option 1: Drop the function**
```kql
.drop function GetSiteTelemetry15Min
```

**Option 2: Revert to previous version**
```kql
.show function GetSiteTelemetry15Min version=1  // Check previous version
.create-or-alter function GetSiteTelemetry15Min ... // Restore old code
```

---

## ✅ POST-DEPLOYMENT COMMUNICATION

### Update Ticket 13080

```markdown
**Status Update:**
✅ Function `GetSiteTelemetry15Min` deployed to [environment name]
✅ Tested with sample data - results validated
✅ Ready for use by consuming applications

**Function Signature:**
GetSiteTelemetry15Min(programName, siteList, startTime, endTime, timeZone)

**Example Usage:**
[Include example from TEST_PLAN.md]

**Next Steps:**
- Integrate with consuming applications
- Monitor performance in production
- Gather feedback from users
```

---

### Notify Stakeholders

**Email/Teams Message:**
```
Subject: Ticket 13080 - GetSiteTelemetry15Min Function Deployed

Hi @Ayub @Naveen @Juan,

The GetSiteTelemetry15Min function is now deployed and ready for use.

Function Details:
- Database: EventHouse
- Function Name: GetSiteTelemetry15Min
- Implementation: Based on Telemetry API (rollup=avg pattern)
- Timezone Support: Central, Eastern, Pacific, Mountain, IST, UTC

Tested with sample data - all tests passing ✅

Please let me know if you need any adjustments or have questions.

Thanks,
Jagan
```

---

## 📝 DEPLOYMENT LOG TEMPLATE

```
Deployment Date: ___________
Environment: ___________
Database: ___________
Deployed By: ___________

Pre-deployment checks:
[ ] Code reviewed
[ ] Tests passed
[ ] Approval obtained

Deployment:
[ ] Function created/updated
[ ] Deployment verified
[ ] Smoke test passed

Post-deployment:
[ ] Test suite executed
[ ] Schema validated
[ ] Stakeholders notified

Issues/Notes:
_________________________________
```

