# Step 6: Testing

## Test Cases

### Test 1: Basic Functionality
**Run this in Fabric Query Editor:**
```kql
getAllVppSitesByUserId('81ab4c51-a8d9-ef11-8eea-00224809f11c', 0, 5)
```

**Check:**
- Does the function run without errors? ✅
- Is there an `external_reference_id` field in the output? ✅
- Does it show account numbers like "APPTPO-2501513034"? ✅

---

### Test 2: Sites Without Account Number
**Check the output:**
- Some sites might not have `accountNumber`
- These should show `external_reference_id: "-"` ✅

---

### Test 3: Pagination
**Run:**
```kql
// Page 0
getAllVppSitesByUserId('81ab4c51-a8d9-ef11-8eea-00224809f11c', 0, 10)

// Page 1
getAllVppSitesByUserId('81ab4c51-a8d9-ef11-8eea-00224809f11c', 1, 10)
```

**Check:**
- Does pagination still work correctly? ✅
- Is `external_reference_id` in both pages? ✅

---

### Test 4: Different Environments

**DEV:**
```kql
getAllVppSitesByUserId('81ab4c51-a8d9-ef11-8eea-00224809f11c', 0, 5)
```

**QA:**
```kql
getAllVppSitesByUserId('13d79b62-cf04-f011-bae2-6045bdf0782b', 0, 5)
```

---

## Expected Output:

```json
{
  "metadata": {
    "pagination": {
      "page": 0,
      "page_size": 5,
      "total_count": 50
    }
  },
  "data": [
    {
      "site_number": "400000020",
      "site_name": "Test Site Name",
      "state": "CA",
      "zipPostalCode": "90210",
      "external_reference_id": "APPTPO-2501513034",  ← NEW FIELD!
      "program_name": ["VPP Program"],
      "SOC": 85.5,
      "rated_capacity": 10000,
      "system_size_kw": 5.5,
      "inverter_status": true,
      "grid_energy_imported": 1000.5,
      "grid_energy_exported": 500.2,
      "lifetime_production": "-",
      "oem_name": "QCells",
      "last_update_in_local_time": "2026-04-02T10:30:00",
      "last_updated_timestamp_utc": "2026-04-02T18:30:00Z",
      "timezone": "America/Los_Angeles"
    }
  ],
  "status": 200
}
```

---

## What to Look For:

✅ **Success Indicators:**
- Function runs without errors
- `external_reference_id` appears in every site record
- Values are either account numbers (e.g., "APPTPO-2501513034") or "-"
- All other fields still work correctly
- Pagination works
- Response time is similar to before

❌ **Failure Indicators:**
- Function throws an error
- `external_reference_id` is missing
- Other fields are broken
- Very slow response time

---

## If Something Goes Wrong:

### Error: "Column 'assetRegistrationInfo' not found"
**Fix:** Run `.show function GetSiteProperties` and verify it returns `assetRegistrationInfo`

### Error: Syntax error
**Fix:** Check for missing commas, quotes, or brackets in your code

### No data returned
**Fix:** Test with a different userId - some users might not have VPP sites

### Function runs but field is always "-"
**Fix:** Run this query to check if accountNumber exists:
```kql
GetSiteProperties(dynamic(['400000020']))
| project assetRegistrationInfo
```

---

## Checklist:

- [ ] Function deploys without errors
- [ ] Test with DEV userId
- [ ] Verify `external_reference_id` appears
- [ ] Test with QA userId
- [ ] Verify pagination works
- [ ] Check sites with and without account numbers
- [ ] Notify frontend team that field is ready
- [ ] Update ADO ticket

---

**Next:** Move to `07_DEPLOYMENT.md`



