# Ticket 18209 - Bug Analysis: Filtering and Sorting Issues

## Summary
Two bugs found in `getAllVppSitesByUserIdV2` function affecting the Resources page:
1. **CONTAINS filter bug** - Shows all records instead of no results when filter doesn't match
2. **Sorting bug** - Descending sort for program_name column not working correctly

---

## Bug 1: CONTAINS Filter (Metadata Issue)

### Issue
When searching with text that doesn't match any records (e.g., "zzzzz"), the function returns:
- `data: []` (correct - no records)
- `total_count: 0` (correct - no matching records)
- `total_records_count: 679` (WRONG - should be 0)
- `status: 404` (correct)

The UI likely uses `total_records_count` to decide whether to show results, causing it to display all 679 records instead of showing "no results".

### Root Cause
**Function:** `getAllVppSitesByUserIdV2`  
**Line:** 110

```kusto
let total_records_count = toscalar(all_sites_basic | count);
```

This calculates total count BEFORE applying search filters, so it always returns the total number of sites (679) regardless of search results.

### The Fix
**Change line 110 to:**
```kusto
let total_records_count = total_count;
```

This will return 0 when no records match the search, which will correctly tell the UI to show "no results".

### Test Case
```kusto
getAllVppSitesByUserIdV2(
    inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", 
    page_index=0, 
    page_size=10,
    searchText="zzzzz"
)
```


**Expected result after fix:**
```json
{
  "metadata": {
    "pagination": {
      "total_count": 0,
      "total_records_count": 0  // Fixed - was 679
    }
  },
  "data": [],
  "status": 404
}
```

**Test file:** `zzz.csv.csv`

---

## Bug 2: Sorting (program_name Column)

### Issue
The `program_name` column contains arrays of strings like `["Program A", "Program B"]`. When sorting:

**Ascending sort:** Seems to work (but uses JSON string representation)
**Descending sort:** Empty arrays appear FIRST instead of LAST

### Test Results

**Ascending test:** `ascending_test.csv`
```
Site 1: program_name = ["20 Aug 2025 ", "ArbitrageDateValidation Check"]
Site 2: program_name = ["61512KT", "Arbitrage Program Y ", "TestingdNet2"]
...
```

**Descending test:** `descending_test.csv`
```
Site 1: program_name = []  (empty - WRONG! Should be last)
Site 2: program_name = []  (empty)
Site 3: program_name = []  (empty)
...
```

### Root Cause
**Function:** `getAllVppSitesByUserIdV2`  
**Line:** 187

```kusto
sort_field == "program_name", tostring(program_name),
```

This converts the array to a JSON string representation like `'["Program A","Program B"]'`, which:
1. Sorts by character-by-character comparison of the JSON string
2. Empty arrays `[]` always sort to the same position in both ASC and DESC

### The Fix

**Option 1: Sort by first element (simple)**
```kusto
sort_field == "program_name", tostring(iff(array_length(program_name) > 0, program_name[0], "")),
```

**Option 2: Sort by all elements joined (recommended)**
```kusto
sort_field == "program_name", strcat_array(program_name, ", "),
```

**Recommended:** Option 2 because:
- Handles multiple programs better
- Natural alphabetical sorting
- Empty arrays correctly go first (ASC) or last (DESC)

### Test Cases

```kusto
// Ascending
getAllVppSitesByUserIdV2(
    inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", 
    page_index=0, 
    page_size=10,
    sorting=dynamic([{"field": "program_name", "direction": "asc"}])
)

// Descending
getAllVppSitesByUserIdV2(
    inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", 
    page_index=0, 
    page_size=10,
    sorting=dynamic([{"field": "program_name", "direction": "desc"}])
)
```

---

## Additional Testing Needed

Test sorting for other columns to confirm the bug is specific to `program_name`:
- `site_number` (ASC/DESC)
- `site_name` (ASC/DESC)
- `state` (ASC/DESC)
- `oem_name` (ASC/DESC)
- `external_reference_id` (ASC/DESC)

**See:** `SORTING_TEST_QUERIES.md` for all test queries

---

## Files in This Ticket

- `ticket.md` - Original bug report
- `BUG_ANALYSIS.md` - This file
- `getAllVppSitesByUserIdV2.kql` - Current function code (with bugs)
- `zzz.csv.csv` - Test result for filter with "zzzzz" (shows bug 1)
- `ascending_test.csv` - Test result for ascending sort on program_name
- `descending_test.csv` - Test result for descending sort on program_name (shows bug 2)
- `SORTING_TEST_QUERIES.md` - Test queries for all sortable columns

---

## Next Steps

1. ✅ Test other columns to confirm sorting bug scope
2. ✅ Apply both fixes to the function
3. ✅ Test in DEV environment
4. ✅ Verify UI displays correctly
5. ✅ Deploy to PROD
