# Two-Function Architecture - Detailed Explanation
## Ticket 20099: How Splitting Functions Actually Works

---

## 🤔 **Your Question**

> "To fetch telemetry, we need siteIds right? And these siteIds come from those joins.
> So how does splitting work? Does frontend call twice, or backend handles it?"

**EXCELLENT question!** This is the key to understanding the architecture.

---

## 📊 **THE ANSWER: Frontend Calls TWICE (Two Separate API Calls)**

### **Flow Diagram:**

```
USER CLICKS "VPP Sites Page"
        ↓
┌───────────────────────────────────────────────────────────────┐
│ FRONTEND: Call 1 - Get Lightweight List                       │
│                                                                │
│ GET /api/vpp-sites-lightweight                                 │
│ {                                                              │
│   userId: "abc123",                                            │
│   page: 0,                                                     │
│   pageSize: 50,                                                │
│   filters: [...],                                              │
│   sorting: [...]                                               │
│ }                                                              │
└───────────────────────────────────────────────────────────────┘
        ↓
┌───────────────────────────────────────────────────────────────┐
│ BACKEND: Function 1 - getAllVppSitesListLightweight()         │
│                                                                │
│ 1. User mapping (get all sites for user)                      │
│ 2. VPP filter (only VPP registered sites)                     │
│ 3. Fetch MINIMAL properties (name, state, etc.)               │
│ 4. Apply filters, sorting, search                             │
│ 5. Paginate (get 50 site IDs)                                 │
│ 6. Return lightweight data                                    │
│                                                                │
│ ⏱️ Time: ~600-900ms                                            │
└───────────────────────────────────────────────────────────────┘
        ↓
┌───────────────────────────────────────────────────────────────┐
│ RESPONSE 1: Lightweight List                                  │
│                                                                │
│ {                                                              │
│   data: [                                                      │
│     {                                                          │
│       site_number: "400012345",                                │
│       site_name: "John's Home Solar",                          │
│       state: "CA",                                             │
│       external_reference_id: "APPTPO-123",                     │
│       program_name: ["DSGS", "LEAP"]                           │
│     },                                                         │
│     ... 49 more sites ...                                      │
│   ],                                                           │
│   metadata: { total: 5000, page: 0, pageSize: 50 }            │
│ }                                                              │
└───────────────────────────────────────────────────────────────┘
        ↓
┌───────────────────────────────────────────────────────────────┐
│ FRONTEND: IMMEDIATELY RENDERS TABLE                           │
│                                                                │
│ ┌─────────────────────────────────────────────────────┐       │
│ │ Site ID       │ Name           │ State │ Program    │       │
│ ├─────────────────────────────────────────────────────┤       │
│ │ 400012345     │ John's Home    │ CA    │ DSGS,LEAP  │       │
│ │ 400012346     │ Mary's Solar   │ TX    │ DSGS       │       │
│ │ ...                                                  │       │
│ └─────────────────────────────────────────────────────┘       │
│                                                                │
│ ✅ USER SEES LIST IN < 1 SECOND!                              │
│                                                                │
│ THEN FRONTEND EXTRACTS SITE IDs: ["400012345", "400012346"...]│
└───────────────────────────────────────────────────────────────┘
        ↓
┌───────────────────────────────────────────────────────────────┐
│ FRONTEND: Call 2 - Get Telemetry Details (ASYNC)              │
│                                                                │
│ POST /api/vpp-sites-details                                    │
│ {                                                              │
│   siteIds: ["400012345", "400012346", ... (50 IDs)]           │
│ }                                                              │
└───────────────────────────────────────────────────────────────┘
        ↓
┌───────────────────────────────────────────────────────────────┐
│ BACKEND: Function 2 - getVppSitesDetails()                    │
│                                                                │
│ 1. Receive array of 50 site IDs                               │
│ 2. Fetch telemetry for ONLY these 50 sites                    │
│ 3. Fetch device data for ONLY these 50 sites                  │
│ 4. Fetch timezone for ONLY these 50 sites                     │
│ 5. Return detailed data                                       │
│                                                                │
│ ⏱️ Time: ~400-600ms (MUCH FASTER - only 50 sites!)            │
└───────────────────────────────────────────────────────────────┘
        ↓
┌───────────────────────────────────────────────────────────────┐
│ RESPONSE 2: Detailed Data                                     │
│                                                                │
│ {                                                              │
│   data: [                                                      │
│     {                                                          │
│       site_number: "400012345",                                │
│       SOC: 85.5,                                               │
│       rated_capacity: 13.5,                                    │
│       system_size_kw: 10.2,                                    │
│       inverter_status: true,                                   │
│       grid_energy_imported: 12345.67,                          │
│       grid_energy_exported: 23456.78,                          │
│       last_update_in_local_time: "2026-06-22 14:30:00",       │
│       timezone: "America/Los_Angeles"                          │
│     },                                                         │
│     ... 49 more sites ...                                      │
│   ]                                                            │
│ }                                                              │
└───────────────────────────────────────────────────────────────┘
        ↓
┌───────────────────────────────────────────────────────────────┐
│ FRONTEND: PATCHES DATA INTO EXISTING ROWS                     │
│                                                                │
│ ┌──────────────────────────────────────────────────────────┐  │
│ │ Site ID  │ Name     │ SOC  │ Capacity │ Status │ ...    │  │
│ ├──────────────────────────────────────────────────────────┤  │
│ │ 40001234 │ John's   │ 85%  │ 13.5kW   │ Online │ ...    │  │
│ │ 40001235 │ Mary's   │ 92%  │ 10.0kW   │ Online │ ...    │  │
│ │ ...                                                       │  │
│ └──────────────────────────────────────────────────────────┘  │
│                                                                │
│ ✅ FULL DATA VISIBLE AFTER +500ms MORE                        │
│                                                                │
│ TOTAL USER WAIT: ~1.5 seconds (feels much faster!)            │
└───────────────────────────────────────────────────────────────┘
```

