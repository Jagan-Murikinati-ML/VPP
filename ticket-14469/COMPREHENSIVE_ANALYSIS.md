# Ticket 14469 - Comprehensive Analysis

**Ticket:** SPIKE: Telemetry backfill for SQMD data  
**Assigned to:** Jagan Murikinati + Sanjeev Lakkaraju  
**Date:** April 2026  
**Status:** Analysis Phase

---

## 🎯 **EXECUTIVE SUMMARY:**

This ticket is part of a larger initiative to create **Settlement Quality Meter Data (SQMD)** for utility billing. The work involves:

1. **Nightly Batch Job:** Daily pipeline from raw telemetry → settlement-quality data
2. **Bi-weekly Updates:** Refresh historical data with OEM corrections
3. **Backfill Investigation:** How to fill historical data gaps

**Business Impact:** Ensures accurate utility settlement = Correct payments = Revenue protection

---

## 📊 **THE BIG PICTURE - DATA FLOW:**

```
┌──────────────────────────────────────────────────────┐
│  STEP 1: PHYSICAL DEVICES                            │
│  Tesla batteries, Enphase solar, SolarEdge inverters │
│  Generate power data every 15 minutes                │
└──────────────────────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────┐
│  STEP 2: OEM CLOUD STORAGE                           │
│  Tesla API, Enphase API, SolarEdge API, etc.         │
│  Store telemetry data in vendor clouds               │
└──────────────────────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────┐
│  STEP 3: CONNECTORS (Already built)                  │
│  Automated pipelines pulling from OEM APIs           │
│  Run every 15 minutes                                │
│  Subject to API rate limits                          │
└──────────────────────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────┐
│  STEP 4: silverCommDataSite (Kusto table)            │
│  Raw telemetry data - ALL fields from OEMs          │
│  Issues: Gaps, duplicates, bad values, 50+ columns  │
└──────────────────────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────┐
│  STEP 5: NIGHTLY BATCH JOB ⭐ YOUR TASK #1           │
│  Extract relevant fields only                        │
│  Basic data cleaning                                 │
│  Schedule: Every night at 2 AM                       │
└──────────────────────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────┐
│  STEP 6: sqTelemetry (Kusto table)                   │
│  Settlement-quality data - Only ~10 key fields       │
│  Cleaner but may still have some gaps               │
└──────────────────────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────┐
│  STEP 7: BI-WEEKLY UPDATE ⭐ YOUR TASK #2            │
│  Re-fetch last 14 days from OEM APIs                │
│  Update corrections in sqTelemetry                   │
│  Schedule: Every 2 weeks (1st & 15th)               │
└──────────────────────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────┐
│  STEP 8: VALIDATION (Sachin's task)                  │
│  Apply SQMD validation rules                         │
│  Label: Valid / Suspect / Invalid                    │
└──────────────────────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────┐
│  STEP 9: ESTIMATION & EDITING (TBD - Future)         │
│  Fix invalid data                                    │
│  Estimate missing values                             │
└──────────────────────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────┐
│  STEP 10: VERSIONING                                 │
│  Create Version 1, 2, 3... as corrections made       │
└──────────────────────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────┐
│  STEP 11: SUBMIT TO UTILITY                          │
│  Send to PG&E, SCE, SDG&E for payment               │
│  Revenue: Millions of dollars annually               │
└──────────────────────────────────────────────────────┘
```

---

## 📋 **KEY CONCEPTS EXPLAINED:**

### **1. Settlement**

**What it means:**
- **Settlement** = Utility paying Q CELLS for battery services
- **NOT** about "settling disputes" or "settling data"

**Example:**
```
April 5, 2026 - Grid Peak Event (6-9 PM)

Q CELLS batteries discharged 50,000 kWh to help grid
Utility (PG&E) owes payment for this service

Settlement process:
1. Q CELLS sends telemetry data (proof of discharge)
2. PG&E validates data meets SQMD standards
3. PG&E calculates payment: 50,000 kWh × $2/kWh = $100,000
4. PG&E pays Q CELLS $100,000
5. Q CELLS shares revenue with battery owners

Missing data = Cannot prove discharge = Lost $100,000! ❌
```

---

### **2. Utility**

