# Ticket 20099 - Quick Start Guide
## Two-Function Architecture Implementation

---

## 📋 **TL;DR**

**Goal:** Split slow `getAllVppSitesByUserIdV2` into TWO fast functions

**Function 1:** Lightweight list (site names, states) → <1 second  
**Function 2:** Heavy details (telemetry, battery) → <600ms  

**Total:** ~1.5 seconds (vs. current 3-4 seconds) ✅

**Frontend:** Calls both functions, merges data

---

## 📂 **Documentation**

| File | Read This If... |
|------|----------------|
| **QUICK_START_GUIDE.md** | You want the summary (this file) |
| **TWO_FUNCTION_ARCHITECTURE_EXPLAINED.md** | You want to understand HOW it works |
| **WHY_TWO_FUNCTIONS_ARE_BETTER.md** | You want to understand WHY it's better |
| **original_code.kql** | You want to see current V2 code |
| **ticket.md** | You want to see original request |

---

## 🎯 **Your Question Answered**

### **Q: "How does splitting work? Does frontend call twice, or backend handles it?"**

**A: Frontend calls TWICE (two separate API calls)**

```
Step 1: Frontend calls Function 1
        ↓
Step 2: Function 1 returns site IDs + lightweight data
        ↓
Step 3: Frontend extracts site IDs from response
        ↓
Step 4: Frontend calls Function 2 with those site IDs
        ↓
Step 5: Function 2 returns telemetry details
        ↓
Step 6: Frontend merges data and displays
```

**You (backend) do NOT call Function 2 from Function 1!**

---

## 🔧 **What You Need to Build**

### **Function 1: getAllVppSitesListLightweight**

**Input:**
```javascript
{
  inputUserId: "abc-123",
  page_index: 0,
  page_size: 50,
  filters: [...],
  sorting: [...],
  searchText: "..."
}
```

**Output:**
```javascript
{
  metadata: { page: 0, pageSize: 50, total: 5000 },
  data: [
    {
      site_number: "400012345",
      site_name: "John's Solar",
      state: "CA",
      external_reference_id: "APPTPO-123",
      program_name: ["DSGS", "LEAP"]
    },
    ... 49 more ...
  ]
}
```

**What it does:**
1. ✅ User mapping (get user's sites)
2. ✅ VPP filtering
3. ✅ Fetch minimal properties (5 fields)
4. ✅ Apply filters, sorting, search
5. ✅ Paginate
6. ❌ NO telemetry
7. ❌ NO device data

**Target: <1 second**

---

### **Function 2: getVppSitesDetails**

**Input:**
```javascript
{
  siteIds: [
    "400012345",
    "400012346",
    ... (typically 10-50 IDs)
  ]
}
```

**Output:**
```javascript
{
  data: [
    {
      site_number: "400012345",
      SOC: 85.5,
      rated_capacity: 13.5,
      system_size_kw: 10.2,
      inverter_status: true,
      grid_energy_imported: 12345.67,
      grid_energy_exported: 23456.78,
      last_update_in_local_time: "2026-06-22 14:30:00",
      timezone: "America/Los_Angeles"
    },
    ... 49 more ...
  ]
}
```

**What it does:**
1. ✅ Fetch telemetry for ONLY input site IDs
2. ✅ Fetch device data for ONLY input site IDs
3. ✅ Fetch timezone for ONLY input site IDs
4. ❌ NO user mapping
5. ❌ NO VPP filtering
6. ❌ NO pagination

**Target: <600ms**

---

## ⚡ **Key Optimizations**

### **Function 1:**

1. **Use helper function for user mapping**
   ```kql
   let site_ids = toscalar(getCurrentUserSiteMapping(inputUserId) | project list_site_ids);
   ```
   Saves: ~600ms

2. **Fetch MINIMAL properties only**
   ```kql
   | where Key in ('siteName', 'address.stateProvince', 'assetRegistrationInfo.accountNumber')
   ```
   Saves: ~300ms

3. **Skip telemetry completely**
   Saves: ~1,500ms

4. **Skip device data completely**
   Saves: ~800ms

**Total savings: ~3,200ms!**

---

### **Function 2:**

1. **Only fetch for paginated sites (50 instead of 5,000)**
   ```kql
   | where siteId in (siteIds)  // Only 50 sites!
   ```
   Saves: ~1,500ms

2. **No user mapping needed** (site IDs already provided)
   Saves: ~800ms

3. **No filtering/sorting needed** (already done)
   Saves: ~400ms

**Total savings: ~2,700ms!**

---

## 📊 **Performance Breakdown**

| Operation | Time | Function |
|-----------|------|----------|
| User mapping | ~200ms | Function 1 |
| VPP filtering | ~200ms | Function 1 |
| Minimal properties | ~300ms | Function 1 |
| Programs | ~400ms | Function 1 |
| Filter/sort/search | ~400ms | Function 1 |
| **Function 1 TOTAL** | **~1,500ms** | ✅ |
| Telemetry (50 sites) | ~200ms | Function 2 |
| Device data (50 sites) | ~150ms | Function 2 |
| Timezone (50 sites) | ~50ms | Function 2 |
| **Function 2 TOTAL** | **~400ms** | ✅ |
| **GRAND TOTAL** | **~1,900ms** | 🎯 |

**User sees list in 1.5s, feels like <1s!**

---

## 🌐 **Frontend Integration**

**React Example:**

```typescript
const loadSites = async () => {
  // Call 1: Get lightweight list
  const response1 = await api.post('/getAllVppSitesListLightweight', {
    userId: currentUser.id,
    page: 0,
    pageSize: 50
  });
  
  setLightweightData(response1.data);
  // ✅ Table renders NOW!
  
  // Call 2: Get details
  const siteIds = response1.data.map(s => s.site_number);
  const response2 = await api.post('/getVppSitesDetails', { siteIds });
  
  setDetailsData(response2.data);
  // ✅ Details patch in!
};
```

---

## ✅ **Implementation Checklist**

### **Phase 1: Function 1 (Lightweight)**
- [ ] Create `getAllVppSitesListLightweight()` function
- [ ] Use `getCurrentUserSiteMapping()` helper
- [ ] Fetch only 5 properties (name, state, ref_id, program)
- [ ] Implement filter/sort/search logic
- [ ] Test performance (<1s target)

### **Phase 2: Function 2 (Details)**
- [ ] Create `getVppSitesDetails()` function
- [ ] Accept array of site IDs as input
- [ ] Fetch telemetry for input sites only
- [ ] Fetch device data for input sites only
- [ ] Test performance (<600ms target)

### **Phase 3: Integration**
- [ ] Deploy both functions to DEV
- [ ] Coordinate with frontend team
- [ ] Test two-call flow
- [ ] Measure end-to-end performance
- [ ] Deploy to QA, then PROD

---

## 🎯 **Success Criteria**

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Function 1 performance | N/A | <1 second | ⏳ |
| Function 2 performance | N/A | <600ms | ⏳ |
| Total time to full data | 3-4s | <2s | ⏳ |
| Time to see list | 3-4s | <1s | ⏳ |
| User satisfaction | Low | High | ⏳ |

---

## 📞 **Key Contacts**

- **Frontend Team:** Need to coordinate two-call integration
- **Juan Pablo:** Kusto optimization expert
- **Sanjeev:** Team lead, code review

---

## 🚀 **Ready to Start?**

1. Read `TWO_FUNCTION_ARCHITECTURE_EXPLAINED.md` for full details
2. Start with Function 1 (lightweight)
3. Test independently
4. Then create Function 2 (details)
5. Coordinate frontend integration

**Let's make VPP sites FAST!** ⚡