---

## 💡 **KEY INSIGHT: Frontend Makes TWO Calls**

### **Call 1: Lightweight (Blocking)**
- User waits for this
- Shows skeleton/spinner
- **FAST:** ~600-900ms
- User sees list immediately

### **Call 2: Details (Non-blocking/Async)**
- Happens in background AFTER table renders
- User can already scroll, click, interact with list
- **Slower but feels fast:** ~400-600ms
- Data "pops in" after load

**Total: ~1.5 seconds, but FEELS like <1 second!** 🎯

---

## 🔧 **BACKEND: You Create TWO Separate Functions**

### **Function 1: Lightweight**

```kql
.create-or-alter function getAllVppSitesListLightweight(
    inputUserId: string = "",
    page_index: int = 0,
    page_size: int = 50,
    sorting: dynamic = dynamic([]),
    filters: dynamic = dynamic([]),
    searchText: string = ""
) {
    // PHASE 1: Get user's sites
    let site_ids_from_user = toscalar(
        getCurrentUserSiteMapping(inputUserId) 
        | project list_site_ids
    );
    
    // PHASE 2: Filter to VPP sites only
    let vppSites = goldAdtPropertyMinMaxLatestViewV2
        | where Id in (site_ids_from_user)
        | where Key == 'isVppRegistered' and tolower(valueMax) == 'true'
        | summarize make_list(Id);
    
    // PHASE 3: Get MINIMAL properties (ONLY for filtering/sorting)
    let site_properties = goldAdtPropertyMinMaxLatestViewV2
        | where Id in (vppSites)
        | where Key in ('siteName', 'address.stateProvince', 
                       'assetRegistrationInfo.accountNumber')
        | summarize 
            siteName = take_anyif(valueMax, Key == 'siteName'),
            state = take_anyif(valueMax, Key == 'address.stateProvince'),
            accountNumber = take_anyif(valueMax, Key == 'assetRegistrationInfo.accountNumber')
        by siteId = Id;
    
    // PHASE 4: Get program names (if needed for display)
    let programs = GetLatestProgramSiteInfo
        | where site_id in (vppSites)
        | join kind=inner GetLatestProgramInfo on program_id
        | summarize program_name = make_set(program_name) by site_id;
    
    // PHASE 5: Combine minimal data
    let all_sites = site_properties
        | join kind=leftouter programs on $left.siteId == $right.site_id
        | project siteId, siteName, state, accountNumber, 
                 program_name = coalesce(program_name, dynamic([]));
    
    // PHASE 6: Apply search
    let searched = all_sites
        | where isempty(searchText) or 
               (siteId contains searchText or
                siteName contains searchText or
                state contains searchText);
    
    // PHASE 7: Apply filters
    let filtered = searched | where /* filter logic */;
    
    // PHASE 8: Apply sorting
    let sorted = filtered | order by /* sort logic */;
    
    // PHASE 9: Paginate
    let paginated = sorted
        | serialize rank = row_number()
        | where rank > page_index * page_size 
            and rank <= (page_index + 1) * page_size;
    
    // PHASE 10: Format response
    let total_count = toscalar(filtered | count);
    
    paginated
    | project 
        site_number = siteId,
        site_name = siteName,
        state,
        external_reference_id = accountNumber,
        program_name
    | summarize data = make_list(pack_all())
    | extend metadata = pack('page', page_index, 
                            'pageSize', page_size, 
                            'total', total_count)
    | project metadata, data;
}
```

