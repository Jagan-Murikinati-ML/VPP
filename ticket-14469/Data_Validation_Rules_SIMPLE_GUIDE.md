# Data Validation Rules - Simple Understanding Guide

**Document Purpose:** Understand data validation rules in simple language with real examples  
**Created For:** Jagan Murikinati  
**Date:** April 9, 2026

---

## 🏢 PART 1: WHO IS WHO?

### Qcells (Your Company)
- **What:** Solar panel + battery manufacturer and installer
- **Business Model:** 
  - Sells solar + battery systems to homeowners
  - Controls customer batteries to help utilities during emergencies
  - Gets paid by utilities for grid services
  
### Utility Companies (The Customers)
- **Examples:** PG&E, SCE, SDG&E (California electric companies)
- **What they do:** Generate and distribute electricity, manage the power grid
- **Why they pay Qcells:** Need help during peak demand or emergencies

### Homeowners (Asset Owners)
- **What:** Buy Qcells solar + battery for their home
- **Why participate:** Get incentive payments when Qcells uses their battery
- **Control:** Allow Qcells to remotely control their battery

---

## 💰 PART 2: HOW MONEY FLOWS

### Revenue Stream 1: Direct Sales
```
Homeowner → Qcells: $25,000 (buy solar + battery)
```
One-time payment (product sale)

### Revenue Stream 2: Grid Services (WHY WE NEED DATA VALIDATION!)
```
Step 1: Utility (PG&E) → Qcells: "Discharge batteries during emergency"
Step 2: Qcells → Customer Batteries: Remote control to discharge
Step 3: Batteries → Grid: Send power (e.g., 5000 kWh total)
Step 4: Qcells → Utility: Submit validated data proving 5000 kWh
Step 5: Utility → Qcells: Payment ($10,000 = 5000 kWh × $2/kWh)
Step 6: Qcells → Homeowners: Share revenue ($5,000)
Step 7: Qcells keeps: Profit ($5,000)
```

**Key Point:** Utility only pays if data is validated (SQMD quality)!

---

## 📋 PART 3: BACKGROUND & PURPOSE (Section-by-Section)

### Section: "Accurate, settlement-quality telemetry is foundational..."

**Simple Translation:**
> The energy data from batteries must be accurate and trustworthy, otherwise utilities won't pay Qcells.

**Real Example:**

**Scenario:** Grid emergency on April 5, 2026, 6-8 PM

**Without Good Data:**
```
Qcells says: "We discharged 5000 kWh"
Utility asks: "Prove it"
Qcells provides: Messy data with missing timestamps and wrong values
Utility responds: ❌ REJECTED - Data not trustworthy
Payment: $0
```

**With Settlement-Quality Data:**
```
Qcells says: "We discharged 5000 kWh"
Qcells provides: Clean data with all intervals, correct timestamps, validated values
Utility responds: ✅ ACCEPTED - SQMD quality
Payment: $10,000
```

---

### Section: "Qcells applies standardized data validation rules aligned with CPUC SQMD principles..."

**Simple Translation:**
> Qcells follows California's official data quality standards (SQMD) so utilities will trust and accept the data.

**What is SQMD?**
- **SQMD** = Settlement Quality Meter Data
- **Created by:** CPUC (California Public Utilities Commission)
- **Purpose:** Official standard for "good enough to bill" energy data
- **Think of it as:** FDA approval for food, but for energy data

**Real Example:**

**Without SQMD Standards:**
```
Qcells: "Here's our data (custom format)"
PG&E: "We don't accept custom formats. Too risky."
Result: No payment
```

**With SQMD Standards:**
```
Qcells: "Here's SQMD-compliant data"
PG&E: "This meets California standards. We accept it."
Result: Payment approved
```

---

### Section: "This BRD defines business requirements for data validation only..."

**Simple Translation:**
> This document only talks about checking if data is good/bad. How to fix bad data is covered in a different document.

**Three Separate Processes:**

1. **Validation** (THIS DOCUMENT)
   - Check if data is good or bad
   - Example: "Battery 003 has missing intervals → Flag as BAD"

