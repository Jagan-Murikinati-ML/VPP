# Juan's LEAP Reporting Script - Analysis & Understanding

**Date:** April 9, 2026  
**Your Call with Juan:** Today  
**Script File:** `Leap Reporting KQL.txt`  
**Purpose:** Extract 15-minute battery interval data for LEAP/DSGS programs

---

## 📋 EXECUTIVE SUMMARY

**What the script does:**
1. Gets site list from Asset Registry (with LEAP contracts)
2. Pulls battery telemetry data for date range
3. Creates 15-minute interval bins
4. Formats output to match LEAP template
5. Exports CSV for submission to LEAP program

**Date range in script:** October 31 - November 1, 2025 (for testing)

**Your task:** Change to April 1-10, 2026

---

## 🗺️ LINE-BY-LINE DETAILED EXPLANATION

---

## 📖 LINES 1-20: CONFIGURATION & DATA CLEANUP

### **LINE 1: Test Site Array (Empty = All Sites)**
```kql
let testsite = dynamic([]);
```

**What it does:**
- Creates empty dynamic array
- **Empty array = Process ALL sites** ✅
- **Not empty = Process only those specific sites** (for testing)

**Your understanding:** ✅ **CORRECT!**
- For 5k or 7.7k sites, you DON'T need to pass all site IDs in this array
- Leave it empty: `dynamic([])` to process all sites
- This is ONLY for testing specific sites during development

---

### **LINES 2-4: Commented Test Examples (IGNORE)**
```kql
// let testsite = dynamic([400000062,400000181,...]); // Test 8 sites
// let testsite = dynamic([400018050]);                // Test 1 site
// let testsite = dynamic([400011870]);                // Specific problematic site
```

**What it is:**
- Juan's testing history (commented out)
- Examples of testing specific sites during development
- **You:** Ignore these lines ✅

---

### **LINES 5-6: DATE RANGE (WHAT YOU WILL CHANGE)**
```kql
let startTime = datetime(10/31/2025 00:00:00);
let endTime   = datetime(11/01/2025 00:00:00);
```

**What it does:**
- Defines extraction date range
- Currently: Oct 31 - Nov 1, 2025 (1 day for testing)

**What you'll change to:**
```kql
let startTime = datetime(4/1/2026 00:00:00);
let endTime   = datetime(4/11/2026 00:00:00);  // 4/11 to include all of 4/10
```

**Why 4/11?** To include entire day of 4/10 (up to 4/10 23:59:59)

---

### **LINES 7-14: BAD DATA FILTER**
```kql
let recordsToRemove =
    silverCommDataSite
    | where 1==1
        // and siteId in (testsite)
        and sourceTimestamp between (datetime(9/30/2025 00:00:00) .. datetime(11/6/2025 00:00:00))
        and (battery_200_IncWhExp >= 7500
          or battery_200_IncWhExp < 0
          or battery_200_IncWhImp >= 7500
          or battery_200_IncWhImp < 0)
    | project siteId, sourceTimestamp, battery_200_IncWhExp, battery_200_IncWhImp
;
```

**Line-by-line breakdown:**

**Line 7:** `let recordsToRemove =`
- Creates variable to store bad/invalid records

**Line 8:** `silverCommDataSite`
- Table containing battery telemetry data

**Line 9:** `| where 1==1`
- **Your question:** Why `1==1`?
- **Answer:** Coding trick! Always evaluates to TRUE
- **Purpose:** Makes it easy to comment/uncomment other filter lines
- **Example:**
  ```kql
  | where 1==1              // Always true (does nothing)
      // and siteId in (...)  // Can easily comment out filters
      and sourceTimestamp ...  // Easier to manage multiple AND conditions
  ```
  Without `1==1`, you'd need to manage which line has `where` vs `and`

**Line 10:** `// and siteId in (testsite)`
- Commented out (not active)
- If active, would only remove bad records for test sites
- Currently removes bad records for ALL sites ✅

**Line 11:** `and sourceTimestamp between (datetime(9/30/2025 ...) .. datetime(11/6/2025 ...))`
- **Your question:** Why not use `startTime` and `endTime` variables?
- **Answer:** Juan wanted a WIDER date range for bad data detection
- **Logic:**
  - Data extraction: Oct 31 - Nov 1 (1 day)
  - Bad data check: Sept 30 - Nov 6 (38 days!)
  - **Why?** Catch bad data from days before/after to prevent it from affecting calculations
