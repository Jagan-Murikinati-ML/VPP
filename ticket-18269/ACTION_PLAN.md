# Ticket 18269 - Your Action Plan

## 🎯 **What You Need to Do**

The Asset Onboarding report is a **Power BI report in Fabric**. You need to:

1. **Find the KQL query** that generates the data for the Power BI report
2. **Modify that query** to add 3 new columns:
   - `type1_oem_name`
   - `type1_oem_siteId`
   - `has_battery`
3. **Refresh the Power BI report** to show the new data

---

## 📍 **Step 1: Find the Data Source Query**

### **Option A: Check Power BI Report Data Source** (Most Likely)

1. Open the Power BI report in Fabric:
   - https://app.fabric.microsoft.com/groups/09c5e73c-a820-4100-aef5-d774ac0395f6/reports/b140bc27-f819-4b74-8ce6-d60b49cc583b/7c30b3e609720e59d7be?experience=fabric-developer

2. Click "Edit" or "Transform data"

3. Look for the **data source**:
   - It could be a **KQL query**
   - Or a **KQL function call** (e.g., `getAssetOnboardingReport()`)
   - Or a **table** in the Fabric warehouse

### **Option B: Search for Existing Functions**

Search for functions with names like:
- `getAssetOnboardingReport`
- `getSiteList`
- `getAllSites`
- `getSiteProperties`

**How to search:**
```kql
.show functions
| where Name contains "asset" or Name contains "onboard" or Name contains "site"
```

### **Option C: Check Fabric Workspace**

Navigate to the Fabric workspace and look for:
- **KQL Queryset** with "Asset Onboarding" in the name
- **Lakehouse tables** that might be the source
- **Dataflow** that generates the report data

---

## 📍 **Step 2: Understand the Current Query Structure**

Once you find the query, it likely looks something like this:

```kql
goldAdtPropertyMinMaxLatestViewV2
| where Key in ('siteId', 'oemInfo.0.oemName', 'oemInfo.0.oemSiteId', ...)
| where actionMax != 'Delete'
| where ModelId startswith 'dtmi:qcells:site'
| summarize 
    siteId = take_anyif(valueMax, Key == 'siteId'),
    oem_name = take_anyif(valueMax, Key == 'oemInfo.0.oemName'),
    oem_siteId = take_anyif(valueMax, Key == 'oemInfo.0.oemSiteId'),
    customer_name = take_anyif(valueMax, Key == 'firstName'),
    ...
by Id
```

---

## 📍 **Step 3: Modify the Query**

### **Change 1: Add Type 1 OEM Keys to the Filter**

Add `'oemInfo.1.oemName'` and `'oemInfo.1.oemSiteId'` to the `where Key in (...)` clause:

```kql
| where Key in ('siteId', 
               'oemInfo.0.oemName', 'oemInfo.0.oemSiteId',
               'oemInfo.1.oemName', 'oemInfo.1.oemSiteId',  // ← ADD THESE
               ...)
```

### **Change 2: Add Type 1 Columns to the Summarize**

Add two new lines in the `summarize` block:

```kql
| summarize 
    siteId = take_anyif(valueMax, Key == 'siteId'),
    oem_name = take_anyif(valueMax, Key == 'oemInfo.0.oemName'),
    oem_siteId = take_anyif(valueMax, Key == 'oemInfo.0.oemSiteId'),
    type1_oem_name = take_anyif(valueMax, Key == 'oemInfo.1.oemName'),    // ← ADD THIS
    type1_oem_siteId = take_anyif(valueMax, Key == 'oemInfo.1.oemSiteId'), // ← ADD THIS
    customer_name = take_anyif(valueMax, Key == 'firstName'),
    ...
by Id
```

### **Change 3: Add Battery Flag**

**Option A: Simple (Product Info-based)**

Add to the `where Key in (...)` clause:
```kql
'productInfo.prodSubType',
```

Add to the `summarize` block:
```kql
prodSubType = take_anyif(valueMax, Key == 'productInfo.prodSubType'),
```

Add after the summarize (as a new `extend`):
```kql
| extend has_battery = prodSubType in ('HybridInverter', 'BatteryInverter')
```

**Option B: Accurate (Relationship-based)** - More complex, ask Shuai first

---

## 📍 **Step 4: Test the Modified Query**

Before updating the report:

1. Run the modified query in **KQL Queryset**
2. Filter for site `100003907`:
   ```kql
   | where siteId == "100003907"
   ```
3. Verify output:
   - `type1_oem_name` should show `"Qcells"`
   - `type1_oem_siteId` should show `"SSMAK9HTBP"`

---

## 📍 **Step 5: Update the Power BI Report**

1. Replace the old query with the new query
2. Refresh the dataset
3. Verify the report shows the new columns
4. Test with site `100003907`

---

## ❓ **What to Ask Shuai**

Before making changes, confirm with Shuai:

### **Question 1:** Where is the data source query?
- "I found the Power BI report link in the ticket. Where is the KQL query that feeds this report?"
- "Is it a KQL function? A queryset? Or direct query?"

### **Question 2:** Battery flag logic?
- "Should I use `productInfo.prodSubType` to detect batteries?"
- "Or should I check for actual battery devices in relationships?"

### **Question 3:** Expected output format?
- "For site 100003907, should the output be:"
  ```
  oem_name: Qcells
  oem_siteId: 100003907
  type1_oem_name: Qcells
  type1_oem_siteId: SSMAK9HTBP
  has_battery: Yes
  ```

---

## 🎯 **Summary**

**Your job:**
1. ✅ Find the KQL query/function that generates the Power BI report data
2. ✅ Add 3 new columns to that query
3. ✅ Test with site 100003907
4. ✅ Update the Power BI report
5. ✅ Verify it works

**You do NOT need to:**
- ❌ Create a new report from scratch
- ❌ Manually edit CSV files
- ❌ Write complex new queries

**You ONLY need to:**
- ✅ Modify existing query to add 3 columns
- ✅ Refresh the report

---

## 📝 **Next Immediate Step**

**Ask Shuai in Slack/Email:**

```
Hi Shuai,

I'm working on ticket 18269 (Asset Onboarding report - add Type 1 OEM fields).

I found the Power BI report link in the ticket. Can you help me find:
1. The KQL query/function that generates the data for this report?
2. Is it a KQL function I need to modify, or a direct query in the report?

Also, for the battery flag:
- Should I use `productInfo.prodSubType` to detect batteries?
- Or check for battery devices in relationships?

Thanks!
```

---

**Once Shuai points you to the query, I'll help you modify it!** 🚀
