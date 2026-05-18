# Quick Command Reference for Naveen Call

**Event:** `Prg -20260318-85e2`  
**Purpose:** All queries executed to analyze this bug

---

## 🎯 **HOW WE GOT THE EVENT IDs**

### **From Screenshot/UI:**

**Main Event:** `Prg -20260318-85e2` (shown in Past Events List UI)

**Then we found the 3 child event IDs by querying:**

```kusto
// This query would show child events (exact query not documented, but likely)
silver_stream_dispatch_events
| where parent_event_id == "Prg -20260318-85e2"
// OR
| where event_name contains "20260318"
| project event_id, event_name, start_time, end_time, strategy
```

**Result: 3 Child Event IDs:**
1. `b45c6b33-ff43-4b66-9fb8-359c2c45eb57` (Event1-0820-0835)
2. `fdf0e836-a75d-4d54-b1e4-15af16ba53dc` (Event2-0851-0855)
3. `44d6d4b8-7b81-4c8d-9cc0-313143973f6f` (Event3-0838-0850)

---

## 🔍 **FUNCTION EXECUTION QUERIES**

### **1. Get Summary for Event1**
```kusto
getVPPDispatchSummary("b45c6b33-ff43-4b66-9fb8-359c2c45eb57")
```
**Result:** Returns data (1.7 kWh net, 4 sites)  
**Output File:** `event1_summary.csv`

---

### **2. Get Summary for Event2**
```kusto
getVPPDispatchSummary("fdf0e836-a75d-4d54-b1e4-15af16ba53dc")
```
**Result:** ❌ NO DATA returned (This is a bug!)  
**Output File:** None

---

### **3. Get Summary for Event3**
```kusto
getVPPDispatchSummary("44d6d4b8-7b81-4c8d-9cc0-313143973f6f")
```
**Result:** Returns data (-0.4 kWh net, 3 sites)  
**Output File:** `event3_summary.csv`

---

## 📊 **HOW WE GOT THE SITE IDs**

### **Query: Count Sites with Non-Stop Commands**

```kusto
let event_ids = dynamic([
    "b45c6b33-ff43-4b66-9fb8-359c2c45eb57", 
    "fdf0e836-a75d-4d54-b1e4-15af16ba53dc", 
    "44d6d4b8-7b81-4c8d-9cc0-313143973f6f"
]);

silver_dispatch_result_dto
| where event_id in (event_ids)
    and tolower(command) !contains "stop"
| summarize 
    total_sites = count_distinct(site_id),
    sites_list = make_set(site_id),
    commands = make_set(command)
| project total_sites, sites_list, commands
```

**Result:**
- **Total Sites:** 4
- **Sites:** `["400005226", "400002331", "400002333", "400005338"]`
- **Commands:** `["CHARGE_FROM_GRID_AND_SOLAR", "SELF_CONSUMPTION"]`

**Output File:** `site_count_with_no_stop_command.csv`

---

## 🔍 **BREAKDOWN BY INDIVIDUAL EVENT**

### **Query: Sites Per Event**

```kusto
let event_ids = dynamic([
    "b45c6b33-ff43-4b66-9fb8-359c2c45eb57", 
    "fdf0e836-a75d-4d54-b1e4-15af16ba53dc", 
    "44d6d4b8-7b81-4c8d-9cc0-313143973f6f"
]);

silver_dispatch_result_dto
| where event_id in (event_ids)
    and tolower(command) !contains "stop"
| summarize 
    site_count = count_distinct(site_id),
    sites = make_set(site_id)
by event_id
```

**Result:**
| Event ID | Site Count | Sites |
|----------|------------|-------|
| `b45c6b33...` (Event1) | 4 | 400005226, 400002331, 400002333, 400005338 |
| `fdf0e836...` (Event2) | 4 | 400002333, 400002331, 400005338, 400005226 |
| `44d6d4b8...` (Event3) | 3 | 400005338, 400002333, 400002331 |

**Output File:** `breakdown_by_event_id_data.csv`

---

## 📋 **ALL COMMANDS FOR ALL SITES**

### **Query: All Commands (Including Stops)**

```kusto
let event_ids = dynamic([
    "b45c6b33-ff43-4b66-9fb8-359c2c45eb57", 
    "fdf0e836-a75d-4d54-b1e4-15af16ba53dc", 
    "44d6d4b8-7b81-4c8d-9cc0-313143973f6f"
]);

silver_dispatch_result_dto
| where event_id in (event_ids)
| project event_id, site_id, command
| order by event_id, site_id
```

**Result:** 60 rows showing ALL commands sent to each site

**Output File:** `commands_for_3_site_ids.csv`

---

## 🔍 **SPECIFIC SITE INVESTIGATION (400005226)**

### **Query: Commands for Site 400005226**

```kusto
let event_ids = dynamic([
    "b45c6b33-ff43-4b66-9fb8-359c2c45eb57", 
    "fdf0e836-a75d-4d54-b1e4-15af16ba53dc", 
    "44d6d4b8-7b81-4c8d-9cc0-313143973f6f"
]);

silver_dispatch_result_dto
| where event_id in (event_ids)
    and site_id == "400005226"
| project event_id, site_id, command, timestamp
```

**Result:**
- Event1: Got `CHARGE_FROM_GRID_AND_SOLAR` ✅
- Event2: Got `CHARGE_FROM_GRID_AND_SOLAR` ✅
- Event3: NO commands ❌

---

## 📊 **TELEMETRY DATA FOR SITE 400005226**

### **Query: All Telemetry Data for Full Hour**

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

**Result for 400005226:**
- **Charged:** 0 Wh
- **Discharged:** 0 Wh
- **Net Energy:** 0 Wh
- **Row Count:** 12 rows (telemetry exists but all 0s!)

**Output File:** `check_all_sites_for that data_in_silvercommdatasites.csv`

---

## ✅ **SUMMARY**

### **How We Got Event IDs:**
1. Main event from UI screenshot: `Prg -20260318-85e2`
2. Queried for child events (3 child event IDs found)

### **How We Got Site IDs:**
1. Queried `silver_dispatch_result_dto` for all events
2. Filtered for non-stop commands
3. Found 4 unique sites: **400005226, 400002331, 400002333, 400005338**

### **How We Got Site Participation Count:**
1. Function uses `COUNT(DISTINCT site_id WHERE command NOT LIKE '%stop%')`
2. Event1: 4 sites
3. Event2: 4 sites  
4. Event3: 3 sites

### **Key Finding:**
- Site **400005226** got commands but has **0 energy performance**
- This site is included in command count but contributes 0 to energy total

---

## 🎯 **READY FOR CALL**

You can show Naveen:
1. ✅ How you found the 3 child event IDs
2. ✅ How you discovered the 4 participating sites
3. ✅ How you identified site 400005226 as the "ghost" site
4. ✅ All the queries you executed

**Just refer to this document during the call!** 📋