**What it means:**
- **Utility** = Electric company that owns/operates power grid
- **NOT** government (but heavily regulated)
- **Examples:** PG&E, SCE, SDG&E in California

**What they do:**
1. Deliver electricity to homes/businesses
2. Manage power grid infrastructure
3. Run programs like LEAP/DSGS
4. Pay for grid services (like battery discharge)

---

### **3. Connectors**

**What they are:**
- **Connector** = Automated pipeline that pulls data from OEM APIs
- **Already built** (not your job to create)
- **Run continuously** (every 15 minutes)

**Example - Tesla Connector:**
```python
# Simplified pseudo-code
while True:
    # Every 15 minutes:
    data = tesla_api.get_battery_telemetry(last_15_minutes)
    kusto.insert_into_silverCommDataSite(data)
    sleep(15 * 60)  # Wait 15 minutes
```

**Each OEM has its own connector:**
- Tesla Connector
- Enphase Connector  
- SolarEdge Connector
- Qcells Connector
- Solax Connector

---

### **4. SQMD (Settlement Quality Meter Data)**

**What it means:**
- **Standard** created by CPUC (California Public Utilities Commission)
- **Purpose:** Define "good enough to bill" energy data
- **Requirements:** Complete, accurate, validated intervals

**Think of it like:**
```
Regular telemetry = Draft document with typos, missing pages
SQMD = Final polished document ready for official use
```

---

### **5. Backfill**

**What it means:**
- **Backfill** = Fill in missing historical data

**Example:**
```
silverCommDataSite data for Site 400012345:

April 1: ✅ 96 intervals (complete day)
April 2: ❌ 0 intervals (MISSING - connector was down!)
April 3: ✅ 96 intervals (complete day)

Backfill process:
1. Identify gap: April 2 missing
2. Check if Tesla API still has April 2 data
3. Re-fetch April 2 from Tesla API
4. Insert into silverCommDataSite
5. Copy to sqTelemetry
6. Now April 2 is complete! ✅
```

---

## 🎯 **YOUR TWO TASKS:**

### **TASK #1: NIGHTLY BATCH JOB**

**What:** Extract yesterday's data from silverCommDataSite → sqTelemetry

**When:** Every night (automated)

**Why:** Settlement only needs specific fields, not all 50+ raw fields

**Implementation:**
```kql
// Pseudo-code - Runs every night at 2 AM

let yesterday_start = now() - 1d | bin(1d);  // Yesterday 00:00
let yesterday_end = now() | bin(1d);          // Today 00:00

.set-or-append sqTelemetry <|
silverCommDataSite
| where sourceTimestamp >= yesterday_start 
    and sourceTimestamp < yesterday_end
| where siteId in (enrolled_sites)  // Only LEAP/DSGS enrolled sites
| project 
    siteId,
    meterId,
    timestamp = sourceTimestamp,
    battery_discharge_kwh = battery_200_IncWhImp / 1000,
    battery_charge_kwh = battery_200_IncWhExp / 1000,
    battery_soc = battery_soc,
    solar_production_kwh = solar_kwh,
    grid_import_kwh = grid_import,
    grid_export_kwh = grid_export
    // Only ~10 key fields, not all 50+
```

**Fields to extract (examples):**
```
FROM silverCommDataSite (50+ columns):
✅ siteId → Keep
✅ meterId → Keep  
✅ sourceTimestamp → Keep (rename to timestamp)
✅ battery_200_IncWhImp → Keep (convert to kWh, rename)
✅ battery_200_IncWhExp → Keep (convert to kWh, rename)
✅ battery_soc → Keep
✅ solar_production → Keep
❌ inverter_temperature → DROP (not needed for settlement)
❌ grid_voltage → DROP
❌ grid_frequency → DROP
... (drop 40+ other technical fields)

TO sqTelemetry (~10 columns):
Only settlement-relevant metrics
```

---

### **TASK #2: BI-WEEKLY UPDATE**

**What:** Re-fetch last 14 days from OEM APIs to capture corrections

**When:** Every 2 weeks (1st and 15th of month)

**Why:** OEMs sometimes fix errors days/weeks later