**What it does NOT fetch:**
- ❌ No telemetry (`silverCommDataSite`) → saves ~500ms
- ❌ No device data (battery, inverter) → saves ~300ms
- ❌ No timezone → saves ~100ms

---

### **Function 2: Details**

```kql
.create-or-alter function getVppSitesDetails(
    siteIds: dynamic  // Array of site IDs like ["400012345", "400012346", ...]
) {
    // PHASE 1: Get timezone (needed for telemetry local time)
    let timezones = goldAdtPropertyMinMaxLatestViewV2
        | where Id in (siteIds)
        | where Key == 'address.location.timeZone'
        | project siteId = Id, 
                 timezone = valueMax;
    
    // PHASE 2: Get telemetry data
    let telemetry = silverCommDataSite
        | where siteId in (siteIds)  // ← ONLY 50 sites!
        | summarize arg_max(sourceTimestamp, *) by siteId
        | join kind=leftouter timezones on siteId
        | extend localTime = datetime_utc_to_local(sourceTimestamp, timezone)
        | project siteId,
                 SOC = battery_713_SoC,
                 grid_energy_imported = grid_200_IncWhImp,
                 grid_energy_exported = grid_200_IncWhExp,
                 inverter_status = sourceTimestamp > ago(1h),
                 last_update_in_local_time = localTime,
                 last_updated_timestamp_utc = sourceTimestamp,
                 timezone;
    
    // PHASE 3: Get device relationships
    let devices = goldAdtAllRelationshipsLatestView
        | where Source in (siteIds)  // ← ONLY 50 sites!
        | where Name in ("hasDevice", "hasSystemInfo")
        | project siteId = Source, deviceId = Target, Name;
    
    // PHASE 4: Get rated capacity
    let capacity = goldAdtPropertyMinMaxLatestViewV2
        | where Key == 'nameplateInfo.wMaxRtg'
        | lookup kind=inner (devices | where Name == 'hasDevice') 
            on $left.Id == $right.deviceId
        | summarize rated_capacity = any(valueMax) by siteId;
    
    // PHASE 5: Get system size
    let systemSize = goldAdtPropertyMinMaxLatestViewV2
        | where Key == 'systemSizeKw'
        | lookup kind=inner (devices | where Name == 'hasSystemInfo')
            on $left.Id == $right.deviceId
        | summarize system_size_kw = any(valueMax) by siteId;
    
    // PHASE 6: Combine all details
    telemetry
    | join kind=leftouter capacity on siteId
    | join kind=leftouter systemSize on siteId
    | project 
        site_number = siteId,
        SOC,
        rated_capacity,
        system_size_kw,
        inverter_status,
        grid_energy_imported,
        grid_energy_exported,
        last_update_in_local_time,
        last_updated_timestamp_utc,
        timezone
    | summarize data = make_list(pack_all())
    | project data;
}
```

**What makes it fast:**
- ✅ Input is ONLY 50 site IDs (not 5,000!)
- ✅ No user mapping needed
- ✅ No VPP filtering needed
- ✅ No pagination needed
- ✅ Straight fetch → ~400-600ms

