# Field Naming Convention

## Current Field Names in the Function

Looking at the `pack()` function (lines 104-119), here are ALL the field names:

```kql
'site_number'                      // snake_case
'site_name'                        // snake_case
'state'                            // lowercase
'zipPostalCode'                    // camelCase
'program_name'                     // snake_case
'SOC'                              // UPPERCASE
'rated_capacity'                   // snake_case
'system_size_kw'                   // snake_case
'inverter_status'                  // snake_case
'grid_energy_imported'             // snake_case
'grid_energy_exported'             // snake_case
'lifetime_production'              // snake_case
'oem_name'                         // snake_case
'last_update_in_local_time'        // snake_case
'last_updated_timestamp_utc'       // snake_case
'timezone'                         // lowercase
```

---

## Pattern Analysis

**MAJORITY:** `snake_case` (13 out of 16 fields)
- site_number
- site_name
- program_name
- rated_capacity
- system_size_kw
- inverter_status
- grid_energy_imported
- grid_energy_exported
- lifetime_production
- oem_name
- last_update_in_local_time
- last_updated_timestamp_utc

**EXCEPTIONS:**
- `zipPostalCode` (camelCase) - 1 field
- `state` (lowercase) - 1 field
- `timezone` (lowercase) - 1 field
- `SOC` (UPPERCASE) - 1 field (acronym)

---

## ✅ Recommendation

**Use `snake_case`** to match the majority convention:

```kql
'external_reference_id', coalesce(accountNumber, '-'),
```

This matches the pattern of:
- `site_number`
- `site_name`
- `oem_name`
- `last_updated_timestamp_utc`

---

## Why `snake_case`?

1. **Consistency**: 13 out of 16 fields use it
2. **Multi-word fields**: All other multi-word fields use snake_case
3. **Frontend expectation**: The parent ticket likely expects this format

---

## ✅ Final Answer

**Field name:** `external_reference_id` (snake_case)

**Not:**
- ❌ `externalReferenceId` (camelCase)
- ❌ `ExternalReferenceId` (PascalCase)
- ❌ `EXTERNAL_REFERENCE_ID` (UPPER_SNAKE_CASE)