**Example scenario:**
```
Week 1 (April 1):
Tesla battery reports: 5.2 kWh discharged
Stored in silverCommDataSite and sqTelemetry

Week 2 (April 8):  
Tesla discovers sensor calibration error
Tesla fixes their database: 5.2 kWh → 5.8 kWh (corrected!)
But our database still shows 5.2 kWh (old value!) ❌

Week 3 (April 15 - Bi-weekly update):
Re-fetch last 14 days (April 1-14) from Tesla API
Discover April 1 changed: 5.2 → 5.8 kWh
Update sqTelemetry: Set April 1 = 5.8 kWh ✅
Now our data matches Tesla's corrected value!

Settlement submission:
Send corrected 5.8 kWh (not wrong 5.2 kWh)
Accurate payment calculation ✅
```

**Implementation approach:**
```kql
// Pseudo-code - Runs every 2 weeks

let lookback_start = now() - 14d;
let lookback_end = now();

// Step 1: Re-fetch from silverCommDataSite 
// (Connector already updated it from OEM APIs)
let refreshed_data = silverCommDataSite
    | where sourceTimestamp >= lookback_start 
        and sourceTimestamp < lookback_end
    | where siteId in (enrolled_sites)
    | project [same fields as nightly job];

// Step 2: Merge with existing sqTelemetry
.set-or-replace sqTelemetry <|
sqTelemetry
| where timestamp < lookback_start  // Keep old data as-is
| union (refreshed_data)             // Add refreshed 14 days
```

---

## ⚠️ **CRITICAL CONSTRAINT: API RATE LIMITS**

### **The Problem:**
OEM APIs have limits on how many calls you can make.
Bi-weekly updates require re-fetching data = More API calls = Risk hitting limits!

---

## 📊 **RATE LIMIT ANALYSIS - BY OEM:**

### **Summary Table:**

| OEM | Rate Limit | Historical Data Range | Real-time Usage | Backfill Capacity | Status |
|-----|------------|----------------------|-----------------|-------------------|---------|
| **Tesla** | 300 calls/min | 20 days per call | 1 call for all sites | 144,000 sites/day | ✅ **EXCELLENT** |
| **Enphase** | No limit | N/A | N/A | Unlimited | ✅ **EXCELLENT** |
| **Qcells** | N/A | N/A | N/A | No issues | ✅ **GOOD** |
| **SolarEdge** | 300 calls/site/day | 1 month per call | 288 calls/site/day | 4 sites/day | ⚠️ **LIMITED** |
| **Solax** | 100 calls/min | 1 day per call | Most of quota used | Very limited | ❌ **PROBLEM** |

---

### **1. TESLA - EXCELLENT ✅**

**API Limits:**
```
300 API calls per minute
Each call can fetch 20 days of data
```

**Real-time Telemetry Usage:**
```
Special feature: One API call retrieves ALL sites in "monitoring group"
Example: 1 call = data for 5,000 Tesla sites!

Real-time consumption: 1 call per 15 minutes
Daily usage: 96 calls/day (not per site, total!)

API budget remaining: 300 calls/min - negligible real-time = Huge capacity!
```

**Backfill Capacity Calculation:**
```
Goal: Backfill 60 days of historical data per site

Step 1: How many calls per site?
- Each call fetches 20 days
- Need 60 days
- Calls needed: ceil(60 / 20) = 3 calls per site

Step 2: How many sites per minute?
- Rate limit: 300 calls/min
- Calls per site: 3
- Sites per minute: 300 / 3 = 100 sites/min

Step 3: Daily backfill capacity:
- Per minute: 100 sites
- Per hour: 100 × 60 = 6,000 sites
- Per day: 6,000 × 24 = 144,000 sites/day! 🚀

Current Tesla sites: ~2,000 sites
Backfill time: 2,000 / 144,000 = 0.014 days ≈ 20 minutes!
```

**Conclusion:** ✅ **Tesla rate limits are NOT a problem!**

**Example:**
```
Scenario: Need to backfill 60 days for 2,000 Tesla sites

Process:
- 3 API calls per site × 2,000 sites = 6,000 total calls
- At 300 calls/min = 20 minutes total time
- Can easily do this during bi-weekly update window

✅ NO ISSUES!
```

---

### **2. ENPHASE - EXCELLENT ✅**