- **For your April 1-10 extraction:**
  ```kql
  and sourceTimestamp between (datetime(3/25/2026 ...) .. datetime(4/15/2026 ...))
  // Check ~1 week before and after your actual date range
  ```

**Lines 12-13:** Battery value validation
```kql
and (battery_200_IncWhExp >= 7500 or battery_200_IncWhExp < 0
  or battery_200_IncWhImp >= 7500 or battery_200_IncWhImp < 0)
```
- **Your understanding:** ✅ **CORRECT!** Valid range is 0-7500 Wh
- **Battery fields:**
  - `battery_200_IncWhExp`: Energy **exported/discharged** (Wh)
  - `battery_200_IncWhImp`: Energy **imported/charged** (Wh)
- **Invalid if:**
  - Value >= 7500 Wh (too high - sensor error)
  - Value < 0 (negative - impossible!)
- **Why 7500?** Typical 15-min interval shouldn't exceed ~2 kWh for residential batteries

**Line 14:** `| project siteId, sourceTimestamp, battery_200_IncWhExp, battery_200_IncWhImp`
- **Your understanding:** ✅ **CORRECT!**
- Selects only needed columns
- Result: List of bad records to exclude later

**What happens to these records?**
- They are **removed** at line 87: `| join kind=leftanti (recordsToRemove)`
- **leftanti join** = Keep records that DON'T match (exclude bad data)

---

### **LINES 15-17: COMMENTED TESTING CODE (IGNORE)**
```kql
// recordsToRemove | extend extendingToCheck = 'whatRecordsAreRemoved' ...
// let startTime = startofmonth(datetime_add("month", -1, now()));
// let endTime = endofmonth(datetime_add("month", -1, now()));
```

**What it is:**
- Juan's testing/debugging code
- Line 15: Would show which records are being removed
- Lines 16-17: Dynamic date calculation (previous month)
- **You:** Ignore these ✅

---

### **LINE 18: THE TIME BACKBONE (15-MIN INTERVALS)**
```kql
let allBins = range bin_base from startTime to endTime step 15m;
```

**What it does:**
- Creates a table with ONE column: `bin_base`
- Contains every 15-minute interval between startTime and endTime

**Example for your April 1-10 dates:**
```
bin_base
------------------------
2026-04-01 00:00:00.000
2026-04-01 00:15:00.000
2026-04-01 00:30:00.000
2026-04-01 00:45:00.000
2026-04-01 01:00:00.000
...
2026-04-10 23:30:00.000
2026-04-10 23:45:00.000

Total rows: 10 days × 4 intervals/hour × 24 hours = 960 intervals
```

**Why is this important?**
- **Foundation for ALL data!**
- Even if battery has no data for a specific 15-min interval, this ensures the interval exists in output
- Missing data → Shows as "Null" in final CSV
- LEAP/DSGS requires complete intervals (no gaps)

**Juan's comment:** `// allBins | extend extendingToCheck = 'thisIsTheBackbone';`
- He literally calls it "the backbone" because everything else joins to this!

---

### **LINE 19: COMMENTED DEBUG (IGNORE)**
```kql
// allBins | extend extendingToCheck = 'thisIsTheBackbone';
```
Testing code to verify interval creation

---

## 📊 SUMMARY OF LINES 1-20:

✅ **Line 1:** Test site array (empty = all sites)
✅ **Lines 2-4:** Testing examples (ignore)
✅ **Lines 5-6:** Date range (CHANGE FOR APRIL 1-10)
✅ **Lines 7-14:** Identify bad data to remove (valid range: 0-7500 Wh)
✅ **Lines 15-17:** Debug code (ignore)
✅ **Line 18:** Create 15-min interval backbone (960 intervals for 10 days)
✅ **Line 19:** Debug code (ignore)

---

**YOUR UNDERSTANDING SO FAR:** 🎯 **100% CORRECT!**

You understood:
- ✅ Test site array purpose
- ✅ Date range configuration
- ✅ Bad data filtering (0-7500 Wh range)
- ✅ Project operator (column selection)
- ✅ The backbone concept

**Ready for Lines 20-40?** That's where the site list magic happens! 🚀

---

## 📖 LINES 20-40: GET SITE LIST FROM ASSET REGISTRY

### **LINES 20-28: FETCH METER IDS FROM ASSET REGISTRY**

