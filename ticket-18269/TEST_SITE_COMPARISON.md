# Test Site Comparison - Site 100003907

## 🎯 **Site: 100003907** (The ONLY site with actual Type 1 OEM data in Query 1)

---

## 📊 **Current Report Data (data.csv)**

```
site_ids:              100003907
oem_siteId:            100003907
oem_name:              Qcells
customer_name:         Di Lu
customer_email:        isdiluapril@gmail.com
site_address:          2847 Varden Ave San Jose CA 95124
state:                 CA
installer_name:        Axia Solar Corp
isTPORegistered:       False
isVppRegistered:       True
isLeapRegistered:      True
leap_meter_id:         0d64cf4c-2814-41fa-bf96-1146c3e36e76
account_number:        APPTPO-2505725520
APP_TPO_AccountId:     2505725520.0
wMaxRtg:               (empty)
system_size_kw:        0.0
productInfo_prodCode:  (empty)
productInfo_prodMfr:   (empty)
productInfo_prodName:  (empty)
productInfo_prodType:  (empty)
productInfo_prodSubType: (empty)
system_status_1h_online: online
last_data_timestamp:   2026-05-18 07:00:12
```

---

## 🔍 **Asset Registry Data (Query 1 & Query 3)**

### **From Query 1 (OEM Info):**

```
siteId:                100003907
type0_oemName:         Qcells
type0_oemSiteId:       100003907
type1_oemName:         Qcells      ⬅️ HAS TYPE 1!
type1_oemSiteId:       SSMAK9HTBP  ⬅️ HAS TYPE 1!
```

### **From Query 3 (Battery Devices):**

Site `100003907` appears in the battery devices list ✅

---

## 🔥 **KEY FINDINGS**

### **1. Type 1 OEM Information:**

**Current Report Shows:**
- `oem_name`: Qcells
- `oem_siteId`: 100003907

**Asset Registry Has:**
- Type 0: `Qcells` / `100003907`
- **Type 1: `Qcells` / `SSMAK9HTBP`** ⬅️ **MISSING FROM REPORT!**

**This is exactly what the ticket is asking for!** We need to add Type 1 columns.

---

### **2. Battery Flag:**

**Current Report Shows:**
- `wMaxRtg`: (empty)
- `productInfo_prodSubType`: (empty)

**Asset Registry Shows:**
- Site appears in Query 3 (battery devices list) ✅
- But product info fields are empty in current report

**Conclusion:** This site HAS a battery device, but we need to use relationship-based detection (not product fields).

---

## 🧪 **What Type 1 OEM Represents in This Case**

### **Interpretation:**

Site `100003907` has:
- Type 0 OEM: `Qcells` / `100003907` (site ID)
- Type 1 OEM: `Qcells` / `SSMAK9HTBP` (device serial number?)

**Likely Scenario:**
- The site has a Qcells solar inverter (Type 0)
- The site has a Qcells battery (Type 1) with serial/ID `SSMAK9HTBP`

**Alternative Scenario:**
- Type 0 could be solar/inverter OEM
- Type 1 could be battery/storage OEM
- In this case, both are Qcells (same manufacturer)

---

## 📋 **Expected Report Output for This Site**

After implementing the changes, the report should show:

```csv
site_ids,oem_name,oem_siteId,type1_oem_name,type1_oem_siteId,has_battery,...
100003907,Qcells,100003907,Qcells,SSMAK9HTBP,Yes,...
```

---

## 🔍 **Additional Test Sites Needed**

To fully understand Type 1 OEM, we should also check:

### **1. Qcells + Tesla (328 sites from Query 2):**

Example: Find a site with:
- Type 0: Qcells (solar)
- Type 1: Tesla (battery)

Expected output:
```csv
site_ids,oem_name,oem_siteId,type1_oem_name,type1_oem_siteId,has_battery,...
4000XXXXX,Qcells,XXXXXXX,Tesla,XXXXXXX-XXXX-...,Yes,...
```

### **2. Enphase + Tesla (67 sites from Query 2):**

Example: Find a site with:
- Type 0: Enphase (solar microinverters)
- Type 1: Tesla (battery)

Expected output:
```csv
site_ids,oem_name,oem_siteId,type1_oem_name,type1_oem_siteId,has_battery,...
4000XXXXX,Enphase,XXXXXXX,Tesla,XXXXXXX-XXXX-...,Yes,...
```

### **3. SolarEdge + Tesla (20 sites from Query 2):**

Example: Find a site with:
- Type 0: SolarEdge (solar inverter)
- Type 1: Tesla (battery)

Expected output:
```csv
site_ids,oem_name,oem_siteId,type1_oem_name,type1_oem_siteId,has_battery,...
4000XXXXX,SolarEdge,XXXXXXX,Tesla,XXXXXXX-XXXX-...,Yes,...
```

---

## ❓ **Questions for Shuai - With Context**

### **Question 1: Output Format Confirmation**

Based on site `100003907`, should the report show:

```csv
site_ids,oem_name,oem_siteId,type1_oem_name,type1_oem_siteId,has_battery
100003907,Qcells,100003907,Qcells,SSMAK9HTBP,Yes
```

**Is this the expected format?**

---

### **Question 2: Type 1 OEM Interpretation**

For site `100003907`:
- Type 0: Qcells / 100003907
- Type 1: Qcells / SSMAK9HTBP

**What does Type 1 represent here?**
- A) Battery device serial number/ID
- B) Second OEM (but same manufacturer)
- C) Different interpretation?

---

### **Question 3: Sites with Different OEM Combinations**

Can you provide examples of:
1. **Qcells solar + Tesla battery** site
2. **Enphase solar + Tesla battery** site
3. **SolarEdge solar + Tesla battery** site

We want to confirm the expected output for these scenarios.

---

### **Question 4: Battery Flag Logic**

Site `100003907` has:
- `wMaxRtg`: empty
- `productInfo_prodSubType`: empty
- But appears in battery devices list (Query 3)

**Should we use:**
- A) Product info fields (may have missing data)
- B) Relationship-based detection (check for battery device in Asset Registry)

---

## 📝 **Next Steps**

1. ✅ Analyze site 100003907 (DONE)
2. 🔄 Run additional query to find examples of:
   - Qcells + Tesla
   - Enphase + Tesla
   - SolarEdge + Tesla
3. 🔄 Ask Shuai the 4 questions above
4. 🔄 Once confirmed, implement the solution