**API Limits:**
```
No rate limit!
```

**Real-time Telemetry Usage:**
```
No constraints
```

**Backfill Capacity:**
```
Unlimited!
Can fetch as much historical data as needed
```

**Conclusion:** ✅ **Enphase is the easiest - no rate limit concerns!**

---

### **3. QCELLS - GOOD ✅**

**API Limits:**
```
Not specified (likely internal API, not third-party)
```

**Real-time Telemetry Usage:**
```
N/A (Q CELLS' own system)
```

**Backfill Capacity:**
```
Assumed sufficient since it's internal API
```

**Conclusion:** ✅ **Qcells should not have rate limit issues**

---

### **4. SOLAREDGE - LIMITED ⚠️**

**API Limits:**
```
300 API calls per site per day

Important: This is PER SITE, not total!
Example: 100 SolarEdge sites = 100 × 300 = 30,000 calls/day budget
```

**Real-time Telemetry Usage:**
```
Special approach: Grid services sites use WebSockets (not REST API)
This frees up the 300 API calls for other uses

Real-time usage:
- Every 15 minutes = 96 pulls/day
- 3 API calls per pull
- Total: 96 × 3 = 288 calls/site/day

Budget used: 288 out of 300 calls
Remaining: 300 - 288 = 12 calls/site/day
```

**Backfill Capacity Calculation:**
```
Available: 12 calls/site/day
Each call fetches: 1 month of data

Scenario 1: Backfill 30 days (1 month)
- Calls needed: 1 call (fetches 1 month)
- Can backfill: 12 sites/day

Scenario 2: Backfill 60 days (2 months)
- Calls needed: 2 calls (2 × 1 month)
- Can backfill: 12 / 2 = 6 sites/day

Scenario 3: Backfill 90 days (3 months)
- Calls needed: 3 calls (3 × 1 month)
- Can backfill: 12 / 3 = 4 sites/day

Current SolarEdge sites: ~1,500 sites
Time to backfill all (60 days): 1,500 / 6 = 250 days! ⚠️
```

**Conclusion:** ⚠️ **SolarEdge rate limits are TIGHT!**
- Can only backfill ~6 sites per day (for 60 days of data)
- Full fleet backfill would take months!
- Bi-weekly updates feasible but slow

**Mitigation:**
```
Option 1: Prioritize critical sites
- Backfill highest revenue sites first
- Leave lower priority sites for later

Option 2: Spread over time
- Don't backfill all sites at once
- Continuous rolling backfill over months

Option 3: Reduce historical range
- Instead of 60 days, backfill 30 days
- Doubles capacity: 12 sites/day instead of 6
```

**Example:**
```
Bi-weekly update (every 2 weeks):
- Need to refresh 14 days of data
- Calls per site: 1 call (covers 30 days, includes the 14 needed)
- Sites updated per day: 12 sites

Over 14 days: 12 × 14 = 168 sites can be refreshed

Current SolarEdge sites: ~1,500
Full refresh time: 1,500 / 168 = 9 bi-weekly cycles ≈ 18 weeks ≈ 4.5 months

⚠️ Cannot refresh all sites every 2 weeks!
Need rotation strategy: Different subset each bi-weekly cycle
```

---

### **5. SOLAX - PROBLEM ❌**

**API Limits:**
```
100 API calls per minute (total, not per site)
Each call fetches: 1 day of data only
```

**Real-time Telemetry Usage:**
```
Real-time connector uses most of the 100 calls/min budget
Very little remaining for backfill
```

**Backfill Capacity:**
```
Extremely limited!

Example calculation:
- Rate limit: 100 calls/min
- Real-time usage: ~90 calls/min (estimated)
- Available for backfill: ~10 calls/min
- Each call = 1 day of data

To backfill 60 days for 1 site:
- Need 60 calls (1 day per call)
- At 10 calls/min = 6 minutes per site
- Per hour: 60 min / 6 = 10 sites
- Per day: 10 × 24 = 240 sites (max)

Current Solax sites: ~500 sites
Time to backfill all: 500 / 240 = 2+ days (if no real-time interference)

But reality: Real-time has priority, so backfill gets even less
Actual capacity: Maybe 50-100 sites/day? ⚠️
```