```kql
let meterId =
    goldAdtPropertyMinMaxLatestViewV2
    | where Key == 'meterId'
      and ModelId startswith 'dtmi:qcells:contract:leapContract'
      and tolower(actionMax) != 'delete'
    | join kind=inner (
        goldAdtAllRelationshipsLatestView
        | where tolower(Action) != 'delete'
        | project siteId = Source, Target
    ) on $left.Id == $right.Target
    | distinct meterId = valueMax, siteId
    | where 1==1
        // and meterId //startswith "d82dd"
        and (siteId in (testsite) or array_length(testsite) ==0)
```

**Your understanding:** ✅ **ALMOST PERFECT!** Let me clarify:

---

### **LINE 20:** `let meterId =`
Creates variable to store site/meter list

---

### **LINE 21:** `goldAdtPropertyMinMaxLatestViewV2`

**What this table is:**
- **Asset Registry table** (Azure Digital Twin property view)
- Contains **metadata** about sites, batteries, contracts, etc.
- Each row = one property of one asset

**Example data:**
```
Id                  | Key        | valueMax                              | ModelId
site_12345_contract | meterId    | f9e463b0-3e50-4abe-9b83-2086403ad102 | dtmi:qcells:contract:leapContract:1
site_12345_contract | startDate  | 2025-01-15                            | dtmi:qcells:contract:leapContract:1
site_12346_battery  | capacity   | 13.5                                  | dtmi:qcells:battery:powerwall:2
```

**Why "MinMax" in table name?**
- Tracks property value changes over time
- `valueMax` = latest/current value

---

### **LINE 22:** `| where Key == 'meterId'`

**What it does:**
- Filter to rows where property name is 'meterId'
- We only want meter IDs, not other properties (capacity, startDate, etc.)

**Result after this filter:**
```
Id                  | Key     | valueMax (this is the meter ID!)
site_12345_contract | meterId | f9e463b0-3e50-4abe-9b83-2086403ad102
site_67890_contract | meterId | e8b1c6f6-8768-4875-92e5-f1a33deb0f78
...
```

---

### **LINE 23:** `and ModelId startswith 'dtmi:qcells:contract:leapContract'`

**What it does:**
- Filter to ONLY LEAP contract entities
- **Your understanding question:** "Why only LEAP contracts?"

**Answer:**
- Asset Registry has MANY contract types:
  - `dtmi:qcells:contract:leapContract` ← We want this!
  - `dtmi:qcells:contract:sgipContract`
  - `dtmi:qcells:contract:maintenanceContract`
  - etc.
- This filter gets only sites enrolled in LEAP program

**For DSGS 2026:**
- You might need: `dtmi:qcells:contract:dsgsContract`
- **ASK JUAN:** What's the DSGS ModelId for 2026?

---

### **LINE 24:** `and tolower(actionMax) != 'delete'`

**What it does:**
- Exclude deleted contracts
- `actionMax` = latest action on this property
- If site was removed from LEAP → `actionMax = 'delete'`
- We only want active contracts ✅

---

### **LINES 25-29: JOIN TO GET SITE IDs**

```kql
| join kind=inner (
    goldAdtAllRelationshipsLatestView
    | where tolower(Action) != 'delete'
    | project siteId = Source, Target
) on $left.Id == $right.Target
```

**Why we need this join:**

**Problem:**
- `goldAdtPropertyMinMaxLatestViewV2` has meter IDs
- But NO site IDs!
- We need BOTH meterId AND siteId

**Solution:**
- `goldAdtAllRelationshipsLatestView` = relationship/link table
- Shows connections: Site ↔ Contract ↔ Meter

**Relationship structure:**
```
Source (siteId)  →  Target (contractId)
400012345        →  site_12345_contract

site_12345_contract  →  meter_f9e463b0...
(This is in property table as Id)
```

**Line 26:** `goldAdtAllRelationshipsLatestView`
- Table showing relationships between entities

**Line 27:** `| where tolower(Action) != 'delete'`
- Only active relationships (not deleted)

**Line 28:** `| project siteId = Source, Target`
- **Source** = Site ID (e.g., "400012345")
- **Target** = Contract ID (e.g., "site_12345_contract")
- Rename Source → siteId for clarity

**Line 29:** `) on $left.Id == $right.Target`
- **Join condition:**
  - `$left.Id` = Contract ID from property table
  - `$right.Target` = Contract ID from relationship table
- **Result:** Links meter ID → contract → site ID

**After join, we have:**
```
meterId                                   | siteId
f9e463b0-3e50-4abe-9b83-2086403ad102     | 400012345
e8b1c6f6-8768-4875-92e5-f1a33deb0f78     | 400067890
```

