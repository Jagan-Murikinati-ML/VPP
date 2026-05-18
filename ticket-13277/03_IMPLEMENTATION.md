# Step 3: Implementation

## What to Change: ADD ONLY 2 LINES

---

## LINE 1: Extract accountNumber

**Location:** In the `project` clause (around line 98)

**Add this line:**
```kql
accountNumber = tostring(assetRegistrationInfo['accountNumber'])
```

### Before:
```kql
let result_data = goldAdtPropertySites
     | project siteId, otherProperties.siteName,
               zipPostalCode = tostring(address['zipPostalCode']),
               state = tostring(address['stateProvince']),
               oemname = tostring( iff(isempty(oemInfo.['1.oemName']),oemInfo.['0.oemName'], oemInfo.['1.oemName']))
```

### After:
```kql
let result_data = goldAdtPropertySites
     | project siteId, otherProperties.siteName,
               zipPostalCode = tostring(address['zipPostalCode']),
               state = tostring(address['stateProvince']),
               oemname = tostring( iff(isempty(oemInfo.['1.oemName']),oemInfo.['0.oemName'], oemInfo.['1.oemName'])),
               accountNumber = tostring(assetRegistrationInfo['accountNumber'])  // ← ADD THIS
```

---

## LINE 2: Add to JSON Response

**Location:** In the `pack()` function (around line 107)

**Add this line:**
```kql
'external_reference_id', coalesce(accountNumber, '-'),
```

### Before:
```kql
     | extend data = pack(
                  'site_number', siteId,
                  'site_name', otherProperties_siteName,
                  'state', state,
                  'zipPostalCode', zipPostalCode,
                  'program_name', program_name,
```

### After:
```kql
     | extend data = pack(
                  'site_number', siteId,
                  'site_name', otherProperties_siteName,
                  'state', state,
                  'zipPostalCode', zipPostalCode,
                  'external_reference_id', coalesce(accountNumber, '-'),  // ← ADD THIS
                  'program_name', program_name,
```

---

## Understanding the Code:

### Line 1 Explanation:
```kql
accountNumber = tostring(assetRegistrationInfo['accountNumber'])
```
- `assetRegistrationInfo` = Column in goldAdtPropertySites (JSON object)
- `['accountNumber']` = Extract the accountNumber property
- `tostring(...)` = Convert to string
- `accountNumber =` = Store in new variable

**Same pattern as existing fields:**
- `zipPostalCode = tostring(address['zipPostalCode'])`
- `state = tostring(address['stateProvince'])`

---

### Line 2 Explanation:
```kql
'external_reference_id', coalesce(accountNumber, '-'),
```
- `'external_reference_id'` = Field name in JSON output
- `coalesce(accountNumber, '-')` = If accountNumber is null, use '-'

**Same pattern as existing fields:**
- `'site_number', siteId`
- `'zipPostalCode', zipPostalCode`

---

## Expected Output After Change:

```json
{
  "data": [
    {
      "site_number": "12345",
      "site_name": "Test Site",
      "state": "CA",
      "zipPostalCode": "90210",
      "external_reference_id": "APPTPO-2501513034",  ← NEW FIELD!
      "program_name": ["VPP Program"],
      ...
    }
  ]
}
```

---

**Next:** Move to `04_HOW_TO_EDIT_FUNCTION.md`