---

## 🌐 **FRONTEND: How to Call These Functions**

### **React/TypeScript Example:**

```typescript
// VPPSitesPage.tsx

const VPPSitesPage = () => {
  const [lightweightData, setLightweightData] = useState([]);
  const [detailsData, setDetailsData] = useState({});
  const [loading, setLoading] = useState(true);
  const [detailsLoading, setDetailsLoading] = useState(false);

  useEffect(() => {
    loadSites();
  }, [page, filters, sorting]);

  const loadSites = async () => {
    // CALL 1: Get lightweight list
    setLoading(true);
    
    const response1 = await fetch('/api/vpp-sites-lightweight', {
      method: 'POST',
      body: JSON.stringify({
        userId: currentUser.id,
        page: 0,
        pageSize: 50,
        filters: filters,
        sorting: sorting
      })
    });
    
    const lightData = await response1.json();
    setLightweightData(lightData.data);
    setLoading(false);
    
    // ✅ TABLE RENDERS NOW! User can see list!
    
    // CALL 2: Get details in background (async)
    setDetailsLoading(true);
    
    const siteIds = lightData.data.map(site => site.site_number);
    
    const response2 = await fetch('/api/vpp-sites-details', {
      method: 'POST',
      body: JSON.stringify({
        siteIds: siteIds
      })
    });
    
    const details = await response2.json();
    
    // Convert array to map for easy lookup
    const detailsMap = {};
    details.data.forEach(detail => {
      detailsMap[detail.site_number] = detail;
    });
    
    setDetailsData(detailsMap);
    setDetailsLoading(false);
  };

  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>Site ID</TableCell>
          <TableCell>Name</TableCell>
          <TableCell>State</TableCell>
          <TableCell>SOC</TableCell>
          <TableCell>Status</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {lightweightData.map(site => {
          const details = detailsData[site.site_number];
          
          return (
            <TableRow key={site.site_number}>
              <TableCell>{site.site_number}</TableCell>
              <TableCell>{site.site_name}</TableCell>
              <TableCell>{site.state}</TableCell>
              <TableCell>
                {details ? (
                  `${details.SOC}%`
                ) : (
                  <Skeleton width={40} />  {/* Loading placeholder */}
                )}
              </TableCell>
              <TableCell>
                {details ? (
                  details.inverter_status ? 'Online' : 'Offline'
                ) : (
                  <Skeleton width={60} />
                )}
              </TableCell>
            </TableRow>
          );
        })}
      </TableBody>
    </Table>
  );
};
```

---

## ⏱️ **PERFORMANCE COMPARISON**

### **OLD: Single Function Approach**

```
User clicks → Wait 3-4 seconds → Table appears with all data
│←────────────── 3-4 seconds ──────────────→│
                                             ✅ Table visible
```

**User perception: "This is SLOW!"** ❌

---

### **NEW: Two Function Approach**

```
User clicks → Wait 0.9s → Table appears → Wait 0.5s → Details pop in
│←─ 0.9s ─→│               │←─ 0.5s ─→│
           ✅ List visible              ✅ Full data visible
```

**User perception: "This is FAST!"** ✅

**Why it feels faster:**
1. User sees SOMETHING in <1 second (psychological threshold)
2. User can scroll, interact while details load
3. Total time (1.4s) is FASTER than old approach (3-4s)

---

## 🎯 **SUMMARY: Who Does What?**

| Responsibility | Who Handles It? |
|---------------|-----------------|
| **Create Function 1 (lightweight)** | ✅ Backend (You) |
| **Create Function 2 (details)** | ✅ Backend (You) |
| **Call Function 1 first** | ✅ Frontend |
| **Extract site IDs from response** | ✅ Frontend |
| **Call Function 2 with site IDs** | ✅ Frontend |
| **Merge/patch data together** | ✅ Frontend |
| **User mapping (joins)** | ✅ Backend (Function 1 ONLY) |
| **VPP filtering (joins)** | ✅ Backend (Function 1 ONLY) |
| **Telemetry fetch** | ✅ Backend (Function 2 ONLY) |

---

