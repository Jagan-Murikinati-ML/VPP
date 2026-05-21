# Sorting Test Queries for All Columns

## Test 1: site_number (Ascending)
```kusto
getAllVppSitesByUserIdV2(
    inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", 
    page_index=0, 
    page_size=10,
    sorting=dynamic([{"field": "site_number", "direction": "asc"}])
)
```

## Test 2: site_number (Descending)
```kusto
getAllVppSitesByUserIdV2(
    inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", 
    page_index=0, 
    page_size=10,
    sorting=dynamic([{"field": "site_number", "direction": "desc"}])
)
```

## Test 3: site_name (Ascending)
```kusto
getAllVppSitesByUserIdV2(
    inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", 
    page_index=0, 
    page_size=10,
    sorting=dynamic([{"field": "site_name", "direction": "asc"}])
)
```

## Test 4: site_name (Descending)
```kusto
getAllVppSitesByUserIdV2(
    inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", 
    page_index=0, 
    page_size=10,
    sorting=dynamic([{"field": "site_name", "direction": "desc"}])
)
```

## Test 5: state (Ascending)
```kusto
getAllVppSitesByUserIdV2(
    inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", 
    page_index=0, 
    page_size=10,
    sorting=dynamic([{"field": "state", "direction": "asc"}])
)
```

## Test 6: state (Descending)
```kusto
getAllVppSitesByUserIdV2(
    inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", 
    page_index=0, 
    page_size=10,
    sorting=dynamic([{"field": "state", "direction": "desc"}])
)
```

## Test 7: zipPostalCode (Ascending)
```kusto
getAllVppSitesByUserIdV2(
    inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", 
    page_index=0, 
    page_size=10,
    sorting=dynamic([{"field": "zipPostalCode", "direction": "asc"}])
)
```

## Test 8: zipPostalCode (Descending)
```kusto
getAllVppSitesByUserIdV2(
    inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", 
    page_index=0, 
    page_size=10,
    sorting=dynamic([{"field": "zipPostalCode", "direction": "desc"}])
)
```

## Test 9: oem_name (Ascending)
```kusto
getAllVppSitesByUserIdV2(
    inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", 
    page_index=0, 
    page_size=10,
    sorting=dynamic([{"field": "oem_name", "direction": "asc"}])
)
```

## Test 10: oem_name (Descending)
```kusto
getAllVppSitesByUserIdV2(
    inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", 
    page_index=0, 
    page_size=10,
    sorting=dynamic([{"field": "oem_name", "direction": "desc"}])
)
```

## Test 11: external_reference_id (Ascending)
```kusto
getAllVppSitesByUserIdV2(
    inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", 
    page_index=0, 
    page_size=10,
    sorting=dynamic([{"field": "external_reference_id", "direction": "asc"}])
)
```

## Test 12: external_reference_id (Descending)
```kusto
getAllVppSitesByUserIdV2(
    inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", 
    page_index=0, 
    page_size=10,
    sorting=dynamic([{"field": "external_reference_id", "direction": "desc"}])
)
```
