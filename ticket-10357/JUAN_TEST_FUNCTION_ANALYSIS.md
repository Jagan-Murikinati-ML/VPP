# Juan's Test Function Analysis & Action Plan

**Function:** `getAllVppSitesByUserId_test_notreleased`  
**Created By:** Juan Pablo Culebro  
**Current Performance:** 5-7 seconds (PROD)  
**Target Performance:** < 2 seconds  
**Deadline:** May 15th Production Release

---

## 🎯 **STEP-BY-STEP ACTION PLAN**

### **Phase 1: Comparative Analysis (Monday)**

#### **Step 1.1: Compare Juan's Test vs V1**

**Goal:** Understand what Juan changed and why it's still slow

**Action Items:**
1. ✅ Extract clean KQL code from CSV
2. ✅ Side-by-side comparison with V1
3. ✅ Identify all optimizations Juan made
4. ✅ Identify what's still causing slowness

---

#### **Step 1.2: Deploy to DEV Environment**

**Goal:** Get accurate performance baseline in DEV

**Actions:**
```kusto
// Deploy Juan's function to DEV
.create-or-alter function getAllVppSitesByUserId_test_notreleased(
    inputUserId:string="", 
    page:int=0, 
    page_size:int=10
) {
    // [Paste Juan's function body]
}
```

**Test queries:**
```kusto
// Test 1: Basic execution
let start = now();
let result = getAllVppSitesByUserId_test_notreleased(
    inputUserId = '81ab4c51-a8d9-ef11-8eea-00224809f11c',
    page = 0,
    page_size = 50
);
let end = now();
result;
print duration_ms = datetime_diff('millisecond', end, start);
```