2. **Estimation** (DIFFERENT DOCUMENT)
   - Fill in missing data using smart guesses
   - Example: "Interval missing at 6:30 PM → Estimate using 6:15 PM and 6:45 PM average"

3. **Editing** (DIFFERENT DOCUMENT)
   - Correct wrong data
   - Example: "Value shows 500 kWh but battery capacity is 10 kWh → Correct to 5 kWh"

---

## 📊 PART 4: SCOPE (What Data Needs Validation?)

### "Interval-based solar production telemetry"

**Simple Translation:** Data from solar panels, recorded every 15 minutes

**Real Example:**
```
Solar Panel Site 001 - April 5, 2026
12:00 PM: Generated 3.2 kWh
12:15 PM: Generated 3.5 kWh
12:30 PM: Generated 3.3 kWh
12:45 PM: Generated 3.4 kWh
... (96 intervals per day)
```

---

### "Interval-based battery operational telemetry"

**Simple Translation:** Data from batteries, recorded every 15 minutes

**Real Example:**
```
Battery Site 010 - April 5, 2026, 6:00-8:00 PM (Grid Event)
6:00 PM: Discharged 2.5 kWh, SoC: 100%
6:15 PM: Discharged 2.8 kWh, SoC: 90%
6:30 PM: Discharged 2.6 kWh, SoC: 80%
6:45 PM: Discharged 2.7 kWh, SoC: 70%
... (8 intervals during event)
```

---

## 🎯 PART 5: USE CASES (Why Validate Data?)

### Use Case 1: Grid Services Programs
**Program:** DSGS (Demand Side Grid Support)  
**Scenario:** California heatwave, grid under stress  
**Qcells Role:** Discharge 100 batteries to help grid  
**Data Validation Need:** Prove to utility how much energy was provided  
**Payment:** Based on validated kWh data

### Use Case 2: Settlement and Incentive Calculations
**Scenario:** End of month billing  
**Utility calculates:** How much to pay Qcells for April 2026  
**Data needed:** All validated discharge events for the month  
**Payment formula:** Total validated kWh × Rate per kWh

### Use Case 3: Performance Analytics
**Scenario:** Qcells internal reporting  
**Question:** "Are our batteries performing as expected?"  
**Data needed:** Validated telemetry to measure actual vs. expected performance  
**Use:** Business decisions, forecasting, program optimization

---

## 📝 SUMMARY - KEY TAKEAWAYS