**Conclusion:** ❌ **Solax rate limits are CRITICAL BLOCKER!**

**From design document:**
> "Solax does not have sufficient rate limits to perform these bi-weekly updates, unless we negotiate higher limits with Solax."

**Impact:**
```
Bi-weekly updates:
✅ Tesla - Supported
✅ Enphase - Supported
✅ Qcells - Supported
⚠️ SolarEdge - Partially supported (slow rotation)
❌ Solax - NOT SUPPORTED (rate limit too low)

Result: Solax sites will have LESS ACCURATE settlement data!
```

**Mitigation:**
```
Option 1: Negotiate with Solax
- Request higher rate limits
- Explain business need (settlement accuracy)
- May require paid tier upgrade

Option 2: Exclude Solax from bi-weekly updates
- Accept that Solax data won't get OEM corrections
- Higher risk of inaccurate settlement data
- Document as known limitation

Option 3: Manual one-time backfill
- Don't do bi-weekly updates for Solax
- Do manual quarterly backfill instead
- Less frequent but better than nothing
```

---

## 🎯 **RATE LIMIT IMPACT ON YOUR TASKS:**

### **Task #1: Nightly Batch Job**
**Impact:** ✅ **NONE!**

**Why:**
- Nightly job reads from silverCommDataSite (already in database)
- Does NOT call OEM APIs
- No rate limits apply
- Safe to process all sites every night

---

### **Task #2: Bi-weekly Update**
**Impact:** ⚠️ **SIGNIFICANT!**

**Why:**
- Bi-weekly update requires re-fetching from OEM APIs
- Rate limits constrain how many sites can be refreshed

**Strategy by OEM:**

**Tesla:** ✅ Full fleet update every 2 weeks (no issues)
```
All ~2,000 Tesla sites refreshed in ~20 minutes
```

**Enphase:** ✅ Full fleet update every 2 weeks (no issues)
```
All Enphase sites refreshed (no limit)
```

**Qcells:** ✅ Full fleet update every 2 weeks (assumed OK)
```
All Qcells sites refreshed (internal API)
```

**SolarEdge:** ⚠️ Partial update, rotation strategy
```
Week 1 (Bi-weekly run 1): Update sites 1-168
Week 3 (Bi-weekly run 2): Update sites 169-336
Week 5 (Bi-weekly run 3): Update sites 337-504
...
Week 19 (Bi-weekly run 10): Update sites 1333-1500

Each site gets refreshed every ~20 weeks (5 months)
Not ideal, but better than nothing
```

**Solax:** ❌ NO bi-weekly updates
```
Exclude from bi-weekly process
Document as limitation
Consider quarterly manual backfill instead
```

---

## 📋 **DECISION MATRIX:**

### **For Bi-weekly Updates:**

| OEM | Update Frequency | Sites per Update | Full Fleet Refresh Time |
|-----|------------------|------------------|------------------------|
| Tesla | Every 2 weeks | ALL (~2,000) | 20 minutes |
| Enphase | Every 2 weeks | ALL | Fast |
| Qcells | Every 2 weeks | ALL | Fast |
| SolarEdge | Every 2 weeks | 168 sites (rotating) | 4.5 months for full rotation |
| Solax | NOT SUPPORTED | 0 | N/A |

---

## 🎯 **QUESTIONS TO CLARIFY IN YOUR CALL:**

### **1. Bi-weekly Update Scope:**
```
Q: "For bi-weekly updates, do we re-fetch from OEM APIs or from silverCommDataSite?"

Scenario A: Re-fetch from OEM APIs
→ Rate limits apply
→ Need rotation strategy for SolarEdge
→ Cannot support Solax

Scenario B: Read from silverCommDataSite (connectors already updated it)
→ No rate limits apply
→ Can update all sites
→ Assumes connectors handle OEM refresh

Which scenario is it?
```

### **2. SolarEdge Strategy:**
```
Q: "SolarEdge can only refresh ~168 sites every 2 weeks. Is this acceptable?"

Option A: Rotate through all sites (4.5 month cycle)
→ Each site refreshed every ~5 months
→ Less frequent but covers everyone eventually

Option B: Prioritize high-value sites
→ Top 168 revenue-generating sites get bi-weekly updates
→ Others get quarterly or never

Which approach should we use?
```