**Expected Outcome:**
- DEV performance: 2-3 seconds (better than PROD's 5-7s due to less data)
- Identify specific slow steps

---

### **Phase 2: Detailed Performance Analysis (Monday-Tuesday)**

#### **Step 2.1: Break Down Performance by Section**

**Test each major section individually:**

```kusto
// Section 1: User Mapping (Juan's new approach)
let start1 = now();
let site_ids_from_user = 
    goldAdtTwinEventsLatestV2
    | where TwinId in (
        goldResourceGroupToSiteMapping 
        | where resource_group_id in (
            goldUserGroupToResourceGroupMapping 
            | where user_group_id in (
                goldUserGroupToUserMapping 
                | where user_ids == inputUserId and isingroup > 0
                | project user_group_id
            ) and isingroup > 0 | project resource_group_ids
        ) and isingroup > 0
        | project site_ids
    ) and Action != 'Delete'
    | extend siteId = TwinId
    | summarize make_set(TwinId)
    | project list_site_ids = set_TwinId;
let end1 = now();
print section1_user_mapping_ms = datetime_diff('millisecond', end1, start1);

// Section 2: VPP Sites
let start2 = now();
let vppSites = goldAdtPropertyMinMaxLatestViewV2 
    | where Id in (site_ids_from_user)
    | where Key == 'isVppRegistered' and tolower(valueMax) == 'true'
    | join kind=inner (goldAdtTwinEventsLatestV2 | where Action != 'Delete') 
        on $left.Id == $right.TwinId;
let end2 = now();
print section2_vpp_sites_ms = datetime_diff('millisecond', end2, start2);

// Continue for all sections...
```

**Measure:**
1. User mapping time
2. VPP sites filter time
3. Pagination time
4. Property fetch time
5. Telemetry fetch time
6. Program data time
7. Device data time
8. Final assembly time

---

#### **Step 2.2: Compare with V1 Performance**

**Create comparison table:**

| Section | V1 Time | Juan's Test | Difference | Status |
|---------|---------|-------------|------------|--------|
| User mapping | ~1,000ms | ??? ms | ??? | ⏳ |
| VPP filter | ~400ms | ??? ms | ??? | ⏳ |
| Pagination | ~5ms | ??? ms | ??? | ⏳ |
| Site properties | ~800ms | ??? ms | ??? | ⏳ |
| Telemetry | ~500ms | ??? ms | ??? | ⏳ |
| Programs | ~400ms | ??? ms | ??? | ⏳ |
| Device data | ~300ms | ??? ms | ??? | ⏳ |
| **TOTAL** | **~3,405ms** | **???ms** | **???** | ⏳ |

---

### **Phase 3: Optimization (If DEV Performance Good)**

#### **Step 3.1: If DEV Performance is 2-3 seconds**

**Then proceed to add V2 features:**

**Missing features to add:**
1. ❌ Dynamic filtering (multiple fields, multiple operators)
2. ❌ Dynamic sorting (any field, asc/desc)
3. ❌ Global search (across all fields)

**Approach:**
```kusto
// Add parameters
.create-or-alter function getAllVppSitesByUserId_optimized(
    inputUserId: string = "",
    filters: dynamic = dynamic([]),      // NEW
    sortBy: string = "siteId",          // NEW
    sortOrder: string = "asc",          // NEW
    searchTerm: string = "",            // NEW
    page: int = 0,
    page_size: int = 10
) {
    // ... Juan's optimized base code ...
    
    // Add filtering logic
    let filteredData = baseData
        | where /* dynamic filter logic */;
    
    // Add search logic
    let searchedData = filteredData
        | where /* search across fields */;
    
    // Add dynamic sorting
    let sortedData = searchedData
        | order by /* dynamic sort */;
    
    // Then paginate
    // ...
}
```

---

#### **Step 3.2: If DEV Performance is Still Slow (>3 seconds)**

**Then we need further optimization:**

**Potential optimizations:**
1. Use `getCurrentUserSiteMapping()` helper (like V3 does)
2. Further consolidate `goldAdtPropertyMinMaxLatestViewV2` queries
3. Make telemetry/programs optional
4. Use materialized views if available

---

### **Phase 4: Testing & Validation (Wednesday-Thursday)**

#### **Step 4.1: Functional Testing**

**Test cases:**
```kusto
// Test 1: Basic pagination
getAllVppSitesByUserId_optimized(
    inputUserId = '81ab4c51-a8d9-ef11-8eea-00224809f11c',
    page = 0,
    page_size = 50
)

// Test 2: With filtering (if added)
getAllVppSitesByUserId_optimized(
    inputUserId = '81ab4c51-a8d9-ef11-8eea-00224809f11c',
    filters = dynamic([{"field": "state", "operator": "==", "value": "CA"}]),
    page = 0,
    page_size = 50
)

// Test 3: With sorting (if added)
getAllVppSitesByUserId_optimized(
    inputUserId = '81ab4c51-a8d9-ef11-8eea-00224809f11c',
    sortBy = "site_name",
    sortOrder = "desc",
    page = 0,
    page_size = 50
)

// Test 4: With search (if added)
getAllVppSitesByUserId_optimized(
    inputUserId = '81ab4c51-a8d9-ef11-8eea-00224809f11c',
    searchTerm = "Solar",
    page = 0,
    page_size = 50
)
```

**Validation:**
- ✅ Output matches V2 structure
- ✅ All 14 fields present
- ✅ Data accuracy (compare with V2)
- ✅ Pagination works correctly
- ✅ Filters work correctly (if added)
- ✅ Sorting works correctly (if added)
- ✅ Search works correctly (if added)

---

#### **Step 4.2: Performance Testing**

**Load testing:**
```kusto
// Test with different user sizes
// Small user (100 sites)
// Medium user (1,000 sites)
// Large user (5,000 sites)
// Extra large user (10,000+ sites)

// Measure performance for each
```

**Target:**
- Small users: < 1 second
- Medium users: < 2 seconds
- Large users: < 3 seconds (acceptable)

---

### **Phase 5: Deployment (Friday, May 9th)**

#### **Step 5.1: Code Review**

**Checklist:**
- ✅ Juan reviews final code
- ✅ Sanjeev reviews (if needed)
- ✅ Naveen approves business logic
- ✅ All tests passing
- ✅ Documentation updated

---

#### **Step 5.2: Deployment to QA**

**Actions:**
1. Deploy to QA environment
2. Run full test suite
3. Get QA sign-off

---

#### **Step 5.3: Production Deployment (May 15th)**

**Actions:**
1. Deploy during maintenance window
2. Monitor performance
3. Rollback plan ready

---

## 📊 **CURRENT STATUS**

- ✅ Juan created test function
- ✅ Function found in PROD
- ✅ Function exported to ticket folder
- ⏳ DEV deployment pending
- ⏳ Performance analysis pending
- ⏳ V2 features (filter/sort/search) pending

---

## 🎯 **IMMEDIATE NEXT STEPS (Monday)**

### **Priority 1: Extract and Analyze**
1. Create clean `.kql` file from CSV
2. Compare with V1 line-by-line
3. Document Juan's optimizations

### **Priority 2: Deploy to DEV**
1. Deploy function to DEV eventhouse
2. Test basic execution
3. Measure performance

### **Priority 3: Decision Point**
Based on DEV performance:
- **If 2-3s:** Add V2 features (filter/sort/search)
- **If >3s:** Apply additional optimizations first

---

**Ready to proceed systematically!** 🚀