## ✅ **YOUR JOB (Backend Engineer):**

1. ✅ Create `getAllVppSitesListLightweight()` function
   - Do ALL the user mapping joins
   - Do VPP filtering
   - Do filter/sort/search/pagination
   - Return lightweight data (5 fields)
   - Target: <1 second

2. ✅ Create `getVppSitesDetails()` function
   - Input: Array of site IDs
   - Fetch telemetry for ONLY those IDs
   - Fetch device data for ONLY those IDs
   - Return detailed data (9 fields)
   - Target: <600ms

3. ✅ The site IDs are passed FROM Function 1 response TO Function 2 BY Frontend

**You do NOT handle calling Function 2 from Function 1. Frontend does that!** 🎯

---

**Does this clarify the architecture?** 🚀

---

## 📝 **PRACTICAL EXAMPLE: Step-by-Step Data Flow**

Let's trace a real request:

### **Step 1: User Opens VPP Sites Page**

Frontend sends:
```json
POST /api/kusto/getAllVppSitesListLightweight
{
  "inputUserId": "abc-123",
  "page_index": 0,
  "page_size": 10,
  "filters": [{"field": "state", "op": "==", "value": "CA"}],
  "sorting": [{"field": "site_name", "direction": "asc"}]
}
```

---

### **Step 2: Function 1 Executes (Backend)**

```
1. User mapping joins → Get 5,000 site IDs for user
2. VPP filter → Reduce to 3,000 VPP sites
3. Fetch minimal properties for 3,000 sites
4. Apply CA filter → Reduce to 500 sites
5. Sort by site name
6. Paginate → Get first 10 sites
7. Return lightweight data
```

Function 1 returns:
```json
{
  "metadata": {
    "page": 0,
    "pageSize": 10,
    "total": 500
  },
  "data": [
    {
      "site_number": "400012345",
      "site_name": "Alice Solar",
      "state": "CA",
      "external_reference_id": "APPTPO-123",
      "program_name": ["DSGS"]
    },
    {
      "site_number": "400012346",
      "site_name": "Bob's Home",
      "state": "CA",
      "external_reference_id": "APPTPO-456",
      "program_name": ["LEAP"]
    },
    ... 8 more sites ...
  ]
}
```

⏱️ **Time: 850ms**

---

### **Step 3: Frontend Renders Table Immediately**

```html
<table>
  <tr>
    <td>400012345</td>
    <td>Alice Solar</td>
    <td>CA</td>
    <td>Loading...</td>  <!-- SOC not loaded yet -->
    <td>Loading...</td>  <!-- Status not loaded yet -->
  </tr>
  <tr>
    <td>400012346</td>
    <td>Bob's Home</td>
    <td>CA</td>
    <td>Loading...</td>
    <td>Loading...</td>
  </tr>
  ...
</table>
```

✅ **User sees table in 850ms!**

---

### **Step 4: Frontend Extracts Site IDs**

```javascript
const siteIds = response.data.map(site => site.site_number);
// Result: ["400012345", "400012346", ..., "400012354"]
```

---

### **Step 5: Frontend Calls Function 2**

Frontend sends:
```json
POST /api/kusto/getVppSitesDetails
{
  "siteIds": [
    "400012345",
    "400012346",
    "400012347",
    "400012348",
    "400012349",
    "400012350",
    "400012351",
    "400012352",
    "400012353",
    "400012354"
  ]
}
```

---

### **Step 6: Function 2 Executes (Backend)**

```
1. Receive 10 site IDs
2. Fetch telemetry for ONLY these 10 sites → 200ms
3. Fetch device data for ONLY these 10 sites → 150ms
4. Fetch timezone for ONLY these 10 sites → 50ms
5. Combine and return
```

Function 2 returns:
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
      "last_update_in_local_time": "2026-06-22 14:30:00",
      "timezone": "America/Los_Angeles"
    },
    {
      "site_number": "400012346",
      "SOC": 92.3,
      "rated_capacity": 10.0,
      ...
    },
    ... 8 more sites ...
  ]
}
```

⏱️ **Time: 420ms**

---

### **Step 7: Frontend Merges Data**

```javascript
// Create lookup map
const detailsMap = {};
detailsResponse.data.forEach(detail => {
  detailsMap[detail.site_number] = detail;
});