1. **Qcells** = Company that manages customer batteries to help utilities
2. **Utilities** = Electric companies that pay Qcells for grid services
3. **Homeowners** = Own the batteries, get paid to participate
4. **SQMD** = California's official standard for trustworthy energy data
5. **Validation** = Checking if data is good/bad (this document's focus)
6. **Why it matters** = No validation → No payment from utilities

---

## 🚀 NEXT: VALIDATION RULES (Coming in Next Section)

We'll cover each validation rule with simple examples:
- Interval Completeness
- Time Integrity
- Spike Detection
- Sum Check
- Channel Mapping
- And more...

---

## 📊 PART 6: DATA INPUTS (What Data Do We Collect?)

### Input 1: Solar Telemetry

**Simple Translation:** How much electricity the solar panels are generating

**What it includes:** Inverter-level production data

**Real Example:**
```
Site: Home_12345
Date: April 5, 2026
Time: 12:00 PM
Solar Production: 3.5 kWh (in last 15 minutes)
```

**Why we need it:**
- Track how much solar energy is being produced
- Compare to battery charging data
- Validate energy balance (where is the solar power going?)

**Data Source:** Solar inverter (device that converts DC to AC power)

---

### Input 2: Battery Telemetry

**Simple Translation:** What the battery is doing (charging, discharging, idle)

**What it includes:**
- Charge/discharge data (how much energy in/out)
- SoC (State of Charge = battery percentage, like phone battery %)

**Real Example:**
```
Site: Home_12345
Date: April 5, 2026, 6:00 PM
Action: Discharging (sending power to grid)
Energy: 2.5 kWh discharged in last 15 minutes
SoC Before: 100% (full battery)
SoC After: 90% (battery used 10%)
Battery Capacity: 10 kWh
```

**Why we need it:**
- Prove to utility how much power was provided
- Calculate payment
- Ensure battery isn't over-discharged (damage protection)

**Data Source:** Battery management system (BMS)

---

### Input 3: Grid Import/Export Data

**Simple Translation:** Power flowing to/from the electric grid

**What it includes:**
- **Import:** Power FROM grid TO home (buying electricity)
- **Export:** Power FROM home TO grid (selling electricity)

**Real Example - Import (Buying from Grid):**
```
Site: Home_12345
Time: 8:00 PM (nighttime, no solar)
Import: 1.5 kWh (home needs power, solar not working, buying from grid)
Export: 0 kWh
```

**Real Example - Export (Selling to Grid):**
```
Site: Home_12345
Time: 12:00 PM (midday, excess solar)
Import: 0 kWh
Export: 2.0 kWh (solar producing more than home needs, selling excess)
```

**Real Example - Grid Event (Battery Helping Grid):**
```
Site: Home_12345
Time: 6:00 PM (peak demand event)
Import: 0 kWh
Export: 2.5 kWh (battery discharging to help grid)
Payment: 2.5 kWh × $2/kWh = $5
```

**Why we need it:**
- Track energy flow direction
- Calculate utility bills
- Calculate grid services payments

**Data Source:** Utility meter or OEM API (Tesla, Enphase, etc.)

---

### Input 4: Consumption Data

**Simple Translation:** How much electricity the home is using

**What it includes:** Total energy consumed by home appliances, AC, lights, etc.

**Real Example:**
```
Site: Home_12345
Time: 6:00 PM (family cooking dinner, AC running)
Consumption: 4.0 kWh in last 15 minutes

Breakdown (estimated):
- Air Conditioning: 2.0 kWh
- Kitchen appliances: 1.0 kWh
- Lights, TV, other: 1.0 kWh
```

**How it's calculated:**
```
Consumption = (Solar Production + Grid Import + Battery Discharge)
              - (Grid Export + Battery Charge)

Example:
Solar: 1.0 kWh
Grid Import: 2.0 kWh
Battery Discharge: 1.5 kWh
Grid Export: 0 kWh
Battery Charge: 0 kWh

Consumption = (1.0 + 2.0 + 1.5) - (0 + 0) = 4.5 kWh
```

**Why we need it:**
- Validate energy balance (all energy must be accounted for)
- Detect data errors (if numbers don't add up)
- Customer billing

**Data Source:** Calculated from other inputs

---

### Input 5: Enrollment Metadata

**Simple Translation:** Information about the site and equipment

**What it includes:**
- Asset ID (unique battery identifier)
- Site ID (unique home identifier)
- Battery capacity (max kWh it can store)
- Installation date
- Program enrollment (DSGS, SGIP, etc.)

**Real Example:**
```
Site ID: SITE_12345
Asset ID: BATTERY_67890
Customer: John Smith
Address: 123 Main St, San Jose, CA 95110
Battery Model: Tesla Powerwall 2
Battery Capacity: 13.5 kWh
Installation Date: Jan 15, 2025
Programs Enrolled: DSGS, SGIP
Status: Active
```

**Why we need it:**
- Link telemetry data to correct site/battery
- Validate capacity limits (can't discharge more than battery holds)
- Determine which programs apply
- Calculate correct incentive payments

**Data Source:** Qcells enrollment database

---

### Input 6: Time Reference

**Simple Translation:** Accurate timestamps with correct timezone

**What it includes:**
- UTC timestamp (universal time)
- Local timezone (PST, PDT, etc.)
- DST awareness (daylight saving time)

**Real Example:**
```
Event: Battery discharge during grid emergency
UTC Time: 2026-04-05T01:00:00Z
Local Time (California): 2026-04-04 18:00:00 PDT (6:00 PM)
Timezone: America/Los_Angeles
DST Active: Yes (Pacific Daylight Time)
```

**Why timezone matters:**

**Wrong Timezone Example:**
```
Event actually happened: 6:00 PM California time
Data submitted with: 6:00 PM UTC (wrong!)
Utility sees: Event at 11:00 AM California time (wrong time slot!)
Result: ❌ Payment rejected (event was 6-8 PM, not 11 AM)
```

**Correct Timezone Example:**
```
Event: 6:00 PM California time (PDT)
Converted to UTC: 01:00:00 UTC (next day)
Utility converts back: 6:00 PM PDT ✅
Result: ✅ Payment approved
```

**Why we need it:**
- Events are time-specific (6-8 PM peak demand)
- Wrong time = wrong billing = no payment
- DST transitions can cause errors

**Data Source:** System clock with timezone database

---

## 🔄 PART 7: HOW ALL INPUTS WORK TOGETHER

### Complete Data Flow Example:

**Scenario: Grid Event on April 5, 2026, 6:00-6:15 PM**

```
1. Time Reference:
   UTC: 2026-04-05T01:00:00Z
   Local: 2026-04-04 18:00:00 PDT

2. Enrollment Metadata:
   Site: SITE_12345
   Battery: BATTERY_67890 (13.5 kWh capacity)
   Program: DSGS

3. Solar Telemetry:
   Production: 0.5 kWh (sun setting, low production)

4. Battery Telemetry:
   Discharge: 2.5 kWh (helping grid)
   SoC: 100% → 90%

5. Grid Import/Export:
   Import: 0 kWh
   Export: 2.0 kWh (battery power to grid)

6. Consumption:
   Home usage: 1.0 kWh

Energy Balance Check:
   Input: Solar (0.5) + Grid Import (0) + Battery Discharge (2.5) = 3.0 kWh
   Output: Grid Export (2.0) + Consumption (1.0) = 3.0 kWh
   ✅ BALANCED!

Payment Calculation:
   Grid Export: 2.0 kWh × $2/kWh = $4
   To Qcells: $2
   To Customer: $2
```

---

## ✅ PART 8: VALIDATION CHECKS OVERVIEW (What Rules Do We Check?)

There are **7 main validation checks** to ensure data quality:

| # | Validation Check | What It Checks | Difficulty | Your Work |
|---|------------------|----------------|------------|-----------|
| 1 | Interval Completeness | All 96 intervals per day present | Easy | ✅ You'll implement |
| 2 | Sum Check | Energy numbers add up correctly | Easy | ✅ You'll implement |
| 3 | Spike Detection | No impossible values | Easy | ✅ You'll implement |
| 4 | Time Integrity | Timestamps are correct | Medium | ✅ You'll implement |
| 5 | Meter Identity | Correct site/battery IDs | Easy | ✅ You'll implement |
| 6 | High/Low Usage | Values within normal range | TBD | Maybe later |
| 7 | Channel Mapping | Power flows correct direction | TBD | Maybe later |

**Focus for next sprint:** Checks 1, 2, 3, 4, 5 (the "Easy" and "Medium" ones)

---

## 🔍 PART 9: VALIDATION CHECK #1 - INTERVAL COMPLETENESS

### What It Checks:
> Every day must have exactly 96 intervals (15-minute intervals × 4 per hour × 24 hours = 96)

### Why It Matters:
If intervals are missing, utility can't verify total energy provided → No payment

---

### Simple Example - PASS ✅

**Date:** April 5, 2026
**Site:** SITE_12345

```
12:00 AM - 12:15 AM: ✅ Present
12:15 AM - 12:30 AM: ✅ Present
12:30 AM - 12:45 AM: ✅ Present
... (all 96 intervals)
11:30 PM - 11:45 PM: ✅ Present
11:45 PM - 12:00 AM: ✅ Present

Total intervals: 96
Result: ✅ PASS - Complete data
```

---

### Simple Example - FAIL ❌

**Date:** April 5, 2026
**Site:** SITE_67890

```
12:00 AM - 12:15 AM: ✅ Present
12:15 AM - 12:30 AM: ❌ MISSING!
12:30 AM - 12:45 AM: ✅ Present
... (some missing intervals)
6:00 PM - 6:15 PM: ❌ MISSING! (This was during grid event!)
6:15 PM - 6:30 PM: ✅ Present

Total intervals: 92 (missing 4)
Result: ❌ FAIL - Incomplete data
Action: Flag for estimation or reject
```

---

### Real-World Impact Example:

**Grid Event: April 5, 2026, 6:00-8:00 PM**

**Site A (Complete Data):**
```
6:00 PM: 2.5 kWh ✅
6:15 PM: 2.8 kWh ✅
6:30 PM: 2.6 kWh ✅
... (all 8 intervals present)
Total: 20 kWh
Payment: 20 kWh × $2 = $40 ✅
```

**Site B (Missing Intervals):**
```
6:00 PM: 2.5 kWh ✅
6:15 PM: MISSING ❌
6:30 PM: 2.6 kWh ✅
... (2 of 8 intervals missing)
Total: Can't calculate (incomplete)
Payment: $0 ❌ (Utility rejects incomplete data)
```

**Lost Revenue:** $40 per site × 100 sites = $4,000 lost!

---

### How You'll Implement This (KQL Pseudocode):

```kql
// Step 1: Count intervals per site per day
let interval_check =
    silverCommDataSite
    | where timestamp >= datetime(2026-04-05) and timestamp < datetime(2026-04-06)
    | summarize interval_count = count() by site_id, format_datetime(timestamp, 'yyyy-MM-dd')
    | extend expected_intervals = 96
    | extend is_complete = iff(interval_count == 96, "✅ PASS", "❌ FAIL")
    | extend missing_intervals = 96 - interval_count;

// Step 2: Show results
interval_check
| project site_id, date, interval_count, expected = 96, status = is_complete, missing_intervals
```

**Output Example:**
```
site_id       | date       | interval_count | expected | status    | missing_intervals
SITE_12345    | 2026-04-05 | 96            | 96       | ✅ PASS   | 0
SITE_67890    | 2026-04-05 | 92            | 96       | ❌ FAIL   | 4
SITE_11111    | 2026-04-05 | 88            | 96       | ❌ FAIL   | 8
```

---

### Edge Case: Daylight Saving Time (DST)

**Spring Forward (March):**
```
Normal day: 96 intervals
DST day (lose 1 hour): 92 intervals (correct!)
Your code must: Expect 92 on DST spring day
```

**Fall Back (November):**
```
Normal day: 96 intervals
DST day (gain 1 hour): 100 intervals (correct!)
Your code must: Expect 100 on DST fall day
```

**Implementation Note:** Document says "DST-adjusted" - you'll need to handle this!

---

## 🔍 PART 10: VALIDATION CHECK #2 - SUM CHECK

### What It Checks:
> Energy IN = Energy OUT (conservation of energy)

### Why It Matters:
If numbers don't add up, data is wrong → Utility rejects

---

### Energy Balance Formula:

```
Energy IN = Energy OUT

IN:  Solar Production + Grid Import + Battery Discharge
OUT: Grid Export + Consumption + Battery Charge
```

---

### Simple Example - PASS ✅

**15-minute interval: April 5, 2026, 12:00-12:15 PM**

```
ENERGY IN:
- Solar Production: 3.0 kWh
- Grid Import: 0 kWh
- Battery Discharge: 0 kWh
Total IN: 3.0 kWh

ENERGY OUT:
- Grid Export: 2.0 kWh (excess solar to grid)
- Consumption: 1.0 kWh (home usage)
- Battery Charge: 0 kWh
Total OUT: 3.0 kWh

Balance: 3.0 = 3.0 ✅ PASS
```

---

### Simple Example - FAIL ❌

**15-minute interval: April 5, 2026, 6:00-6:15 PM**

```
ENERGY IN:
- Solar Production: 0.5 kWh
- Grid Import: 0 kWh
- Battery Discharge: 2.5 kWh
Total IN: 3.0 kWh

ENERGY OUT:
- Grid Export: 2.0 kWh
- Consumption: 1.0 kWh
- Battery Charge: 0 kWh
Total OUT: 3.0 kWh

Wait... but data shows:
Grid Export recorded as: 5.0 kWh ❌ (Wrong!)

New Total OUT: 6.0 kWh

Balance: 3.0 ≠ 6.0 ❌ FAIL
Error: 3.0 kWh difference (impossible!)
```

**Problem:** Can't export 5 kWh when only 3 kWh came in! Data error!

---

### Real-World Example:

**Scenario: Sensor Malfunction**

```
Battery discharges: 2.5 kWh (actual)
Sensor reports: 25.0 kWh (wrong - decimal error!)

Energy IN: 25.0 kWh (wrong sensor reading)
Energy OUT: 2.0 kWh (export) + 1.0 kWh (consumption) = 3.0 kWh
Balance: 25.0 ≠ 3.0 ❌ FAIL

Sum Check catches error → Flag for review
Without sum check → Utility sees 25 kWh claim → Rejects as impossible → No payment
```

---

### How You'll Implement This (KQL Pseudocode):

```kql
// Step 1: Calculate energy balance per interval
let sum_check =
    silverCommDataSite
    | where timestamp >= datetime(2026-04-05) and timestamp < datetime(2026-04-06)
    | extend energy_in = solar_production + grid_import + battery_discharge
    | extend energy_out = grid_export + consumption + battery_charge
    | extend balance_diff = energy_in - energy_out
    | extend tolerance = 0.1  // Allow 0.1 kWh difference (rounding)
    | extend is_balanced = iff(abs(balance_diff) <= tolerance, "✅ PASS", "❌ FAIL");

// Step 2: Show failed checks
sum_check
| where is_balanced == "❌ FAIL"
| project site_id, timestamp, energy_in, energy_out, balance_diff, status = is_balanced
```

**Output Example:**
```
site_id    | timestamp           | energy_in | energy_out | balance_diff | status
SITE_67890 | 2026-04-05 18:00:00 | 3.0       | 6.0        | -3.0         | ❌ FAIL
SITE_11111 | 2026-04-05 12:15:00 | 25.0      | 3.0        | 22.0         | ❌ FAIL
```

---

## 🔍 PART 11: VALIDATION CHECK #3 - SPIKE DETECTION

### What It Checks:
> Values must be physically possible (can't discharge more than battery capacity)

### Why It Matters:
Impossible values = bad sensor or data error → Utility rejects

---

### Simple Example - PASS ✅

**Battery Capacity:** 10 kWh (Tesla Powerwall 2)

```
15-minute intervals:
6:00 PM: Discharged 2.5 kWh ✅ (Possible - less than 10 kWh)
6:15 PM: Discharged 2.8 kWh ✅ (Possible)
6:30 PM: Discharged 2.6 kWh ✅ (Possible)
6:45 PM: Discharged 2.7 kWh ✅ (Possible)

Result: ✅ PASS - All values within capacity
```

---

### Simple Example - FAIL ❌

**Battery Capacity:** 10 kWh

```
15-minute intervals:
6:00 PM: Discharged 2.5 kWh ✅
6:15 PM: Discharged 50 kWh ❌ SPIKE! (Impossible - battery only holds 10 kWh!)
6:30 PM: Discharged 2.6 kWh ✅
6:45 PM: Discharged 2.7 kWh ✅

Result: ❌ FAIL - Spike detected at 6:15 PM
Likely cause: Sensor error, decimal point error, bad data
Action: Flag for manual review or estimation
```

---

### Real-World Example:

**Scenario: Decimal Point Error**

```
Battery actually discharged: 5.0 kWh
Sensor reports: 50.0 kWh (decimal error!)

Check against capacity: 10 kWh
50 kWh > 10 kWh → ❌ SPIKE DETECTED

Without spike detection:
- Submit 50 kWh to utility
- Utility sees impossible value
- Rejects entire day's data
- Payment: $0

With spike detection:
- Flag 50 kWh as error
- Estimate correct value (5.0 kWh based on neighboring intervals)
- Submit corrected data
- Payment: Approved ✅
```

---

## 🔍 PART 12: VALIDATION CHECK #4 - TIME INTEGRITY

### What It Checks:
> Timestamps must be in correct sequence with 15-minute gaps

### Why It Matters:
Wrong timestamps = wrong billing period = no payment

---

### Simple Example - PASS ✅

```
Interval 1: 2026-04-05 18:00:00 ✅
Interval 2: 2026-04-05 18:15:00 ✅ (15 min later)
Interval 3: 2026-04-05 18:30:00 ✅ (15 min later)
Interval 4: 2026-04-05 18:45:00 ✅ (15 min later)

Gap between each: 15 minutes exactly
Result: ✅ PASS - Time integrity correct
```

---

### Simple Example - FAIL ❌

```
Interval 1: 2026-04-05 18:00:00 ✅
Interval 2: 2026-04-05 18:15:00 ✅
Interval 3: 2026-04-05 18:50:00 ❌ (35 min gap! Should be 18:30:00)
Interval 4: 2026-04-05 19:05:00 ❌ (Wrong gap)

Result: ❌ FAIL - Time gaps incorrect
Action: Flag for review
```

---

### Real-World Example - Timezone Error:

**Grid Event:** 6:00-8:00 PM **Pacific Time**

**Wrong Timezone:**
```
Data submitted with timestamps:
18:00:00 UTC (= 11:00 AM Pacific) ❌ WRONG!
18:15:00 UTC (= 11:15 AM Pacific) ❌ WRONG!

Utility checks: Event was 6-8 PM, but data shows 11 AM
Result: ❌ REJECTED - Wrong time period, no payment
```

**Correct Timezone:**
```
Data submitted with timestamps:
2026-04-05 18:00:00 PDT (= 01:00:00 UTC next day) ✅
2026-04-05 18:15:00 PDT (= 01:15:00 UTC next day) ✅

Utility checks: Event was 6-8 PM Pacific ✅
Result: ✅ APPROVED - Correct time period, payment processed
```

---

### Real-World Example - Clock Drift:

**Scenario: Device clock is off**

```
Actual time:     18:00:00
Device reports:  18:00:37 (37 seconds drift)

Over 96 intervals:
Drift accumulates: 37 sec × 96 = 59 minutes off!

Last interval shows: 11:59 PM instead of 11:00 PM
Result: ❌ FAIL - Intervals don't align to 15-minute boundaries
```

---

## 🔍 PART 13: VALIDATION CHECK #5 - METER IDENTITY

### What It Checks:
> Data is linked to correct site and battery (no mix-ups)

### Why It Matters:
Wrong site = payment goes to wrong customer, billing errors

---

### Simple Example - PASS ✅

**Enrollment Database:**
```
Site ID: SITE_12345
Battery ID: BATTERY_67890
Customer: John Smith
Address: 123 Main St, San Jose, CA
```

**Telemetry Data Received:**
```
Site ID: SITE_12345 ✅ (Matches enrollment)
Battery ID: BATTERY_67890 ✅ (Matches enrollment)
Timestamp: 2026-04-05 18:00:00
Energy: 2.5 kWh

Result: ✅ PASS - Meter identity correct
```

---

### Simple Example - FAIL ❌

**Enrollment Database:**
```
Site ID: SITE_12345
Battery ID: BATTERY_67890
```

**Telemetry Data Received:**
```
Site ID: SITE_12345 ✅
Battery ID: BATTERY_99999 ❌ (This battery doesn't exist at this site!)
Timestamp: 2026-04-05 18:00:00
Energy: 2.5 kWh

Result: ❌ FAIL - Meter identity mismatch
Action: Reject data - can't verify which battery provided energy
```

---

### Real-World Example - Mix-up Scenario:

**What Happened:**
```
Technician installed new battery at Site A
Accidentally configured it with Site B's ID in the system
```

**Impact:**
```
Site A (John Smith):
- Has battery installed ✅
- Battery discharges during event
- Data reports to Site B ❌
- John gets: $0 payment (no data linked to his site)

Site B (Jane Doe):
- No battery installed
- Receives data from Site A's battery ❌
- Jane gets: $50 payment (for battery she doesn't have!)
- Jane is confused: "I don't have a battery?"

Utility sees mismatch → Rejects both sites → No one gets paid

Meter Identity Check catches this error immediately!
```

---

### Real-World Example - Replacement Battery:

**Scenario: Battery replaced but ID not updated**

```
Original Battery: BATTERY_11111 (installed 2024, died 2025)
New Battery: BATTERY_22222 (installed 2026)

Enrollment Database (not updated):
Site: SITE_12345, Battery: BATTERY_11111 ❌ (Old battery!)

Telemetry from new battery:
Site: SITE_12345, Battery: BATTERY_22222 ✅ (New battery!)

Meter Identity Check:
BATTERY_22222 not in enrollment for SITE_12345 → ❌ FAIL

Result: Payment rejected until enrollment updated
Action: Update enrollment database with new battery ID
```

---

## 🔍 PART 14: VALIDATION CHECK #6 - HIGH/LOW USAGE (Future)

### What It Checks:
> Values are within normal historical range

### Why It Matters:
Detect unusual patterns that might indicate errors

---

### Simple Example:

**Historical Data for Site_12345:**
```
Typical discharge during events: 2-3 kWh per 15 min
Average: 2.5 kWh
Max ever seen: 4.0 kWh
```

**New Data Received:**
```
6:00 PM: 2.8 kWh ✅ (Normal range)
6:15 PM: 15.0 kWh ❌ (Way above max! Suspicious!)
6:30 PM: 2.6 kWh ✅ (Back to normal)

Result: Flag 6:15 PM for review
Likely: Sensor spike or data error
```

**Note:** This check is "TBD" (To Be Determined) - might implement later

---

## 🔍 PART 15: VALIDATION CHECK #7 - CHANNEL MAPPING (Future)

### What It Checks:
> Power flow direction is correct (import vs export, charge vs discharge)

### Why It Matters:
Reversed channels = wrong billing

---

### Simple Example:

**Correct Channel Mapping:**
```
Battery Discharging (helping grid):
- Channel A: Discharge = 2.5 kWh ✅ (Positive value)
- Channel B: Charge = 0 kWh ✅ (Zero)
```

**Wrong Channel Mapping:**
```
Battery Discharging (helping grid):
- Channel A: Discharge = 0 kWh ❌ (Should be positive!)
- Channel B: Charge = 2.5 kWh ❌ (Wrong direction!)

Values swapped! Battery is discharging but reporting as charging!
```

**Note:** This check is "TBD" - might implement later

---

## 📊 SUMMARY - ALL 7 VALIDATION CHECKS

| # | Check | What It Catches | Priority | Status |
|---|-------|-----------------|----------|--------|
| 1 | **Interval Completeness** | Missing intervals | High | ✅ Implement |
| 2 | **Sum Check** | Energy balance errors | High | ✅ Implement |
| 3 | **Spike Detection** | Impossible values | High | ✅ Implement |
| 4 | **Time Integrity** | Wrong timestamps | High | ✅ Implement |
| 5 | **Meter Identity** | Wrong site/battery IDs | High | ✅ Implement |
| 6 | **High/Low Usage** | Unusual patterns | Medium | TBD (Future) |
| 7 | **Channel Mapping** | Reversed flows | Medium | TBD (Future) |

---

## 🎯 YOUR NEXT SPRINT TASKS (Likely)

Based on this document, you'll probably:

**Task 1:** Implement Interval Completeness Check
- Count intervals per day per site
- Flag sites with missing intervals
- Handle DST edge cases

**Task 2:** Implement Sum Check
- Calculate energy IN vs energy OUT
- Flag imbalanced intervals
- Allow small tolerance for rounding

**Task 3:** Implement Spike Detection
- Check values against battery capacity
- Flag impossible values
- Create alerts for review

**Task 4:** Implement Time Integrity Check
- Verify 15-minute gaps between intervals
- Check timezone consistency
- Validate timestamp sequences

**Task 5:** Implement Meter Identity Check
- Cross-check site/battery IDs against enrollment
- Flag orphaned or mismatched data
- Validate before processing

---

**Status:** All Main Sections Complete ✅
**Document Ready:** For next sprint reference

**You now understand:**
- ✅ Why validation matters (payments depend on it)
- ✅ What data is collected (6 input types)
- ✅ What checks to implement (5 main validation rules)
- ✅ How each check works (with real examples)
- ✅ Business impact (revenue loss if validation fails)






