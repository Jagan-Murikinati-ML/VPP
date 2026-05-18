# Ticket 14469 - Quick Reference Guide

**Last Updated:** April 2026

---

## 🎯 **WHAT YOU'RE BUILDING:**

### **Task #1: Nightly Batch Job**
```
Source: silverCommDataSite (Kusto)
Process: Extract 10 key fields, basic cleaning
Destination: sqTelemetry (Kusto)
Schedule: Every night at 2 AM
```

### **Task #2: Bi-weekly Update**
```
Source: OEM APIs (or silverCommDataSite - TBD)
Process: Re-fetch last 14 days, update corrections
Destination: sqTelemetry (update existing)
Schedule: 1st and 15th of each month
```

### **Task #3: Backfill Investigation (SPIKE)**
```
Goal: Determine how to fill historical data gaps
Output: Document with recommendations
Timeline: This sprint (investigation only)
```

---

## 📊 **KEY TERMS - ONE SENTENCE EACH:**

| Term | Definition |
|------|------------|
| **Settlement** | Utility paying Q CELLS for battery services |
| **Utility** | Electric company (PG&E, SCE, SDG&E) that owns grid and makes payments |
| **SQMD** | Settlement Quality Meter Data - CPUC standard for "billing-grade" energy data |
| **Connector** | Automated pipeline that pulls data from OEM API every 15 minutes |
| **Backfill** | Filling in missing historical data gaps |
| **OEM** | Original Equipment Manufacturer (Tesla, Enphase, SolarEdge, etc.) |
| **Rate Limit** | Maximum API calls allowed per time period |

---

## ⚡ **RATE LIMITS - AT A GLANCE:**

```
✅ Tesla:     300 calls/min, 20 days/call → Can backfill 144,000 sites/day!
✅ Enphase:   No limit → Unlimited backfill capacity
✅ Qcells:    Internal API → Assumed OK
⚠️ SolarEdge: 12 calls/site/day → Can only backfill 6 sites/day (for 60 days)
❌ Solax:     100 calls/min total → Insufficient for bi-weekly updates
```

**Impact:** Solax excluded from bi-weekly updates. SolarEdge needs rotation strategy.

---

## 🔧 **FIELDS TO EXTRACT:**

### **From silverCommDataSite (50+ columns) to sqTelemetry (~10 columns):**

```
✅ KEEP:
- siteId
- meterId  
- sourceTimestamp → timestamp
- battery_200_IncWhImp → battery_discharge_kwh (÷ 1000)
- battery_200_IncWhExp → battery_charge_kwh (÷ 1000)
- battery_soc
- solar_production_kwh
- grid_import_kwh
- grid_export_kwh

❌ DROP:
- inverter_temperature
- grid_voltage
- grid_frequency
- (40+ other technical fields not needed for settlement)
```

---

## 📋 **QUESTIONS FOR YOUR CALL:**

### **Critical Decisions Needed:**

1. **Bi-weekly Update Source:**
   - [ ] Re-fetch from OEM APIs directly?
   - [ ] Read from silverCommDataSite (assume connectors updated it)?

2. **SolarEdge Strategy:**
   - [ ] Rotate through all sites (4.5 month cycle)?
   - [ ] Prioritize high-revenue sites only?

3. **Solax Handling:**
   - [ ] Exclude from bi-weekly updates?
   - [ ] Do quarterly manual backfill instead?
   - [ ] Wait for higher API limits?

4. **Implementation:**
   - [ ] Use KQL for both jobs?
   - [ ] Use Python for bi-weekly (more complex)?

---

## 🎯 **SUCCESS CRITERIA:**

### **Nightly Batch Job:**
- ✅ Runs automatically every night
- ✅ Processes previous day's data
- ✅ Extracts only settlement-relevant fields
- ✅ Loads into sqTelemetry within 30 minutes
- ✅ No data loss or corruption
- ✅ Monitoring/alerting in place

### **Bi-weekly Update:**
- ✅ Runs automatically on 1st and 15th
- ✅ Refreshes last 14 days for Tesla, Enphase, Qcells
- ✅ Rotates through SolarEdge sites (168 per run)
- ✅ Updates only changed values (not full replace)
- ✅ Completes within maintenance window
- ✅ Logging shows what was updated

### **Backfill SPIKE:**
- ✅ Document approach for one-time historical backfill
- ✅ Estimate effort and timeline
- ✅ Identify data sources
- ✅ Account for rate limit constraints
- ✅ Provide recommendation

---

## 📂 **FILES TO REVIEW:**

1. **design-document.md** - Naveen's proposal (read first!)
2. **oem-rate-limit-api-calls.md** - Rate limit details (critical!)
3. **COMPREHENSIVE_ANALYSIS.md** - Complete analysis (this is your study guide)
4. **QUICK_REFERENCE.md** - This file (quick lookup)

---

## 🚀 **NEXT STEPS:**

### **Today:**
- [x] Read COMPREHENSIVE_ANALYSIS.md ✅
- [x] Understand rate limits ✅
- [ ] Review design-document.md
- [ ] Prepare questions for call

### **After Call:**
- [ ] Document decisions
- [ ] Create nightly job implementation plan
- [ ] Create bi-weekly update implementation plan
- [ ] Start SPIKE investigation

### **This Sprint:**
- [ ] Complete SPIKE document
- [ ] Build nightly job (KQL/Python)
- [ ] Test nightly job in DEV
- [ ] Deploy nightly job to PROD

### **Next Sprint:**
- [ ] Build bi-weekly update logic
- [ ] Implement SolarEdge rotation
- [ ] Test bi-weekly in DEV
- [ ] Deploy to PROD

---

**You're ready! Good luck with your call!** 🎯🚀
