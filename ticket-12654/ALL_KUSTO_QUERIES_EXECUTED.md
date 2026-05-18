# ADO-12654: Complete List of Kusto Queries Executed

**Event:** Prg -20260318-85e2  
**Date:** 2026-03-27  
**Analyst:** Jagan Murikinati

---

## 📋 **TABLE OF CONTENTS**

1. [Function Definition Queries](#1-function-definition-queries)
2. [Function Execution Queries](#2-function-execution-queries)
3. [Command Analysis Queries](#3-command-analysis-queries)
4. [Telemetry Data Queries](#4-telemetry-data-queries)
5. [Event Details Queries](#5-event-details-queries)

---

## 1. FUNCTION DEFINITION QUERIES

### Query 1.1: Show Function Definition
```kusto
.show function getVPPDispatchSummary
```
**Purpose:** Get the complete function code  
**Output File:** `dispatach_summary_function_output.csv`

---

## 2. FUNCTION EXECUTION QUERIES

### Query 2.1: Execute Function for Event1
```kusto
getVPPDispatchSummary("b45c6b33-ff43-4b66-9fb8-359c2c45eb57")
```
**Purpose:** Get summary data for Event1 (03:20-03:35)  
**Output File:** `event1_summary.csv`  
**Result:** Returns 2 rows with cumulative energy values

### Query 2.2: Execute Function for Event2
```kusto
getVPPDispatchSummary("fdf0e836-a75d-4d54-b1e4-15af16ba53dc")
```
**Purpose:** Get summary data for Event2 (03:52-03:55)  
**Output File:** None  
**Result:** ❌ NO DATA returned

### Query 2.3: Execute Function for Event3
```kusto
getVPPDispatchSummary("44d6d4b8-7b81-4c8d-9cc0-313143973f6f")
```
**Purpose:** Get summary data for Event3 (03:39-03:50)  
**Output File:** `event3_summary.csv`  
**Result:** Returns 2 rows with cumulative energy values

---

## 3. COMMAND ANALYSIS QUERIES

### Query 3.1: Count Sites with Non-Stop Commands
```kusto
let event_ids = dynamic(["b45c6b33-ff43-4b66-9fb8-359c2c45eb57", 
                         "fdf0e836-a75d-4d54-b1e4-15af16ba53dc", 
                         "44d6d4b8-7b81-4c8d-9cc0-313143973f6f"]);
silver_dispatch_result_dto
| where event_id in (event_ids)
    and tolower(command) !contains "stop"
| summarize 
    total_sites = count_distinct(site_id),
    sites_list = make_set(site_id),
    commands = make_set(command)
| project total_sites, sites_list, commands
```
**Purpose:** Count sites that received non-stop commands across all 3 events  
**Output File:** `site_count_with_no_stop_command.csv`  
**Result:** 4 sites (400005226, 400002331, 400002333, 400005338)

### Query 3.2: Count Sites with Stop Commands
```kusto
let event_ids = dynamic(["b45c6b33-ff43-4b66-9fb8-359c2c45eb57", 
                         "fdf0e836-a75d-4d54-b1e4-15af16ba53dc", 
                         "44d6d4b8-7b81-4c8d-9cc0-313143973f6f"]);
silver_dispatch_result_dto
| where event_id in (event_ids)
    and tolower(command) contains "stop"
| summarize 
    total_sites = count_distinct(site_id),
    sites_list = make_set(site_id),
    commands = make_set(command)
| project total_sites, sites_list, commands
```
**Purpose:** Check which sites received stop commands  
**Output File:** `site_count_with_stop_command.csv`  
**Result:** 3 sites (400005338, 400002333, 400002331) - excludes 400005226

### Query 3.3: Breakdown by Event ID
```kusto
let event_ids = dynamic(["b45c6b33-ff43-4b66-9fb8-359c2c45eb57", 
                         "fdf0e836-a75d-4d54-b1e4-15af16ba53dc", 
                         "44d6d4b8-7b81-4c8d-9cc0-313143973f6f"]);
silver_dispatch_result_dto
| where event_id in (event_ids)
    and tolower(command) !contains "stop"
| summarize 
    site_count = count_distinct(site_id),
    sites = make_set(site_id)
    by event_id
```
**Purpose:** See site count per individual event  
**Output File:** `breakdown_by_event_id_data.csv`  
**Result:** Event1: 4 sites, Event2: 4 sites, Event3: 3 sites

### Query 3.4: All Commands for Sites
```kusto
let event_ids = dynamic(["b45c6b33-ff43-4b66-9fb8-359c2c45eb57", 
                         "fdf0e836-a75d-4d54-b1e4-15af16ba53dc", 
                         "44d6d4b8-7b81-4c8d-9cc0-313143973f6f"]);
silver_dispatch_result_dto
| where event_id in (event_ids)
| project event_id, site_id, command
| order by event_id, site_id
```
**Purpose:** See all commands (including stops) sent to each site  
**Output File:** `commands_for_3_site_ids.csv`  
**Result:** 60 rows showing all command details

### Query 3.5: Check Commands for Specific Site
```kusto
let event_ids = dynamic(["b45c6b33-ff43-4b66-9fb8-359c2c45eb57", 
                         "fdf0e836-a75d-4d54-b1e4-15af16ba53dc", 
                         "44d6d4b8-7b81-4c8d-9cc0-313143973f6f"]);
silver_dispatch_result_dto
| where event_id in (event_ids)
    and site_id == "400005226"
| project event_id, site_id, command, timestamp
```
**Purpose:** Check what commands site 400005226 received  
**Result:** Got CHARGE_FROM_GRID_AND_SOLAR in Event1 and Event2, no commands in Event3

---

## 4. TELEMETRY DATA QUERIES

**Note:** These queries are run directly in the database containing `silverCommDataSite` table (no database prefix needed).

### Query 4.1: Event1 Telemetry Data
```kusto
silverCommDataSite
| where sourceTimestamp >= datetime(2026-03-18 03:20:00)
    and sourceTimestamp < datetime(2026-03-18 03:35:00)
    and siteId in ("400005338", "400002333", "400002331", "400005226")
| summarize
    total_charged = sum(battery_200_IncWhImp),
    total_discharged = sum(battery_200_IncWhExp),
    row_count = count()
    by siteId
| extend net_energy = total_charged - total_discharged
```
**Purpose:** Get telemetry data for Event1 from raw table
**Output File:** `event1_data_in_silvercommdatasite.csv`
**Result:**
- 400005226: 0 charged, 0 discharged (3 rows)
- 400002331: 0 charged, 600 Wh discharged (3 rows)
- 400002333: 0 charged, 300 Wh discharged (3 rows)

### Query 4.2: Event2 Telemetry Data
```kusto
silverCommDataSite
| where sourceTimestamp >= datetime(2026-03-18 03:52:00)
    and sourceTimestamp < datetime(2026-03-18 03:55:00)
    and siteId in ("400005338", "400002333", "400002331", "400005226")
| summarize
    total_charged = sum(battery_200_IncWhImp),
    total_discharged = sum(battery_200_IncWhExp),
    row_count = count()
    by siteId
| extend net_energy = total_charged - total_discharged
```
**Purpose:** Check if Event2 has telemetry data
**Result:** ❌ NO DATA (confirms Event2 is missing from silverCommDataSite)

### Query 4.3: Event3 Telemetry Data
```kusto
silverCommDataSite
| where sourceTimestamp >= datetime(2026-03-18 03:39:00)
    and sourceTimestamp < datetime(2026-03-18 03:50:00)
    and siteId in ("400005338", "400002333", "400002331")
| summarize
    total_charged = sum(battery_200_IncWhImp),
    total_discharged = sum(battery_200_IncWhExp),
    row_count = count()
    by siteId
| extend net_energy = total_charged - total_discharged
```
**Purpose:** Get telemetry data for Event3
**Output File:** `event3_data_in_silvercommdatasite.csv`
**Result:**
- 400002331: 0 charged, 400 Wh discharged (2 rows)
- 400002333: 0 charged, 200 Wh discharged (2 rows)

### Query 4.4: All Data for Full Hour
```kusto
silverCommDataSite
| where sourceTimestamp >= datetime(2026-03-18 03:00:00)
    and sourceTimestamp < datetime(2026-03-18 04:00:00)
    and siteId in ("400005338", "400002333", "400002331", "400005226")
| summarize
    total_charged = sum(battery_200_IncWhImp),
    total_discharged = sum(battery_200_IncWhExp),
    row_count = count(),
    min_time = min(sourceTimestamp),
    max_time = max(sourceTimestamp)
    by siteId
| extend net_energy = total_charged - total_discharged
```
**Purpose:** Get total telemetry across all events
**Output File:** `check_all_sites_for that data_in_silvercommdatasites.csv`
**Result:**
- 400005226: 0 charged, 0 discharged (12 rows)
- 400002333: 0 charged, 1200 Wh discharged (12 rows)
- 400002331: 0 charged, 2400 Wh discharged (12 rows)

---

## 5. EVENT DETAILS QUERIES

### Query 5.1: Sample Event Stream Data
```kusto
silver_stream_dispatch_events
| take 10
```
**Purpose:** See sample data structure and available columns  
**Output File:** `silver_stream_dispatch_event_sample_data.csv`

---

## 📊 **SUMMARY OF FINDINGS**

### Key Discoveries:
1. ✅ Event2 has NO data in `silverCommDataSite` table
2. ✅ Site 400005226 received commands but has 0 energy
3. ✅ Event1 and Event3 have data but values don't match Site-Level Performance UI
4. ✅ Function returns cumulative values (last row = total)
5. ✅ Function uses two data sources (commands + telemetry)

### Files Generated:
- `event1_summary.csv`
- `event3_summary.csv`
- `site_count_with_no_stop_command.csv`
- `site_count_with_stop_command.csv`
- `breakdown_by_event_id_data.csv`
- `commands_for_3_site_ids.csv`
- `event1_data_in_silvercommdatasite.csv`
- `event3_data_in_silvercommdatasite.csv`
- `check_all_sites_for that data_in_silvercommdatasites.csv`
- `silver_stream_dispatch_event_sample_data.csv`

---

**Document Created:** 2026-03-27  
**Last Updated:** 2026-03-27