**Your understanding:** ✅ **CORRECT!**
> "meterId is not present in silverCommDataSite, so they fetch it from these tables"

**Clarification:**
- `silverCommDataSite` HAS meterId! ✅
- BUT we need to know WHICH meterIds are in LEAP program
- Asset Registry tells us which meters are enrolled in LEAP

---

### **LINE 30:** `| distinct meterId = valueMax, siteId`

**What it does:**
- Remove duplicates (one site might have multiple properties)
- Rename `valueMax` → `meterId` for clarity
- **Result:** Unique list of (meterId, siteId) pairs

---

### **LINE 31:** `| where 1==1`

Same trick as before (makes commenting easier)

---

### **LINE 32:** `// and meterId //startswith "d82dd"`

Commented testing filter (ignore)

---

### **LINE 33:** `and (siteId in (testsite) or array_length(testsite) ==0)`

**Your understanding:** ✅ **CORRECT!**

**What it does:**
- If `testsite` array is NOT empty → Only include those specific sites
- If `testsite` array IS empty (`array_length == 0`) → Include ALL sites

**Logic:**
```
testsite = dynamic([])               → Process ALL sites ✅
testsite = dynamic([400000062, ...]) → Process only those 8 sites
```

**For production (5k or 7.7k sites):**
- Leave `testsite = dynamic([])` (empty)
- Script automatically processes all sites in Asset Registry ✅

---

## 📊 SUMMARY OF LINES 20-33:

**What this section does:**
```
Step 1: Get contracts from Asset Registry (LEAP enrolled)
Step 2: Filter to meterId properties only
Step 3: Exclude deleted contracts
Step 4: Join to get site IDs (contract → site relationship)
Step 5: Get distinct (meterId, siteId) pairs
Step 6: Apply test filter (if testing specific sites)

Result: List of all sites enrolled in LEAP program
        Format: meterId | siteId
        Count: ~5,000 sites (for LEAP 2025)
```

**What YOU understood correctly:**
- ✅ meterId fetched from Asset Registry (not in telemetry table alone)
- ✅ Joins goldAdtPropertyMinMaxLatestViewV2 + goldAdtAllRelationshipsLatestView
- ✅ Filters to non-deleted, LEAP-enrolled sites
- ✅ testsite array controls which sites to process

---

## ⚠️ THE BIG PROBLEM FOR DSGS 2026:

**This section gives us:** ~5,000 LEAP sites from Asset Registry

**Shuai needs:** ~7,700 DSGS sites

**Options Juan mentioned:**
1. **Wait for Asset Registry update** with DSGS contracts
2. **Use Shuai's Excel file** instead of Asset Registry query
3. **Hybrid:** Asset Registry + manually add missing 2,700 sites

