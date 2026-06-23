# Battery Power Field Addition
## getVppSitesTelemetryBatch Enhancement

**Date:** 2026-06-22  
**Requested By:** Alex  
**Implemented By:** Jagan Murikinati  
**Status:** ✅ COMPLETE

---

## 📋 **Request**

Alex's comment on ticket:
> "Can we also have battery power field in the response of any of these endpoints?"

---

## ✅ **Implementation**

### **Field Added:** `battery_power_w`

**Source:** `silverCommDataSite.battery_200_W`  
**Type:** `real` (number)  
**Unit:** Watts (W)  
**Description:** Instantaneous battery power reading

---

## 📊 **Field Details**

### **Value Interpretation:**

| Value | Meaning | Example |
|-------|---------|---------|
| **Positive** | Battery **discharging** (sending power out) | `5000` = Discharging at 5 kW |
| **Negative** | Battery **charging** (receiving power) | `-3000` = Charging at 3 kW |
| **Zero** | Battery idle (no power flow) | `0` = Idle |
| **Null** | No telemetry data available | `null` = Offline/no data |

---

## 📝 **Changes Made**

### **File 1: getVppSitesTelemetryBatch.kql**

**Line 55-64** - Added to telemetry query:
```kql
| project siteId,
          SOC = battery_713_SoC,
          battery_power_w = battery_200_W,  // ⚡ ADDED
          grid_energy_imported = grid_200_IncWhImp,
          grid_energy_exported = grid_200_IncWhExp,
          ...
```

**Line 127-140** - Added to final output:
```kql
| project
    site_number = siteId,
    SOC,
    battery_power_w,  // ⚡ ADDED
    rated_capacity,
    system_size_kw,
    ...
```

### **File 2: API_CONTRACTS.md**

Updated response schema and field descriptions to include `battery_power_w`.

---

## 🎯 **Response Example**

### **Before:**
```json
{
  "data": [
    {
      "site_number": "400012345",
      "SOC": 85.5,
      "rated_capacity": 13.5,
      "system_size_kw": 10.2,
      "inverter_status": true,
      "grid_energy_imported": 12345.67,
      "grid_energy_exported": 23456.78,
      ...
    }
  ]
}
```

### **After:**
```json
{
  "data": [
    {
      "site_number": "400012345",
      "SOC": 85.5,
      "battery_power_w": 5000,              // ⚡ NEW FIELD
      "rated_capacity": 13.5,
      "system_size_kw": 10.2,
      "inverter_status": true,
      "grid_energy_imported": 12345.67,
      "grid_energy_exported": 23456.78,
      ...
    }
  ]
}
```

---

## ⚡ **Performance Impact**

**Impact:** ✅ **ZERO**

- Field already exists in `silverCommDataSite` table
- No additional query needed
- Same `arg_max()` query retrieves all telemetry fields
- No JOIN required
- No performance degradation

---

## ✅ **Validation**

### **Data Source Confirmed:**
- ✅ `battery_200_W` exists in `silverCommDataSite` table
- ✅ Used in other production functions (getSiteDispatchCommandSummary)
- ✅ Real-time instantaneous power reading
- ✅ Standard field across all OEMs (Tesla, Qcells, etc.)

### **Why This Field:**
- `battery_200_W` = AC battery power (most common) ✅
- `battery_701_W` = Alternative AC battery power
- `battery_714_DCW` = DC battery power

**Decision:** Used `battery_200_W` (standard AC power field)

---

## 🧪 **Testing**

### **Test Query:**
```kql
getVppSitesTelemetryBatch(
    siteIds = dynamic(["400012345", "400012346"])
)
```

### **Expected Output:**
- `battery_power_w` field present in all records ✅
- Value range: typically -10000 to +10000 (W)
- Null for sites with no recent telemetry

---

## 📋 **Updated Response Schema**

| Field | Type | Unit | Description |
|-------|------|------|-------------|
| `site_number` | string | - | Site ID |
| `SOC` | number | % | State of Charge (0-100) |
| **`battery_power_w`** | **number** | **W** | **Instantaneous battery power** ⚡ |
| `rated_capacity` | number | kW | Battery capacity |
| `system_size_kw` | number | kW | PV system size |
| `inverter_status` | boolean | - | Online status |
| `grid_energy_imported` | number | Wh | Cumulative grid import |
| `grid_energy_exported` | number | Wh | Cumulative grid export |
| `lifetime_production` | string | - | Placeholder |
| `last_update_in_local_time` | datetime | - | Last update (local) |
| `last_updated_timestamp_utc` | datetime | - | Last update (UTC) |
| `timezone` | string | - | Site timezone |

---

## ✅ **Checklist**

- [x] Field added to telemetry query (Line 57)
- [x] Field added to final output (Line 130)
- [x] API documentation updated
- [x] Performance impact: None
- [x] Backward compatible: Yes (additive change)
- [x] Data source validated: battery_200_W exists
- [x] Ready for deployment

---

## 🚀 **Deployment**

**No additional steps required!**

The function already updated:
- ✅ `getVppSitesTelemetryBatch.kql` - Production code
- ✅ `API_CONTRACTS.md` - Documentation

**Deploy same as before - battery power field automatically included!** ✅


