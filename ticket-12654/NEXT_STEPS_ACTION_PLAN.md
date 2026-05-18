# Action Plan: Fix getVPPSiteLevelPerformance in PROD

**Date:** May 14, 2026  
**Issue:** Function works in DEV but not in PROD

---

## 🎯 Root Cause Identified

**`getVPPSiteLevelPerformance` depends on `getSiteDispatchCommandSummary` helper function which returns NO DATA in PROD.**

---

## 📋 Step-by-Step Investigation

### **Step 1: Test Helper Function Directly in PROD**

Run this in **PROD eventhouseVPP:**

```kusto
getSiteDispatchCommandSummary(inputEventIds = pack_array('ca0c0d89-614d-4358-b31f-2cb27a29cf5f'))
```

**Expected Result:**
- **If returns 0 rows:** Helper function is broken ❌
- **If returns data:** Issue is in the join/filter logic ⚠️

---

### **Step 2: Get Helper Function Code**

Run this in **PROD eventhouseVPP:**

```kusto
.show function getSiteDispatchCommandSummary
```

**Then compare with DEV:**

Run this in **DEV eventhouseVPP:**

```kusto
.show function getSiteDispatchCommandSummary
```

**Look for differences in:**
- Table names
- Database references
- Filtering logic
- Time window calculations

---

### **Step 3: Check if Helper Function Exists**

Run this in **PROD:**

```kusto
.show functions
| where Name == 'getSiteDispatchCommandSummary'
```

**Possible outcomes:**
- Function doesn't exist in PROD ❌
- Function exists but different version ⚠️
- Function exists and same version ✅ (then check data)

---

### **Step 4: Check Underlying Data Tables**

The helper function likely queries these tables:

```kusto
// Check silver_dispatch_result_dto
silver_dispatch_result_dto
| where event_id == 'ca0c0d89-614d-4358-b31f-2cb27a29cf5f'
| take 10

// Check silverCommDataSite
database('EventHouse').silverCommDataSite
| where siteId in ('400032980', '400033526')
| where sourceTimestamp between (datetime(2026-05-12T07:15:00.000Z) .. datetime(2026-05-12T08:15:00.000Z))
| take 10
```

---

## 🔧 Quick Fix Options

### **Option 1: Deploy Helper Function from DEV to PROD**

If helper function is missing or different in PROD:

1. Get function code from DEV
2. Deploy to PROD using `.create-or-alter function`
3. Test `getVPPSiteLevelPerformance` again

---

### **Option 2: Rewrite getVPPSiteLevelPerformance (Recommended)**

Make it work like `getVPPDispatchSummary` - query silverCommDataSite directly:

**Advantages:**
- No dependency on helper function
- More resilient
- Direct data access
- Same pattern as working function

**Disadvantage:**
- Requires rewriting ~40 lines of code

---

### **Option 3: Add Fallback Logic**

Modify `getVPPSiteLevelPerformance` to fallback to silverCommDataSite if helper function returns no data.

---

## 📝 Queries to Share with Team

### **For Shaun/Naveen:**

```
Hi team,

I've identified the root cause:

getVPPSiteLevelPerformance depends on a helper function called getSiteDispatchCommandSummary 
which returns NO DATA in PROD but works fine in DEV.

Can you please:
1. Check if getSiteDispatchCommandSummary exists in PROD eventhouseVPP?
2. Compare its code between DEV and PROD?
3. Check if it's deployed to PROD?

Test query:
getSiteDispatchCommandSummary(inputEventIds = pack_array('ca0c0d89-614d-4358-b31f-2cb27a29cf5f'))

This should return site-level command summary data but returns 0 rows in PROD.

Thanks,
Jagan
```

---

## 🎯 Expected Timeline

| Step | Action | Time | Owner |
|------|--------|------|-------|
| 1 | Test helper function in PROD | 5 min | Jagan |
| 2 | Get function code from DEV/PROD | 10 min | Jagan |
| 3 | Compare functions | 15 min | Jagan |
| 4 | Identify fix approach | 15 min | Team discussion |
| 5 | Deploy fix to PROD | 30 min | DevOps/Juan |
| 6 | Test in PROD | 10 min | Jagan |
| 7 | Verify UI works | 10 min | Kushal/QA |

**Total:** ~2 hours

---

## ✅ Success Criteria

After fix is deployed, this should work in PROD:

```kusto
getVPPSiteLevelPerformance(input_event_name='ca0c0d89-614d-4358-b31f-2cb27a29cf5f')
```

**Should return:**
- Site-level performance data for each site in the event
- Energy discharged/charged per site
- Customer names, OEM info
- Dispatch windows per site

---

## 🚀 Ready for Next Steps!

You now have:
1. ✅ Complete analysis of both functions
2. ✅ Root cause identified (helper function dependency)
3. ✅ Action plan to fix the issue
4. ✅ Queries to test the fix

**Next action:** Test `getSiteDispatchCommandSummary` in PROD and report findings!
