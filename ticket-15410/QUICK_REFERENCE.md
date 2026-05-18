# Quick Reference - Fabric Data Pipeline

## 🚀 **Quick Start (5 Steps)**

1. **Create Pipeline:** Fabric Workspace → New → Data pipeline → Name it
2. **Add Activity:** Drag "KQL script" from Activities panel
3. **Configure:** Select eventhouseVPP database → Paste script
4. **Test:** Click "Run" → Verify data copied
5. **Schedule:** Add trigger → Schedule (Daily, 2 AM) → Activate

---

## 📋 **Pipeline Configuration**

### **Activity Settings:**

| Setting | Value |
|---------|-------|
| **Name** | Copy_Yesterday_Data |
| **Workspace** | Your workspace |
| **KQL Database** | eventhouseVPP |
| **Use query** | Text |
| **Script** | See `incremental_copy_script.kql` |

### **Schedule Trigger:**

| Setting | Value |
|---------|-------|
| **Name** | Nightly_2AM_Trigger |
| **Frequency** | Day |
| **Repeat every** | 1 day |
| **Start time** | 02:00:00 |
| **Time zone** | Central Time (US & Canada) |

---

## ✅ **Verification Queries**

### **Check Yesterday's Data:**
```kql
sqTelemetry
| where sourceTimestamp >= startofday(ago(1d))
| where sourceTimestamp < startofday(now())
| count
```

### **Check Daily Growth:**
```kql
sqTelemetry
| summarize count() by Day = startofday(sourceTimestamp)
| order by Day desc
```

### **Check Total Size:**
```kql
sqTelemetry
| summarize TotalRows = count(), 
    MinDate = min(sourceTimestamp), 
    MaxDate = max(sourceTimestamp)
```

---

## 🔧 **Common Tasks**

### **Manually Trigger Pipeline:**
1. Open pipeline
2. Click "Run"
3. Click "OK"

### **View Run History:**
1. Open pipeline
2. Click "Monitoring" or "Run history" tab

### **Edit Schedule:**
1. Pipeline → Triggers section
2. Edit trigger
3. Save changes

### **Disable Pipeline:**
1. Pipeline → Triggers
2. Toggle trigger to "Disabled"

---

## 🚨 **Troubleshooting**

| Issue | Solution |
|-------|----------|
| Can't find KQL activity | Use search box, type "KQL" or look under "Script" section |
| Pipeline fails | Check Output tab for error details |
| No data copied | Verify data exists in source for yesterday |
| Permission error | Check write access to sqTelemetry |
| Trigger not firing | Verify trigger is "Active/Enabled" |
| Duplicate data | Check run history for multiple executions |

---

## 📊 **Expected Performance**

| Metric | Value |
|--------|-------|
| **Data per day** | ~10K-100K rows |
| **Execution time** | 10-60 seconds |
| **Schedule** | Daily at 2 AM |
| **Data latency** | ~2 hours (2 AM run copies previous day) |

---

## 📝 **Files in This Ticket**

1. **FABRIC_PIPELINE_GUIDE.md** - Complete step-by-step tutorial
2. **incremental_copy_script.kql** - The KQL script to use in pipeline
3. **QUICK_REFERENCE.md** - This cheat sheet
4. **ticket.md** - Ticket description

---

## ✅ **Completion Checklist**

- [ ] Pipeline created and saved
- [ ] Manual test successful
- [ ] Data verified in sqTelemetry
- [ ] Schedule configured (2 AM daily)
- [ ] Trigger activated
- [ ] 2-3 successful scheduled runs
- [ ] Monitoring set up
- [ ] Team notified

---

**Total Time:** 2-4 hours (first time learning)  
**Future Changes:** < 30 minutes

**Good luck!** 🚀