**This is what Lines 31-78 address!** (We'll cover next)

---

**Ready for Lines 34-78?** That's the REMOVE/ADD section Juan said you need to discuss with him! 🎯

---

### **PART 2: Data Cleaning (Lines 7-14)**
```kql
let recordsToRemove = silverCommDataSite
    | where battery_200_IncWhExp >= 7500 
         or battery_200_IncWhExp < 0 
         or battery_200_IncWhImp >= 7500 
         or battery_200_IncWhImp < 0
```

**Purpose:** Remove bad/impossible data values
- Battery values > 7500 Wh or < 0 are errors

**You:** Don't need to change this ✅

---

### **PART 3: Time Backbone (Line 18)**
```kql
let allBins = range bin_base from startTime to endTime step 15m;
```

**Purpose:** Creates 15-minute interval grid (foundation for all data)

**Example for your dates:**
```
4/1/2026 00:00:00
4/1/2026 00:15:00
4/1/2026 00:30:00
...
4/10/2026 23:45:00
```

**Total intervals:** 10 days × 96 intervals/day = 960 intervals

---

### **PART 4: SITE LIST - THE BIG SECTION (Lines 20-78)**

This is what Juan said is "THE BIGGEST THING" you need to understand!

#### **Step 1: Get Sites from Asset Registry (Lines 20-28)**
```kql
let meterId =
    goldAdtPropertyMinMaxLatestViewV2
    | where Key == 'meterId' 
      and ModelId startswith 'dtmi:qcells:contract:leapContract' 
      and tolower(actionMax) != 'delete'
    | join kind=inner (goldAdtAllRelationshipsLatestView...) on ...
    | distinct meterId = valueMax, siteId
```

**What this does:**
- Queries Asset Registry for sites with LEAP contracts
- Result in 2025: ~5,000 sites

**The problem:** DSGS 2026 has 7,700 sites (not all in Asset Registry!)

---

#### **Step 2: REMOVE Sites (Lines 32-42) - Month-Specific**

This is the "messy" part Juan warned about!

```kql
// Line 34-35: July exclusions (commented out)
// Line 36: August exclusions (commented out)
// Line 37-39: September exclusions (commented out - HUGE list!)
// Line 42: October exclusions (ACTIVE - currently used)
| where meterId !in ('bc163f23-78c6-43b0-81c4-11426de4304c', ...)
```

**What this is:**
- Juan found sites that SHOULD NOT be in the list each month
- Different exclusions for different months
- October 2025 (active): excludes 27 sites

**Why different each month?**
- Sites were added/removed from LEAP program
- Some sites had bad data
- Manual corrections needed

**For your April 2026 task:**
- You'll need a NEW exclusion list (or none if all sites are clean)
- Discuss with Juan/Shuai during call

---

#### **Step 3: ADD Sites (Lines 43-75) - Month-Specific**

```kql
| union (
    // Line 45-47: July additions (commented)
    // Line 46: August additions (commented)
    // Line 47: September additions (commented)
    // Line 48: October additions (ACTIVE)
    print dynamic(['151be5e9-1071-426e-9dc5-dabe4ed209f0', ...]) // 7 sites
    | mv-expand print_0
    | project meterId = tostring(print_0)
    | extend siteId = case(
        meterId == 'e670c793-c1d4-4aaa-8a0b-7c311f83005f', '400015821',
        meterId == 'e8b1c6f6-8768-4875-92e5-f1a33deb0f78', 'ES-CA992COBRE94513',
        ...
    )
)
```

**What this is:**
- Sites that are IN LEAP but NOT in Asset Registry
- Manually added with hardcoded meterId → siteId mapping

**For April 2026:**
- This is the 2,700-site gap Jua

n mentioned!
- Need to decide: Use Shuai's Excel or wait for Asset Registry update

---

### **PART 5: Get Telemetry Data (Lines 81-95)**

```kql
let sites = silverCommDataSite
    | where siteId in (meterId|project siteId)
    | where sourceTimestamp between (startTime .. endTime)
    | join kind=leftanti (recordsToRemove) on siteId, sourceTimestamp  // Remove bad data
    | extend normalizedTimestamp = bin(sourceTimestamp, 15m)  // Round to 15-min
    | extend local_normalizedts = bin((sourceTimestamp - 7h), 15m)  // California time
    | project siteId, meterId, oem, sourceTimestamp, normalizedTimestamp, 
              battery_200_IncWhImp, battery_200_IncWhExp  // Import/Export energy
```

**What this does:**
1. Filters to sites from Part 4
2. Filters to date range
3. Removes bad records
4. Normalizes timestamps to 15-min boundaries
5. Converts UTC to local time (PST = UTC - 7 hours)
6. Gets battery energy data

**Energy fields:**
- `battery_200_IncWhImp`: Energy imported (charging) in Wh
- `battery_200_IncWhExp`: Energy exported (discharging) in Wh

---

### **PART 6: Create 15-Min Intervals (Lines 112-146)**

```kql
let new_bin_base_join = 
    meterId                              // All sites
    | join allBins                       // × All 15-min intervals
    | join (sites) on timestamp + site   // Fill with actual data
    | extend energy_consumed_kwh = battery_200_IncWhImp/1000  // Convert Wh → kWh
    | extend energy_generated_kwh = battery_200_IncWhExp/1000
    | extend energy_net_kwh = energy_consumed_kwh - energy_generated_kwh
```

**Result:** Every site × every 15-min interval (with data or NULL)

**Example:**
```
Site 400000001, 4/1/2026 00:00:00 → data (or NULL if missing)
Site 400000001, 4/1/2026 00:15:00 → data
Site 400000001, 4/1/2026 00:30:00 → data
...
Site 400000001, 4/10/2026 23:45:00 → data
Site 400000002, 4/1/2026 00:00:00 → data
...
```

---

### **PART 7: Format Output (Lines 152-173)**

```kql
new_bin_base_join
| summarize energy_net_kwh = sum(energy_net_kwh), ...
    by meter_id, interval_start_time_utc, interval_end_time_utc
| project meter_id, 
    interval_start_time_utc = "2026-04-01T00:00:00.0000Z",  // ISO 8601 format
    interval_end_time_utc = "2026-04-01T00:15:00.0000Z",
    energy_net_kwh = "2.5",  // Rounded to 3 decimals, or "Null"
    energy_consumed_kwh = "3.0",
    energy_generated_kwh = "0.5",
    final = 'true',
    region = 'CA'
| order by interval_start_time_utc asc, meter_id asc
```

**Output matches LEAP template exactly!** ✅

---

## 🎯 WHAT YOU NEED TO CHANGE FOR APRIL 1-10, 2026

### **Change 1: Date Range (Lines 5-6)**
```kql
// OLD:
let startTime = datetime(10/31/2025 00:00:00);
let endTime = datetime(11/01/2025 00:00:00);

// NEW:
let startTime = datetime(4/1/2026 00:00:00);
let endTime = datetime(4/11/2026 00:00:00);  // 4/11 to include all of 4/10
```

---

### **Change 2: Site List (Lines 42-75) - DISCUSSION NEEDED**

**Current (October 2025):**
- Exclusion list: 27 sites
- Addition list: 7 sites

**For April 2026:**
- Need to discuss with Juan/Shuai:
  - Which sites to exclude (if any)?
  - Which sites to add manually?
  - Or use Shuai's Excel file instead?

---

### **Change 3: RecordsToRemove Date Range (Line 11)**
```kql
// OLD:
and sourceTimestamp between (datetime(9/30/2025 ...) .. datetime(11/6/2025 ...))

// NEW:
and sourceTimestamp between (datetime(3/31/2026 ...) .. datetime(4/11/2026 ...))
```

---

## 💬 QUESTIONS TO ASK JUAN IN TODAY'S CALL

### **Question 1: Site List Approach**
"For April 2026 DSGS data (7,700 sites), should I:
- A) Wait for Asset Registry to be updated with all DSGS sites?
- B) Use Shuai's Excel file as the site list source?
- C) Use current Asset Registry (5k) + manually add 2,700 sites?"

