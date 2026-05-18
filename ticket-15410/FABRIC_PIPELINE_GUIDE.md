# Fabric Data Pipeline - Complete Beginner's Guide
## Ticket #15410: Nightly Data Copy (silverCommDataSite → sqTelemetry)

**Author:** Jagan Murikinati  
**Date:** 2026-04-25  
**Ticket:** #15410  
**Purpose:** Build your first Fabric Data Pipeline for automated nightly data copy  

---

## 🎯 **What We're Building:**

**Goal:** Automated pipeline that copies yesterday's data from silverCommDataSite to sqTelemetry every night.

**Approach:**
1. ✅ Start simple - Manual trigger with basic script
2. ✅ Test and validate
3. ✅ Add scheduling (nightly at 2 AM)
4. ✅ Add monitoring and error handling

---

## 📋 **Prerequisites:**

Before starting, make sure you have:
- ✅ Access to Fabric workspace
- ✅ Access to eventhouse (silverCommDataSite)
- ✅ Access to eventhouseVPP (sqTelemetry)
- ✅ Permissions to create Data Pipelines
- ✅ Working KQL script (we have this!)

---

## 🚀 **Phase 1: Create Your First Pipeline (Manual Trigger)**

### **Step 1: Open Fabric Workspace**

1. Go to your Fabric workspace in browser
2. You should see: eventhouse, eventhouseVPP, KQL Querysets, etc.

**Screenshot location:** Top-left, you'll see workspace name

---

### **Step 2: Create New Data Pipeline**

1. Click **"+ New"** button (top-left or center)
2. Scroll down and find **"Data pipeline"**
3. Click on it

**Alternative path:** 
- Click "Create" → "Data pipeline"

**Popup will appear:**
- Name: `sqTelemetry_Daily_Copy`
- Description: `Nightly incremental copy from silverCommDataSite to sqTelemetry`

4. Click **"Create"**

**Result:** You'll see a blank pipeline canvas (drag-and-drop interface)

---

### **Step 3: Alternative - Use Notebook or Direct Fabric Approach**

**IMPORTANT UPDATE:** If you don't see KQL Database connection options, Fabric might require a different approach.

---

## 🎯 **RECOMMENDED: Skip Pipeline for Now - Use Fabric Jobs Instead**

**Better approach for Fabric + KQL:**

Instead of Data Pipeline, use **Fabric KQL Queryset with Scheduled Refresh** or **Power Automate**.

**However, if you want to continue with Pipeline:**

Use **"Invoke Pipeline"** or **"Web Activity"** to call Fabric REST API to execute KQL.

---

## 🔄 **SIMPLER ALTERNATIVE: Manual Scheduling**

For your first implementation, let's do this:

### **Step 3A: Create a KQL Queryset**

1. Go to Fabric workspace
2. Click **"+ New"** → **"KQL Queryset"**
3. Name it: `Daily_Copy_Job`
4. Connect to **eventhouseVPP** database
5. Paste your script from `incremental_copy_script.kql`
6. **Save it**

---

### **Step 3B: Schedule It (Using Power Automate)**

Since Fabric Data Pipelines don't support KQL connections easily, use Power Automate:

1. Go to **Power Automate** (powerautomate.microsoft.com)
2. Create new **"Scheduled cloud flow"**
3. Name: `Nightly_sqTelemetry_Copy`
4. Trigger: Daily at 2 AM
5. Action: Use **"HTTP"** connector to call Fabric API
6. Execute your KQL script

---

## ⚡ **EVEN SIMPLER: Use Fabric Scheduled Job (If Available)**

**Check if your Fabric has this feature:**

1. Go to eventhouseVPP
2. Look for **"Jobs"** or **"Scheduled Queries"** section
3. Create new scheduled job
4. Paste your KQL script
5. Set schedule: Daily, 2 AM

---

**Let me create a new guide for the simpler approach...**

---

### **Step 4: Configure KQL Script Activity**

**Click on the "KQL script1" box** to configure it:

#### **A. General Tab:**

1. **Name:** Change to `Copy_Yesterday_Data`
2. **Description:** `Copies previous day data from silverCommDataSite to sqTelemetry`
3. **Timeout:** Leave default (12 hours - more than enough)

#### **B. Settings Tab:**

This is where the magic happens!

#### **1. Create/Select Connection:**

**If you DON'T have a connection yet:**

1. Next to **"Connection"** dropdown, click **"+ New"**
2. **New connection dialog appears:**
   - **Connection name:** `eventhouseVPP_Connection`
   - **Connection type:** "KQL Database" or "Azure Data Explorer"
   - **Account selection:** Select your workspace/account
   - **Database:** Select **eventhouseVPP** (where sqTelemetry is)
3. Click **"Create"** or **"OK"**

**If connection already exists:**
- Select it from **"Connection"** dropdown

#### **2. Add the Script:**

After connection is set:

1. Find the **"Script"** or **"Query"** text box (large text area)
2. **Paste this KQL query:**

