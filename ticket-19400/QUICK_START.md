# 🚀 QUICK START - Ticket 19400 Validation

**Goal:** Validate 8,188 enrolled DSGS sites have Leap Contracts in Asset Registry

---

## ⚡ **3-STEP EXECUTION**

### **Step 1: Run Query** (2 minutes)
1. Open **Fabric/Eventhouse**
2. Load: `ticket-19400/DSGS_LeapContract_Validation_READY.kql`
3. Click **"Run"**
4. Wait ~30-60 seconds

### **Step 2: Export Results** (1 minute)
1. Scroll to **"SITES MISSING LEAP CONTRACTS"** table
2. Click **Export** → **CSV**
3. Save as: `dsgs_sites_missing_leap_contracts_20260529.csv`

### **Step 3: Report to AR Team** (5 minutes)
1. Email CSV to: `ashok.bhaskar@qcells.com`, `chanhyup.kim@qcells.com`
2. CC: Shuai Zhang, Juan Culebro, Kai Xu, Sanjeev Lakkaraju
3. Use email template from `VALIDATION_SUMMARY.md`

---

## 📊 **WHAT TO EXPECT**

### **Query Output:**
```
VALIDATION SUMMARY
------------------------------------------
Total Enrolled DSGS Sites:        8,188
Sites WITH Leap Contract:         ???  (calculated)
Sites MISSING Leap Contract:      ???  (calculated)

▼ Full Validation Results Table
  siteId      | meterId                              | leap_contract_status
  ------------|--------------------------------------|----------------------
  100002495   | a1b2c3d4-...                        | Has Leap Contract
  100002784   | null                                | Missing Leap Contract
  ...

▼ Sites Missing Leap Contracts Table  ← EXPORT THIS!
  siteId
  -----------
  100002784
  400001234
  ...
```

---

## 📁 **KEY FILES**

| What You Need | File | Lines |
|---------------|------|-------|
| **🔥 Main Query** | `DSGS_LeapContract_Validation_READY.kql` | 1,741 |
| Documentation | `README.md` | Comprehensive guide |
| Summary | `VALIDATION_SUMMARY.md` | Detailed summary |
| This guide | `QUICK_START.md` | You are here |

---

## 📧 **EMAIL TEMPLATE (Copy & Paste)**

```
Subject: DSGS Sites Missing Leap Contracts in Asset Registry - Action Required

Hi Ashok and Chanhyup,

I've validated the 8,188 enrolled DSGS sites against Asset Registry Leap Contracts.

RESULTS:
- Total sites: 8,188
- Missing Leap Contracts: [SEE ATTACHED CSV]

REQUEST:
Please add Leap Contracts in AR for the sites listed in the attached CSV. 
We need all sites validated before extracting April & May 2026 interval data.

Once completed, let me know so I can re-validate.

Thanks!
Jagan

CC: Shuai Zhang, Juan Culebro, Kai Xu, Sanjeev Lakkaraju
```

---

## ⏭️ **AFTER AR UPDATE**

1. Wait for AR team confirmation
2. Re-run `DSGS_LeapContract_Validation_READY.kql`
3. Verify: "Sites MISSING Leap Contract: 0"
4. ✅ Proceed with April & May data extraction

---

## ❓ **TROUBLESHOOTING**

**Query too large?**
- The query has 8,188 site IDs embedded (1,741 lines)
- If Kusto/Fabric rejects it, we can batch it into smaller chunks
- Contact me if this happens

**Different results expected?**
- This validates CURRENT state of Asset Registry
- No date filters (Leap Contracts are enrollment records, not time-series)

**Need to regenerate query?**
```powershell
cd ticket-19400
python generate_validation_query.py
# Outputs: DSGS_LeapContract_Validation_READY.kql
```

---

**Ready? Open `DSGS_LeapContract_Validation_READY.kql` and hit Run!** 🚀