### **3. Solax Handling:**
```
Q: "Solax rate limits are insufficient. What's the plan?"

Option A: Exclude Solax from bi-weekly updates entirely
→ Document as limitation
→ Accept lower data quality for Solax sites

Option B: Quarterly manual backfill for Solax
→ Do a big one-time refresh every 3 months
→ Better than nothing but not bi-weekly

Option C: Negotiate with Solax for higher limits
→ Wait for business team to get better API access
→ Delay Solax implementation until resolved

Which path?
```

### **4. Implementation Approach:**
```
Q: "Should nightly job and bi-weekly update be KQL or Python?"

KQL Pros:
- Native to Kusto/Fabric
- Fast for large data operations
- Easy to schedule in Fabric

Python Pros:
- More flexible error handling
- Can integrate with external systems
- Better for complex API orchestration

Recommendation?
```

---

## 📊 **REAL-WORLD EXAMPLES:**

### **Example 1: Tesla Bi-weekly Update**

**Scenario:**
```
Current date: April 15, 2026 (bi-weekly update day)
Need to refresh: April 1-14 data (14 days)
Tesla sites: 2,000 sites
```

**Process:**
```
Step 1: Check if connector already updated silverCommDataSite
- If YES: Skip to Step 3 ✅
- If NO: Proceed to Step 2

Step 2: Re-fetch from Tesla API (if needed)
- Tesla API call: Get April 1-14 data for all 2,000 sites
- Calls needed: 1 call (Tesla's group API fetches all sites together!)
- Time: < 1 minute
- Update silverCommDataSite with corrections

Step 3: Refresh sqTelemetry
- Read refreshed April 1-14 data from silverCommDataSite
- Compare with existing sqTelemetry
- Update changed values
- Time: ~5-10 minutes

Total time: ~10 minutes for 2,000 sites ✅
```

---

### **Example 2: SolarEdge Bi-weekly Update**

**Scenario:**
```
Current date: April 15, 2026 (bi-weekly update day)
Need to refresh: April 1-14 data (14 days)
SolarEdge sites: 1,500 total
Daily API budget per site: 12 calls
Bi-weekly period: 14 days
```

**Calculation:**
```
Available calls per site during 14 days:
- Per day: 12 calls
- 14 days: 12 × 14 = 168 calls total

Each site needs: 1 call (fetches 30 days, covers the 14 needed)

Sites that can be refreshed: 168 sites (out of 1,500)

Percentage: 168 / 1,500 = 11.2%
```

**Rotation Strategy:**
```
Bi-weekly Run 1 (April 1-14):   Sites 1-168
Bi-weekly Run 2 (April 15-28):  Sites 169-336
Bi-weekly Run 3 (April 29-May 12): Sites 337-504
...
Bi-weekly Run 9 (July 1-14):    Sites 1333-1500

Complete cycle: 9 bi-weekly runs = 18 weeks = 4.5 months

Result: Each SolarEdge site gets refreshed once every 4.5 months
Not ideal, but constrained by API limits ⚠️
```

---

### **Example 3: Backfill Scenario**

**Scenario:**
```
Problem discovered: March 15-20 data missing for 100 sites (connector was down)
OEMs: 60 Tesla, 30 SolarEdge, 10 Enphase
Need to backfill: 6 days of missing data
```

**Tesla Backfill (60 sites):**
```
Data range: 6 days
Tesla API: Each call fetches 20 days (covers the 6 needed)
Calls needed: 1 call per site × 60 sites = 60 calls
Rate limit: 300 calls/min
Time: 60 / 300 = 0.2 minutes = 12 seconds! ✅

Result: All 60 Tesla sites backfilled in 12 seconds
```

**Enphase Backfill (10 sites):**
```
No rate limit!
Fetch as fast as possible
Time: ~1 minute ✅

Result: All 10 Enphase sites backfilled easily
```

**SolarEdge Backfill (30 sites):**
```
Data range: 6 days
SolarEdge API: Each call fetches 30 days (covers the 6 needed)
Calls needed: 1 call per site × 30 sites = 30 calls
Daily budget per site: 12 calls (after real-time usage)

Can backfill per day: 12 sites
Time to backfill 30 sites: 30 / 12 = 2.5 days ⚠️

Result: SolarEdge backfill takes 3 days (slower but feasible)
```

