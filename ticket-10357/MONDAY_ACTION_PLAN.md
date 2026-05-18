# Monday Action Plan - Ticket 10357

**Status:** Juan created test function, currently 5-7s in PROD  
**Goal:** Get to <2s by May 15th  
**Your Role:** Senior Data Engineer - systematic optimization

---

## 📋 **MORNING SESSION (2-3 hours)**

### **Task 1: Deploy Juan's Function to DEV (30 min)**

```kusto
// Copy from: ticket-10357/getAllVppSitesByUserId_test_notreleased.kql
// Deploy to: DEV eventhouse

.create-or-alter function getAllVppSitesByUserId_test_notreleased(
    inputUserId:string="", 
    page:int=0, 
    page_size:int=10
) {
    // ... paste Juan's code ...
}
```

**Verify deployment:**
```kusto
.show function getAllVppSitesByUserId_test_notreleased
```

---

### **Task 2: Baseline Performance Test (30 min)**

```kusto
// Test 1: Measure total execution time
let start = now();
let result = getAllVppSitesByUserId_test_notreleased(
    inputUserId = '81ab4c51-a8d9-ef11-8eea-00224809f11c',
    page = 0,
    page_size = 50
);
let end = now();
result;
print total_duration_ms = datetime_diff('millisecond', end, start);
```

**Expected in DEV:** 2-3 seconds (much better than PROD's 5-7s)

---

### **Task 3: Section-by-Section Performance Analysis (1 hour)**

**Measure each major section:**

```kusto
// Section 1: User Mapping
let start1 = now();
let site_ids = /* user mapping logic */;
let end1 = now();
print user_mapping_ms = datetime_diff('millisecond', end1, start1);

// Section 2: VPP Sites Filter  
let start2 = now();
let vpp = /* vpp filter logic */;
let end2 = now();
print vpp_filter_ms = datetime_diff('millisecond', end2, start2);

// Continue for all sections...
```

**Document results in comparison table**

---

### **Task 4: Compare with V1 (30 min)**

**Create performance comparison:**

| Section | V1 | Juan's Test | Improvement | Analysis |
|---------|----|-----------| ------------|----------|
| User mapping | ~1000ms | ???ms | ??? | ⏳ |
| VPP filter | ~400ms | ???ms | ??? | ⏳ |
| Site properties | ~800ms | ???ms | ??? | ⏳ |
| Telemetry | ~500ms | ???ms | ??? | ⏳ |
| Programs | ~400ms | ???ms | ??? | ⏳ |
| Device data | ~300ms | ???ms | ??? | ⏳ |
| **TOTAL** | **~3400ms** | **???ms** | **???** | ⏳ |

---

## 📋 **AFTERNOON SESSION (2-3 hours)**

### **Decision Point: Based on DEV Performance**

#### **Scenario A: DEV is 2-3 seconds** ✅

**Action:** Proceed with adding V2 features (filter/sort/search)

**Tasks:**
1. Add dynamic filtering parameters
2. Add dynamic sorting parameters
3. Add global search parameter
4. Test each feature
5. Ensure performance stays <3s

---

#### **Scenario B: DEV is >3 seconds** ❌

**Action:** Apply additional optimizations first

**Priority Optimizations:**

**1. Replace User Mapping with Helper Function**
```kusto
// Current (Juan's nested in operators)
let site_ids_from_user = 
    goldAdtTwinEventsLatestV2
    | where TwinId in (
        goldResourceGroupToSiteMapping 
        | where resource_group_id in (...)
    ) ...

// Optimized (use helper like V3 does)
let site_ids_from_user = toscalar(
    getCurrentUserSiteMapping(inputUserId) 
    | project list_site_ids
);
```
**Expected savings:** -600 to -800ms

**2. Make Telemetry Optional**
```kusto
.create-or-alter function getAllVppSitesByUserId_optimized(
    inputUserId: string,
    includeTelemetry: bool = true,
    includePrograms: bool = true,
    page: int = 0,
    page_size: int = 10
) {
    let commData = iff(includeTelemetry,
        silverCommDataSite | where ...,
        datatable(siteId:string, SOC:real, ...)[]);  // Empty if not needed
    
    let program_data = iff(includePrograms,
        GetLatestProgramSiteInfo | where ...,
        datatable(site_id:string, program_name:dynamic)[]);  // Empty if not needed
    
    // ... rest of function ...
}
```
**Expected savings:** Up to -900ms when optional data not needed

**3. Test Performance After Each Optimization**

---

## 📋 **END OF DAY**

### **Deliverables:**

1. ✅ **Performance Analysis Document**
   - Juan's Test vs V1 comparison
   - Section-by-section breakdown
   - Bottleneck identification

2. ✅ **Updated Function (if optimized)**
   - With additional optimizations applied
   - Performance test results

3. ✅ **Status Update to Juan**
   ```
   Hi Juan,
   
   Tested your function in DEV:
   - Performance: [X]ms
   - Analysis: [bottlenecks found]
   - Recommendations: [optimizations to apply]
   
   [If good] Ready to add V2 features (filter/sort/search)
   [If slow] Suggest additional optimizations first
   
   Can we sync tomorrow to discuss next steps?
   
   Thanks,
   Jagan
   ```

4. ✅ **Ticket Update**
   ```
   Update:
   
   Analyzed Juan's test function (getAllVppSitesByUserId_test_notreleased):
   - PROD performance: 5-7s
   - DEV performance: [X]s
   - Key optimizations Juan made:
     • Eliminated GetSiteProperties() helper (-500ms)
     • Consolidated device data queries (-150ms)
     • Optimized property fetching
   
   Current bottlenecks:
   - [List specific bottlenecks]
   
   Next steps:
   - [Based on decision point A or B]
   
   Target: <2s by May 15th
   Status: On track / Needs additional optimization
   ```

---

## 🎯 **KEY SUCCESS METRICS**

### **By End of Monday:**
- ✅ Juan's function deployed to DEV
- ✅ Baseline performance measured
- ✅ Bottlenecks identified
- ✅ Clear path forward defined

### **By End of Week (May 9th):**
- ✅ Optimized function <2s in DEV
- ✅ V2 features added (if performance allows)
- ✅ All tests passing
- ✅ Ready for QA deployment

### **By May 15th:**
- ✅ Production deployment
- ✅ Performance target met

---

## 📁 **REFERENCE DOCUMENTS**

1. **JUAN_TEST_FUNCTION_ANALYSIS.md** - Overall strategy
2. **V1_VS_JUAN_COMPARISON.md** - Detailed comparison
3. **getAllVppSitesByUserId_test_notreleased.kql** - Clean code to deploy
4. **UNDERSTANDING.md** - Background context

---

## 💡 **TIPS FOR SUCCESS**

### **As a Senior Engineer:**
1. **Measure everything** - Don't guess, measure actual performance
2. **One optimization at a time** - Test impact of each change
3. **Document decisions** - Keep ticket updated
4. **Communicate proactively** - Update Juan/Naveen regularly
5. **Think systematically** - Follow the plan, don't jump around

### **Time Management:**
- Morning: Analysis and measurement
- Afternoon: Optimization and testing
- End of day: Documentation and communication

### **Communication:**
- Update ticket with findings
- Message Juan with results
- Flag blockers immediately
- Ask for help if stuck >30 minutes

---

**You're ready to execute systematically!** 🚀

**Start with deployment and measurement - data will guide next steps!**