```kql
.set-or-append sqTelemetry <|
database("eventHouse").silverCommDataSite
| where sourceTimestamp >= startofday(ago(1d))
| where sourceTimestamp < startofday(now())
| project 
    siteId = siteId,
    assetId = assetId,
    oem = oem,
    sourceTimestamp = sourceTimestamp,
    battery_200_DailyWhExp = battery_200_DailyWhExp,
    battery_200_DailyWhExp_dl = "",
    battery_200_DailyWhImp = battery_200_DailyWhImp,
    battery_200_DailyWhImp_dl = "",
    battery_200_IncWhExp = battery_200_IncWhExp,
    battery_200_IncWhExp_dl = "",
    battery_200_IncWhImp = battery_200_IncWhImp,
    battery_200_IncWhImp_dl = "",
    battery_200_TotWhExp = battery_200_TotWhExp,
    battery_200_TotWhExp_dl = "",
    battery_200_TotWhImp = battery_200_TotWhImp,
    battery_200_TotWhImp_dl = "",
    battery_200_W = battery_200_W,
    battery_200_W_dl = "",
    battery_713_SoC = battery_713_SoC,
    battery_713_SoC_dl = "",
    battery_713_SoH = battery_713_SoH,
    battery_713_SoH_dl = "",
    grid_200_DailyWhExp = grid_200_DailyWhExp,
    grid_200_DailyWhExp_dl = "",
    grid_200_DailyWhImp = grid_200_DailyWhImp,
    grid_200_DailyWhImp_dl = "",
    grid_200_IncWhExp = grid_200_IncWhExp,
    grid_200_IncWhExp_dl = "",
    grid_200_IncWhImp = grid_200_IncWhImp,
    grid_200_IncWhImp_dl = "",
    grid_200_TotWhExp = grid_200_TotWhExp,
    grid_200_TotWhExp_dl = "",
    grid_200_TotWhImp = grid_200_TotWhImp,
    grid_200_TotWhImp_dl = "",
    grid_200_W = grid_200_W,
    grid_200_W_dl = "",
    load_200_IncWhExp = load_200_IncWhExp,
    load_200_IncWhExp_dl = "",
    load_200_IncWhImp = load_200_IncWhImp,
    load_200_IncWhImp_dl = "",
    load_200_TotWhExp = load_200_TotWhExp,
    load_200_TotWhExp_dl = "",
    load_200_TotWhImp = load_200_TotWhImp,
    load_200_TotWhImp_dl = "",
    load_200_W = load_200_W,
    load_200_W_dl = "",
    pv_200_DailyWhExp = pv_200_DailyWhExp,
    pv_200_DailyWhExp_dl = "",
    pv_200_IncWhExp = pv_200_IncWhExp,
    pv_200_IncWhExp_dl = "",
    pv_200_IncWhImp = pv_200_IncWhImp,
    pv_200_IncWhImp_dl = "",
    pv_200_TotWhExp = pv_200_TotWhExp,
    pv_200_TotWhExp_dl = "",
    pv_200_TotWhImp = pv_200_TotWhImp,
    pv_200_TotWhImp_dl = "",
    pv_200_W = pv_200_W,
    pv_200_W_dl = ""
```

5. Click **"OK"** or **"Apply"**

---

### **Step 5: Save the Pipeline**

1. Click **"Save"** button (top-right or toolbar)
2. Pipeline is now saved!

**You should see:** "Pipeline saved successfully" notification

---

## 🧪 **Phase 2: Test Your Pipeline (Manual Run)**

### **Step 6: Manually Trigger the Pipeline**

**Purpose:** Test if everything works before scheduling

1. In your pipeline, click **"Run"** button (top toolbar)
2. A dialog will appear: **"Pipeline run"**
3. Click **"OK"** or **"Run"**

**What happens:**
- Pipeline starts executing
- You'll see a progress indicator

---

### **Step 7: Monitor the Pipeline Run**

**Watch the execution:**

1. You'll see the activity turn **yellow** (running)
2. After completion, it turns **green** (success) or **red** (failed)

**To see details:**
1. Click on the **"Output"** tab at the bottom
2. You'll see execution logs

**OR**

1. Click the **activity box** on canvas
2. Look at **"Output"** panel on the right

---

### **Step 8: Verify Data Was Copied**

**Open a KQL Queryset and run:**

```kql
// Check if yesterday's data was copied
sqTelemetry
| where sourceTimestamp >= startofday(ago(1d))
| where sourceTimestamp < startofday(now())
| summarize RowCount = count(),
    MinTime = min(sourceTimestamp),
    MaxTime = max(sourceTimestamp),
    Sites = dcount(siteId)
```

**Expected result:**
- RowCount > 0 (should have rows!)
- MinTime and MaxTime should be yesterday's date range
- Sites = number of unique sites

**If you get 0 rows:**
- Check if there's actually data in silverCommDataSite for yesterday
- Check the query logs for errors

---

## ⏰ **Phase 3: Add Scheduling (Nightly Automation)**

### **Step 9: Create a Schedule Trigger**

**Now that manual run works, let's automate it!**

1. In your pipeline, look for **"Add trigger"** button (top toolbar)
2. Click it → Select **"Schedule"**

**Schedule trigger dialog appears:**