**Total Backfill Time:**
```
Tesla: 12 seconds ✅
Enphase: 1 minute ✅
SolarEdge: 3 days ⚠️

Bottleneck: SolarEdge rate limits
```

---

## ✅ **SUMMARY - YOUR UNDERSTANDING VALIDATED:**

| Topic | Your Understanding | ✅/❌ | Final Clarification |
|-------|-------------------|-------|---------------------|
| **Backfill** | Store missing data in gaps | ✅ | Correct! |
| **Settlement** | Payment from utility | ✅ | Utility = PG&E/SCE (electric companies) |
| **Bi-weekly refetch** | Get updated data from source | ✅ | Fetch all 14 days, update only changes |
| **Connectors** | Pipelines from OEM APIs | ✅ | Already built, not your job |
| **Utility** | "Who uses power" | ⚠️ | Actually: Who PAYS for grid services |
| **Data issues** | Gaps, duplicates, bad values | ✅ | Correct! |
| **Nightly job** | silverCommDataSite → sqTelemetry | ✅ | Only 10 key fields, not all 50+ |
| **Bi-weekly updates** | Update sqTelemetry with OEM corrections | ⚠️ | Need to clarify who updates silverCommDataSite |
| **Rate limits** | Constraint on API calls | ✅ | Major issue for SolarEdge & Solax |
| **Solax exclusion** | Cannot do bi-weekly | ✅ | Confirmed: Rate limits too low |
| **KQL vs Python** | Not sure which to use | ⚠️ | Discuss with team, likely KQL |

---

## 🎯 **YOUR ACTION ITEMS:**

### **Before Your Next Call:**

1. ✅ **Review this analysis document**
2. ✅ **Prepare questions** (listed in "Questions to Clarify" section above)
3. ✅ **Understand rate limit constraints** (you now do!)
4. ✅ **Think through bi-weekly update strategy** for each OEM

### **During Your Call:**

1. **Clarify scope:**
   - "For bi-weekly updates, do we call OEM APIs or read from silverCommDataSite?"
   - "What's the rotation strategy for SolarEdge?"
   - "What's the plan for Solax?"

2. **Confirm implementation approach:**
   - "Should we use KQL or Python for nightly job?"
   - "Same question for bi-weekly updates?"

3. **Understand backfill SPIKE:**
   - "For the SPIKE ticket, what specific backfill scenario should I investigate?"
   - "Is this about one-time historical backfill or ongoing bi-weekly?"

### **After Your Call:**

1. **Document decisions** from the call
2. **Create implementation plan** for nightly job
3. **Create implementation plan** for bi-weekly updates
4. **Start coding** (after approval)

---

## 📁 **FILES IN THIS TICKET:**

```
ticket-14469/
├── ticket.md                          (Ticket title)
├── design-document.md                 (Naveen's design proposal)
├── oem-rate-limit-api-calls.md       (Rate limit details)
├── Data_Validation_Rules_SIMPLE_GUIDE.md (SQMD validation rules)
└── COMPREHENSIVE_ANALYSIS.md          (This document) ⭐
```

---

## 🎯 **FINAL SUMMARY:**

**What you're building:**
1. **Nightly batch job:** Raw telemetry → Settlement-quality data (daily pipeline)
2. **Bi-weekly updates:** Refresh with OEM corrections (quality improvement)
3. **Backfill investigation:** How to fill historical gaps (SPIKE research)

**Why it matters:**
- Ensures accurate utility settlement
- Protects millions in annual revenue
- Enables correct payments to battery owners

**Key challenges:**
- ✅ Tesla, Enphase, Qcells: No rate limit issues
- ⚠️ SolarEdge: Tight limits, need rotation strategy
- ❌ Solax: Cannot support bi-weekly updates

**Your role:**
- Build data pipelines (ETL processes)
- Work with Sanjeev on implementation
- Navigate rate limit constraints

**You're ready for the discussion!** 🚀

---

**Questions? Review this document before your call and you'll be fully prepared!** 💪

