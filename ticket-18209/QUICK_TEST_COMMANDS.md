# Quick Test Commands - Copy & Paste

## Priority Tests (Test These First)

### 1. site_name ASC
```kusto
getAllVppSitesByUserIdV2(inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", page_index=0, page_size=10, sorting=dynamic([{"field": "site_name", "direction": "asc"}]))
```
**Save as:** `site_name_asc.csv`

### 2. site_name DESC
```kusto
getAllVppSitesByUserIdV2(inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", page_index=0, page_size=10, sorting=dynamic([{"field": "site_name", "direction": "desc"}]))
```
**Save as:** `site_name_desc.csv`

### 3. oem_name ASC
```kusto
getAllVppSitesByUserIdV2(inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", page_index=0, page_size=10, sorting=dynamic([{"field": "oem_name", "direction": "asc"}]))
```
**Save as:** `oem_name_asc.csv`

### 4. oem_name DESC
```kusto
getAllVppSitesByUserIdV2(inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", page_index=0, page_size=10, sorting=dynamic([{"field": "oem_name", "direction": "desc"}]))
```
**Save as:** `oem_name_desc.csv`

### 5. state ASC
```kusto
getAllVppSitesByUserIdV2(inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", page_index=0, page_size=10, sorting=dynamic([{"field": "state", "direction": "asc"}]))
```
**Save as:** `state_asc.csv`

### 6. state DESC
```kusto
getAllVppSitesByUserIdV2(inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", page_index=0, page_size=10, sorting=dynamic([{"field": "state", "direction": "desc"}]))
```
**Save as:** `state_desc.csv`

---

## What to Look For

**For each ASC test:**
- Check if first record has smallest/earliest value
- Check if empty values appear at the top

**For each DESC test:**
- Check if first record has largest/latest value
- Check if empty values appear at the bottom (NOT at the top)

**Quick Check:**
Compare first record of ASC with last record of DESC - should they be similar?

---

## Expected Results

### site_name
- **ASC:** Empty names first, then "" → "A..." → "Z..."
- **DESC:** "Z..." → "A..." → "" → Empty names last

### oem_name
- **ASC:** "Enphase" → "SolarEdge" → "Tesla" (alphabetical)
- **DESC:** "Tesla" → "SolarEdge" → "Enphase" (reverse)

### state
- **ASC:** "CA" → Other states (if any)
- **DESC:** Other states (if any) → "CA"

---

## Decision Tree

```
Run site_name ASC/DESC tests
    ↓
DESC works correctly?
    ↓
YES → Bug is specific to program_name (array issue)
NO → Bug affects all DESC sorts (general sorting issue)
```