---

### **Question 2: Monthly Exclusions/Additions**
"Lines 32-75 have month-specific exclusions and additions. For April 2026:
- Do I need a new exclusion list?
- Do I need a new addition list?
- Or can I start clean (no exclusions/additions)?"

---

### **Question 3: Output Verification**
"After I run the script, how do I verify the output is correct?
- How many total rows should I expect?
- What checks should I run before sharing with Shuai?"

Expected: 7,700 sites × 960 intervals = ~7.4 million rows

---

### **Question 4: SolarEdge Adjustment**
"Lines 144-145 have a special adjustment for SolarEdge sites. Does this still apply for April 2026?"

---

## 📊 OUTPUT FORMAT (Matches LEAP Template)

```csv
meter_id,interval_start_time_utc,interval_end_time_utc,energy_net_kwh,energy_consumed_kwh,energy_generated_kwh,final,region
f9e463b0-3e50-4abe-9b83-2086403ad102,2026-04-01T00:00:00.0000Z,2026-04-01T00:15:00.0000Z,2.345,3.100,0.755,true,CA
f9e463b0-3e50-4abe-9b83-2086403ad102,2026-04-01T00:15:00.0000Z,2026-04-01T00:30:00.0000Z,Null,Null,Null,true,CA
...
```

**Column mapping:**
- `meter_id`: Battery meter ID (from Asset Registry or manual list)
- `interval_start_time_utc`: Start of 15-min interval (ISO 8601 UTC)
- `interval_end_time_utc`: End of 15-min interval
- `energy_net_kwh`: Net energy (consumed - generated) in kWh
- `energy_consumed_kwh`: Energy imported/charged in kWh
- `energy_generated_kwh`: Energy exported/discharged in kWh
- `final`: Always 'true' (finalized data)
- `region`: Always 'CA' (California)

---

## ✅ NEXT STEPS AFTER CALL WITH JUAN

1. ✅ Clarify site list approach (Excel vs Asset Registry vs hybrid)
2. ✅ Get exclusion/addition lists for April 2026 (if needed)
3. ✅ Update date ranges in script
4. ✅ Update site list section
5. ✅ Run script in DEV/QA environment
6. ✅ Verify output row count and format
7. ✅ Export to CSV
8. ✅ Share with Shuai for review

---

**Status:** Ready for call with Juan ✅  
**Estimated time to modify script after call:** 30-60 minutes  
**Estimated time to run script:** 5-10 minutes (depending on data size)
