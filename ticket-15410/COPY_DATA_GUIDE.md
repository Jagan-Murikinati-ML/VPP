# Simple Guide: Using Copy Data Activity

## 🎯 **What You Discovered:**

Copy Data activity CAN connect to eventHouse and eventhouseVPP!

This is the SIMPLEST approach - let's use it!

---

## 🚀 **Step-by-Step Guide:**

### **Step 1: Create Pipeline**

1. Fabric Workspace → **"+ New"** → **"Data pipeline"**
2. Name: `sqTelemetry_Daily_Copy`
3. Click **"Create"**

---

### **Step 2: Add Copy Data Activity**

1. In Activities panel (left side), find **"Copy data"**
2. **Drag and drop** onto the canvas
3. A box appears: "Copy data1"
4. **Click on it** to configure

---

### **Step 3: Configure SOURCE**

**Go to "Source" tab:**

1. **Data store type:** Select **"Workspace"**

2. **Workspace data store type:** Select **"KQL Database"** or **"Eventhouse"**

3. **Eventhouse:** Select **"eventHouse"** (where silverCommDataSite is)

4. **Database:** Should auto-select or select the database

5. **Table:** Select **"silverCommDataSite"**

6. **Use query:** Select **"Query"** (not "Table")

7. **Query:** Paste this:
   ```kql
   silverCommDataSite
   | where sourceTimestamp >= startofday(ago(1d))
   | where sourceTimestamp < startofday(now())
   | project 
       siteId, assetId, oem, sourceTimestamp,
       battery_200_DailyWhExp, battery_200_DailyWhImp,
       battery_200_IncWhExp, battery_200_IncWhImp,
       battery_200_TotWhExp, battery_200_TotWhImp,
       battery_200_W, battery_713_SoC, battery_713_SoH,
       grid_200_DailyWhExp, grid_200_DailyWhImp,
       grid_200_IncWhExp, grid_200_IncWhImp,
       grid_200_TotWhExp, grid_200_TotWhImp, grid_200_W,
       load_200_IncWhExp, load_200_IncWhImp,
       load_200_TotWhExp, load_200_TotWhImp, load_200_W,
       pv_200_DailyWhExp, pv_200_IncWhExp, pv_200_IncWhImp,
       pv_200_TotWhExp, pv_200_TotWhImp, pv_200_W
   ```

**Note:** We only select the 31 metric/base fields (NOT the _dl fields)

---

### **Step 4: Configure DESTINATION (Sink)**

**Go to "Destination" or "Sink" tab:**

1. **Data store type:** Select **"Workspace"**

2. **Workspace data store type:** Select **"KQL Database"** or **"Eventhouse"**

3. **Eventhouse:** Select **"eventhouseVPP"** (where sqTelemetry is)

4. **Database:** Should auto-select

5. **Table:** Select **"sqTelemetry"**

6. **Write behavior/method:** 
   - Look for "Append" option
   - Or "Insert" (NOT "Truncate" or "Overwrite")

---

### **Step 5: Configure MAPPING**

**Go to "Mapping" tab:**

**Option A: Import schemas**
1. Click **"Import schemas"**
2. It will auto-map the 31 columns
3. The 27 `_dl` columns in sqTelemetry will remain NULL (perfect!)

**Option B: Manual mapping**
- Only needed if auto-map doesn't work
- Map each source column to destination column (same names)

**IMPORTANT:** 
- Do NOT map the `_dl` fields
- They will automatically be NULL/empty in the destination

---

### **Step 6: Save Pipeline**

1. Click **"Save"** (top toolbar)
2. Pipeline saved!

---

### **Step 7: Test Run**

1. Click **"Run"** or **"Debug"**
2. Monitor the execution
3. Check Output tab for results

---

### **Step 8: Verify Data Copied**

**Open KQL Queryset connected to eventhouseVPP:**

```kql
// Check yesterday's data was copied
sqTelemetry
| where sourceTimestamp >= startofday(ago(1d))
| where sourceTimestamp < startofday(now())
| summarize 
    RowCount = count(),
    MinTime = min(sourceTimestamp),
    MaxTime = max(sourceTimestamp),
    Sites = dcount(siteId)
```

**Check _dl fields are NULL:**
```kql
sqTelemetry
| take 5
| project siteId, battery_200_DailyWhExp, battery_200_DailyWhExp_dl
```

**Expected:** `battery_200_DailyWhExp_dl` should be empty (NULL)

---

### **Step 9: Add Schedule Trigger**

**Same as before:**

1. Click **"Add trigger"** → **"Schedule"**
2. Name: `Nightly_2AM_Trigger`
3. Frequency: **Daily**
4. Time: **02:00:00**
5. Time zone: **Central Time**
6. Click **"OK"**
7. **Activate** the trigger

---

## ✅ **Why This Works:**

### **Key Insight:**

When Copy Data inserts rows into sqTelemetry:
- ✅ It inserts the 31 mapped columns
- ✅ The 27 `_dl` columns are NOT in the source
- ✅ Kusto automatically sets them to NULL/empty
- ✅ This is EXACTLY what we want!

**No need for complex transformations!** 🎉

---

## 📊 **What Gets Inserted:**

**From silverCommDataSite (31 columns):**
```
siteId, assetId, oem, sourceTimestamp,
battery_200_DailyWhExp, battery_200_DailyWhImp, ... (27 metrics)
```

**Into sqTelemetry (58 columns):**
```
siteId ✅ (copied)
assetId ✅ (copied)
oem ✅ (copied)
sourceTimestamp ✅ (copied)
battery_200_DailyWhExp ✅ (copied)
battery_200_DailyWhExp_dl ✅ (NULL automatically)
battery_200_DailyWhImp ✅ (copied)
battery_200_DailyWhImp_dl ✅ (NULL automatically)
...
```

**Perfect!** 🎯

---

## 🎯 **Summary:**

**Total Steps:**
1. ✅ Create pipeline
2. ✅ Add Copy Data activity
3. ✅ Configure Source (eventHouse.silverCommDataSite with yesterday filter)
4. ✅ Configure Destination (eventhouseVPP.sqTelemetry, append mode)
5. ✅ Map 31 columns (leave 27 _dl unmapped)
6. ✅ Test
7. ✅ Schedule (Daily, 2 AM)
8. ✅ Activate

**Time:** 1-2 hours

**Result:** Automated nightly data copy! 🚀

---

## ⚠️ **Potential Issues:**

### **Issue 1: Can't select "Query" option in Source**

**Solution:** Use "Table" instead, then add filter in "Additional settings" or "Filter" field

### **Issue 2: _dl fields showing errors in mapping**

**Solution:** Just ignore them - don't map them. They'll be NULL.

### **Issue 3: "Append" option not available**

**Solution:** Look for "Insert" or "Add" mode. Avoid "Truncate" or "Overwrite".

---

**This should work! Let me know when you try it!** 🎉
