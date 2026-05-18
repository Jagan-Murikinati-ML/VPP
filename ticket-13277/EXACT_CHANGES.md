# Exact Changes for Ticket #13277

## Summary: Add ONLY 2 Lines

---

## CHANGE 1: Extract accountNumber (Line 98)

### BEFORE:
```kql
let result_data = goldAdtPropertySites
     | project siteId, otherProperties.siteName,
               zipPostalCode = tostring(address['zipPostalCode']),
               state = tostring(address['stateProvince']),
               oemname = tostring( iff(isempty(oemInfo.['1.oemName']),oemInfo.['0.oemName'], oemInfo.['1.oemName']))
```

### AFTER:
```kql
let result_data = goldAdtPropertySites
     | project siteId, otherProperties.siteName,
               zipPostalCode = tostring(address['zipPostalCode']),
               state = tostring(address['stateProvince']),
               oemname = tostring( iff(isempty(oemInfo.['1.oemName']),oemInfo.['0.oemName'], oemInfo.['1.oemName'])),
               accountNumber = tostring(assetRegistrationInfo['accountNumber'])  // ADDED for Ticket #13277: Extract account number
```

**What Changed:**
- Added a comma at the end of the `oemname` line
- Added new line to extract `accountNumber` from `assetRegistrationInfo`

---

## CHANGE 2: Add to JSON Response (Line 108)

### BEFORE:
```kql
     | extend data = pack(
                  'site_number', siteId,
                  'site_name', otherProperties_siteName,
                  'state', state,
                  'zipPostalCode', zipPostalCode,
                  'program_name', program_name,
```

### AFTER:
```kql
     | extend data = pack(
                  'site_number', siteId,
                  'site_name', otherProperties_siteName,
                  'state', state,
                  'zipPostalCode', zipPostalCode,
                  'external_reference_id', accountNumber,  // ADDED for Ticket #13277: External Reference ID field
                  'program_name', program_name,
```

**What Changed:**
- Added new field `'external_reference_id', accountNumber,` after `zipPostalCode`
- This adds the field to the JSON output

---

## Why No `coalesce`?

Looking at the existing pack() function, most fields just pass the value directly:
- `'SOC', SOC` ← No coalesce
- `'program_name', program_name` ← No coalesce
- `'rated_capacity', rated_capacity` ← No coalesce
- `'timezone', timezone` ← No coalesce

**Only exception:** `'lifetime_production', '-'` is hardcoded to '-'

So we follow the pattern: `'external_reference_id', accountNumber`

---

## If You Want to Handle Null/Empty Values:

**Option 1 (Current - matches existing pattern):**
```kql
'external_reference_id', accountNumber,
```
- If accountNumber is null → shows `null` in JSON
- If accountNumber is empty string → shows `""` in JSON

**Option 2 (Use coalesce):**
```kql
'external_reference_id', coalesce(accountNumber, '-'),
```
- If accountNumber is null or empty → shows `"-"` in JSON
- More user-friendly for frontend

**Recommendation:** Use Option 1 first, test it. If frontend wants "-" for empty values, switch to Option 2.

---

## Line Numbers Reference:

| Change | Line Number | What to Add |
|--------|-------------|-------------|
| Extract accountNumber | ~98 | `accountNumber = tostring(assetRegistrationInfo['accountNumber'])` |
| Add to JSON | ~108 | `'external_reference_id', accountNumber,` |

---

## Complete Modified Function:

See `05_COMPLETE_MODIFIED_FUNCTION.md` for the full code ready to copy-paste!

---

## Visual Guide:

```
Step 8: Combine all data
├── project clause (lines 94-98)
│   ├── siteId
│   ├── siteName
│   ├── zipPostalCode
│   ├── state
│   ├── oemname
│   └── accountNumber  ← NEW LINE 1
│
└── pack() function (lines 103-120)
    ├── 'site_number', siteId
    ├── 'site_name', otherProperties_siteName
    ├── 'state', state
    ├── 'zipPostalCode', zipPostalCode
    ├── 'external_reference_id', accountNumber  ← NEW LINE 2
    ├── 'program_name', program_name
    └── ... other fields
```

---

**That's it! Just 2 lines to add!**