---

### **Step 10: Configure Schedule**

**Basic Settings:**

1. **Name:** `Nightly_2AM_Trigger`
2. **Description:** `Runs every night at 2 AM to copy previous day data`

**Recurrence:**

1. **Frequency:** Select **"Day"**
2. **Repeat every:** `1` day
3. **Start date and time:**
   - Date: Today or tomorrow
   - Time: `02:00:00` (2 AM)
4. **Time zone:** Select **"(UTC-05:00) Central Time (US & Canada)"** or your preferred timezone

**Advanced (Optional):**
- Leave end date blank (runs forever)
- Leave other options as default

5. Click **"OK"** or **"Save"**

---

### **Step 11: Activate the Trigger**

**Important:** The trigger is created but NOT active yet!

1. Go to pipeline **"Home"** tab or **"Triggers"** section
2. Find your trigger: `Nightly_2AM_Trigger`
3. Toggle it to **"Enabled"** or **"Active"**

**You should see:** Green checkmark or "Active" status

**Congratulations!** 🎉 Pipeline will now run every night at 2 AM automatically!

---

## 📊 **Phase 4: Monitoring and Maintenance**

### **Step 12: View Pipeline Run History**

**To see past runs:**

1. Go to your pipeline
2. Click **"Monitoring"** or **"Run history"** tab
3. You'll see a list of all runs with:
   - Start time
   - Duration
   - Status (Success/Failed)
   - Rows processed

---

### **Step 13: Set Up Alerts (Optional but Recommended)**

**Get notified if pipeline fails:**

1. In pipeline settings, look for **"Alerts"** or **"Notifications"**
2. Add your email
3. Select: **"Notify on failure"**

**Now you'll get an email if the nightly job fails!**

---

## 🔧 **Phase 5: Testing and Validation**

### **Step 14: Test the Schedule (Don't Wait for 2 AM!)**

**Temporarily change schedule to test:**

1. Edit your trigger
2. Change time to 5 minutes from now
3. Save and activate
4. Wait 5 minutes
5. Check if it ran successfully
6. **Change back to 2 AM** after testing!

---

### **Step 15: Validate Data Quality**

**After a few days of runs, check:**

```kql
// Check daily data growth
sqTelemetry
| summarize RowCount = count() by Day = startofday(sourceTimestamp)
| order by Day desc
| take 7  // Last 7 days
```

**Expected:**
- Each day should have similar row counts
- No gaps in dates
- Increasing total over time

---

## 📝 **Common Issues and Solutions**

### **Issue 1: Pipeline Run Fails**

**Error:** "Database not found"
- **Solution:** Check KQL Database setting - make sure it's `eventhouseVPP`

**Error:** "Permission denied"
- **Solution:** Check if you have write access to sqTelemetry table

**Error:** "Query timeout"
- **Solution:** Increase timeout in activity settings

---

### **Issue 2: No Data Copied (0 rows)**

**Check 1:** Is there data in silverCommDataSite for yesterday?
```kql
database("eventHouse").silverCommDataSite
| where sourceTimestamp >= startofday(ago(1d))
| where sourceTimestamp < startofday(now())
| count
```

**Check 2:** Is the cross-database query working?
- Test in KQL Queryset first

---

### **Issue 3: Duplicate Data**

**Symptom:** Same data copied multiple times

**Solution:** Check trigger - might be firing multiple times
- Disable and re-create trigger
- Check run history for duplicate runs

---

## 🎓 **Key Concepts You Learned**

✅ **Data Pipeline:** Automated workflow for data movement
✅ **Activities:** Building blocks of pipelines (KQL Script, Copy Data, etc.)
✅ **Triggers:** Schedule-based or event-based execution
✅ **Monitoring:** Track runs and debug failures
✅ **Incremental Copy:** Only copy new data (yesterday), not full table

---

## 📚 **Next Steps After Pipeline Works**

1. ✅ Document the pipeline (runbook)
2. ✅ Share with team for review
3. ✅ Add to production monitoring dashboard
4. ✅ Create alerting for failures
5. ✅ Plan for bi-weekly update job (separate pipeline)

---

## ✅ **Checklist Before Closing Ticket**

- [ ] Pipeline created in Fabric
- [ ] Manual run tested successfully
- [ ] Data verified in sqTelemetry
- [ ] Schedule trigger configured (2 AM nightly)
- [ ] Trigger activated and working
- [ ] At least 2-3 successful scheduled runs completed
- [ ] Monitoring and alerts set up
- [ ] Documentation updated
- [ ] DevOps team notified (if needed)
- [ ] Ticket updated with completion notes

---

## 🎯 **Summary**

**What You Built:**
- Automated nightly data pipeline
- Copies yesterday's data from silverCommDataSite → sqTelemetry
- Runs every night at 2 AM
- Monitored and alerting enabled

**Time Investment:**
- Setup: 2-4 hours (first time)
- Testing: 1-2 hours
- Monitoring: Ongoing (5 min/day)

**Result:**
- Automated, reliable, hands-off data synchronization! 🎉

---

**Good luck with your first Fabric Data Pipeline!** 🚀
