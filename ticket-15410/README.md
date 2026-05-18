# Ticket #15410: Nightly Data Copy Pipeline

## 📋 **Ticket Summary**

**Title:** Perform nightly data copy from silverCommDataSite to sqTelemetry table

**Type:** Task  
**Story Points:** 5  
**Assignee:** Jagan Murikinati  
**Status:** In Progress  

---

## 🎯 **Objective**

Build an automated Fabric Data Pipeline that copies **yesterday's data** from `silverCommDataSite` (eventHouse) to `sqTelemetry` (eventhouseVPP) every night at 2 AM.

---

## 📊 **Data Flow**

```
┌─────────────────────────────┐
│   silverCommDataSite        │
│   (eventHouse database)     │
│   - Raw telemetry data      │
│   - Billions of rows        │
│   - Updated every 15 min    │
└──────────┬──────────────────┘
           │
           │ Nightly at 2 AM
           │ (Copy yesterday's data only)
           │ ~10K-100K rows
           │
           ▼
┌─────────────────────────────┐
│      sqTelemetry            │
│   (eventhouseVPP database)  │
│   - Settlement quality data │
│   - Incremental growth      │
│   - 58 columns              │
└─────────────────────────────┘
```

---

## 🔧 **Implementation Approach**

### **Phase 1: Manual Testing** ✅
1. Create Fabric Data Pipeline
2. Add KQL Script activity
3. Test with manual trigger
4. Verify data copied correctly

### **Phase 2: Automation** ⏰
1. Add schedule trigger (Daily, 2 AM)
2. Activate trigger
3. Monitor first few runs

### **Phase 3: Validation** ✔️
1. Run for 2-3 days
2. Verify consistent daily copies
3. Check for errors/gaps

---

## 📁 **Files & Documentation**

| File | Purpose |
|------|---------|
| **FABRIC_PIPELINE_GUIDE.md** | Complete step-by-step tutorial for building the pipeline |
| **incremental_copy_script.kql** | KQL script to use in the pipeline activity |
| **QUICK_REFERENCE.md** | Quick cheat sheet for common tasks |
| **README.md** | This file - overview and summary |

---

## 🚀 **Getting Started**

### **New to Fabric Pipelines?**
👉 Start with **FABRIC_PIPELINE_GUIDE.md** - complete beginner's tutorial

### **Just Need the Script?**
👉 Use **incremental_copy_script.kql** - ready to paste into pipeline

### **Quick Reference?**
👉 Check **QUICK_REFERENCE.md** - commands and settings

---

## ⏱️ **Timeline**

| Phase | Duration | Status |
|-------|----------|--------|
| Pipeline Setup | 2-4 hours | 🔄 In Progress |
| Testing | 1-2 hours | ⏳ Pending |
| Scheduling | 30 min | ⏳ Pending |
| Validation | 2-3 days | ⏳ Pending |

**Total Estimated:** 5-8 hours (first time learning Fabric Pipelines)

---

## 📊 **Expected Results**

### **Daily Execution:**
- **Time:** 2:00 AM (Central Time)
- **Duration:** 10-60 seconds
- **Rows Copied:** ~10,000-100,000 (varies by day)
- **Data Latency:** ~2 hours (yesterday's data available at 2 AM)

### **Data Growth:**
```
Day 1:  12,129 rows (initial April 1 sample)
Day 2:  25,000 rows (+ yesterday's ~13K)
Day 3:  38,500 rows (+ yesterday's ~13.5K)
Day 4:  52,000 rows (+ yesterday's ~13.5K)
...
Month 1: ~400,000 rows
Year 1:  ~5,000,000 rows
```

---

## ✅ **Success Criteria**

- [x] Pipeline created in Fabric workspace
- [ ] Manual run successful with data verified
- [ ] Schedule trigger configured (2 AM daily)
- [ ] Trigger activated
- [ ] 3 consecutive successful scheduled runs
- [ ] No data gaps or duplicates
- [ ] Monitoring and alerts configured
- [ ] Documentation complete

---

## 🎓 **Learning Outcomes**

By completing this ticket, you will learn:

✅ How to create Fabric Data Pipelines  
✅ How to use KQL Script activities  
✅ How to configure schedule triggers  
✅ How to monitor pipeline runs  
✅ How to work with cross-database queries  
✅ How to implement incremental data synchronization  

---

## 📝 **Notes**

- This is an **incremental copy**, NOT a full table copy
- Only **yesterday's data** is copied each night
- Uses `.set-or-append` to avoid duplicates
- Data label fields default to empty (NULL) as per Naveen's guidance
- This handles **forward-fill** only (new data going forward)
- **Bi-weekly update job** (separate ticket) will handle data corrections

---

## 🔗 **Related Tickets**

- **#15188** - Created sqTelemetry table structure
- **#14469** - SPIKE: Telemetry backfill investigation
- **Future** - Bi-weekly update job for data corrections

---

## 📞 **Questions or Issues?**

Contact:
- **Naveen Siddalingaswamy** (Tech Lead)
- **Rohit** (Scrum Master)
- **Ali Rizvi** (DevOps - for production deployment)

---

**Happy Pipeline Building!** 🚀
