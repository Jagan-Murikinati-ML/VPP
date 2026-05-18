# Quick Start - Ticket 15188

## 🎯 What You're Doing

Creating `sqTelemetry` table with **56 fields** in **eventhouseVPP** database.

---

## 📍 Location

**Source:** `silverCommDataSite` (in **eventhouse** database)  
**Target:** `sqTelemetry` (in **eventhouseVPP** database)

---

## ⚡ Quick Steps

### 1. Open Fabric → eventhouseVPP → New KQL Queryset

### 2. Run This (Create Table):

```kql
.create table sqTelemetry (
    siteId: string, assetId: string, oem: string, sourceTimestamp: datetime,
    battery_200_DailyWhExp: real, battery_200_DailyWhExp_dl: string,
    battery_200_DailyWhImp: real, battery_200_DailyWhImp_dl: string,
    battery_200_IncWhExp: real, battery_200_IncWhExp_dl: string,
    battery_200_IncWhImp: real, battery_200_IncWhImp_dl: string,
    battery_200_TotWhExp: real, battery_200_TotWhExp_dl: string,
    battery_200_TotWhImp: real, battery_200_TotWhImp_dl: string,
    battery_200_W: real, battery_200_W_dl: string,
    battery_713_SoC: real, battery_713_SoC_dl: string,
    battery_713_SoH: real, battery_713_SoH_dl: string,
    grid_200_DailyWhExp: real, grid_200_DailyWhExp_dl: string,
    grid_200_DailyWhImp: real, grid_200_DailyWhImp_dl: string,
    grid_200_IncWhExp: real, grid_200_IncWhExp_dl: string,
    grid_200_IncWhImp: real, grid_200_IncWhImp_dl: string,
    grid_200_TotWhExp: real, grid_200_TotWhExp_dl: string,
    grid_200_TotWhImp: real, grid_200_TotWhImp_dl: string,
    grid_200_W: real, grid_200_W_dl: string,
    load_200_IncWhExp: real, load_200_IncWhExp_dl: string,
    load_200_IncWhImp: real, load_200_IncWhImp_dl: string,
    load_200_TotWhExp: real, load_200_TotWhExp_dl: string,
    load_200_TotWhImp: real, load_200_TotWhImp_dl: string,
    load_200_W: real, load_200_W_dl: string,
    pv_200_DailyWhExp: real, pv_200_DailyWhExp_dl: string,
    pv_200_IncWhExp: real, pv_200_IncWhExp_dl: string,
    pv_200_IncWhImp: real, pv_200_IncWhImp_dl: string,
    pv_200_TotWhExp: real, pv_200_TotWhExp_dl: string,
    pv_200_TotWhImp: real, pv_200_TotWhImp_dl: string,
    pv_200_W: real, pv_200_W_dl: string
)
```

### 3. Verify:

```kql
sqTelemetry | getschema | count
```

**Expected:** 56 columns ✅

---

## 📌 Key Points

- **56 total columns** (4 base + 26 metrics + 26 data labels)
- Each metric has a corresponding `_dl` field (VALID/SUSPECT/INVALID)
- Data labels default to "VALID" for sample data
- Source database: **eventhouse**
- Target database: **eventhouseVPP**

---

## 🔥 Files Ready

1. **create_sqTelemetry_table.kql** - Full create script
2. **insert_sample_data.kql** - Insert April 1 data (needs database name update)
3. **EXECUTION_GUIDE.md** - Detailed step-by-step guide

---

**Start with Step 1! Open Fabric and create the table.** 🚀