// Merge with lightweight data
const mergedData = lightweightData.map(site => ({
  ...site,
  ...detailsMap[site.site_number]
}));

// Result:
[
  {
    site_number: "400012345",
    site_name: "Alice Solar",
    state: "CA",
    external_reference_id: "APPTPO-123",
    program_name: ["DSGS"],
    SOC: 85.5,  // ← From Function 2
    rated_capacity: 13.5,  // ← From Function 2
    inverter_status: true,  // ← From Function 2
    ...
  },
  ...
]
```

---

### **Step 8: Frontend Updates Table**

```html
<table>
  <tr>
    <td>400012345</td>
    <td>Alice Solar</td>
    <td>CA</td>
    <td>85.5%</td>     <!-- ✅ Updated! -->
    <td>Online</td>    <!-- ✅ Updated! -->
  </tr>
  <tr>
    <td>400012346</td>
    <td>Bob's Home</td>
    <td>CA</td>
    <td>92.3%</td>     <!-- ✅ Updated! -->
    <td>Online</td>    <!-- ✅ Updated! -->
  </tr>
  ...
</table>
```

✅ **Full data visible in 850ms + 420ms = 1,270ms total!**

---

## 🎯 **KEY TAKEAWAYS**

### **1. Backend Creates TWO Independent Functions**

Function 1: Does ALL the joins (user mapping, VPP filter, etc.)
Function 2: Takes site IDs as input (NO joins needed)

### **2. Frontend Orchestrates the Calls**

```
Frontend → Call Function 1 → Get site IDs → Call Function 2 → Merge data
```

### **3. Site IDs Flow:**

```
User mapping joins → VPP filter → Pagination → Site IDs → Function 2
     (Function 1)                                              ↓
                                                          Telemetry fetch
```

### **4. You (Backend) Do NOT Call Function 2 from Function 1**

- ❌ Function 1 does NOT call Function 2
- ❌ Function 1 does NOT fetch telemetry
- ✅ Function 1 ONLY returns site IDs + lightweight data
- ✅ Frontend extracts site IDs from Function 1 response
- ✅ Frontend calls Function 2 with those site IDs

### **5. Performance Breakdown**

| Operation | Time | Where |
|-----------|------|-------|
| User mapping joins | ~200ms | Function 1 |
| VPP filtering | ~200ms | Function 1 |
| Minimal properties | ~300ms | Function 1 |
| Filter/sort/search | ~150ms | Function 1 |
| **Function 1 TOTAL** | **~850ms** | ✅ |
| Telemetry (10 sites) | ~200ms | Function 2 |
| Device data (10 sites) | ~150ms | Function 2 |
| Timezone (10 sites) | ~50ms | Function 2 |
| **Function 2 TOTAL** | **~420ms** | ✅ |
| **GRAND TOTAL** | **~1,270ms** | 🎯 |

**But user sees list in 850ms, so it FEELS fast!** ⚡

---

## ❓ **FAQ: Common Questions**

### **Q1: Why not call Function 2 from inside Function 1?**

**A:** Because then it would be slow again! The whole point is to return lightweight data FAST, then fetch heavy data separately.

### **Q2: Won't this use more resources (two API calls)?**

**A:** Actually NO!
- Old way: Fetch telemetry for ALL 5,000 sites, then filter → HUGE waste
- New way: Fetch telemetry for ONLY 10 paginated sites → Much less data

### **Q3: What if user changes page?**

**A:** Same flow:
1. Frontend calls Function 1 with page=1
2. Gets next 10 site IDs
3. Calls Function 2 with those 10 IDs
4. Renders

### **Q4: Do we need to fetch telemetry EVERY time?**

**A:** Yes, because telemetry changes frequently (SOC, inverter status, etc.). But since it's only 10 sites, it's fast!

### **Q5: Can we cache Function 1 results?**

**A:** Potentially yes! Lightweight data (site name, state) doesn't change often, so you could cache for 5-10 minutes. Telemetry should NOT be cached.

---

**Now you understand the complete architecture!** 🚀
