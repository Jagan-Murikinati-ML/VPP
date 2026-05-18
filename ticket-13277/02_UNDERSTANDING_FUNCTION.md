# Step 2: Understanding the Function

## What is `getAllVppSitesByUserId`?

A KQL function in Fabric Eventhouse that returns VPP site data for a specific user.

---

## Current Function Structure (9 Steps):

**Step 1:** Get site IDs for the user  
**Step 2:** Filter VPP registered sites  
**Step 3:** Apply pagination  
**Step 4:** Get site properties via `GetSiteProperties()` → **Stores in `goldAdtPropertySites`**  
**Step 5:** Get telemetry data  
**Step 6:** Get program info  
**Step 7:** Get device data (rated_capacity, system_size)  
**Step 8:** Combine all data into JSON  
**Step 9:** Return paginated response  

---

## Current Response Format:

```json
{
  "data": [
    {
      "site_number": "12345",
      "site_name": "Test Site",
      "state": "CA",
      "zipPostalCode": "90210",
      "program_name": ["VPP Program"],
      "SOC": 85,
      "rated_capacity": 10000,
      "system_size_kw": 5.5,
      "inverter_status": true,
      "grid_energy_imported": 1000,
      "grid_energy_exported": 500,
      "lifetime_production": "-",
      "oem_name": "QCells",
      "last_update_in_local_time": "2026-04-02T10:30:00",
      "last_updated_timestamp_utc": "2026-04-02T18:30:00Z",
      "timezone": "America/Los_Angeles"
    }
  ],
  "metadata": {...},
  "status": 200
}
```

---

## Key Discovery: `GetSiteProperties` Returns `assetRegistrationInfo`

Looking at `getsiteproperties_function.csv` (line 23):
```kql
assetRegistrationInfo = anyif(todynamic(ParsedValue), Property == 'assetRegistrationInfo')
```

**This means:**
- `GetSiteProperties()` already fetches `assetRegistrationInfo`
- It's stored in the `goldAdtPropertySites` variable (line 42 of main function)
- `assetRegistrationInfo` is a JSON object containing `accountNumber`

---

## What We Already Have:

At **Step 4** (line 42), the function calls:
```kql
let goldAdtPropertySites = GetSiteProperties(paginatedSiteIdsList)
```

This returns a table with columns:
- `siteId`
- `address` (JSON object)
- `oemInfo` (JSON object)
- `assetRegistrationInfo` (JSON object) ← **Contains accountNumber!**
- `otherProperties`

---

## Where We Need to Make Changes:

**Step 8 (lines 94-120):** This is where all data is combined into JSON.

Currently it extracts data like:
```kql
zipPostalCode = tostring(address['zipPostalCode'])      // From address object
oemname = tostring(oemInfo.['1.oemName'])               // From oemInfo object
```

We need to add:
```kql
accountNumber = tostring(assetRegistrationInfo['accountNumber'])  // From assetRegistrationInfo object
```

---

## Summary:

✅ Function already has `assetRegistrationInfo` data  
✅ We just need to extract `accountNumber` from it  
✅ Add it to the JSON response  
✅ No new database queries needed!  

---

**Next:** Move to `03_IMPLEMENTATION.md`

