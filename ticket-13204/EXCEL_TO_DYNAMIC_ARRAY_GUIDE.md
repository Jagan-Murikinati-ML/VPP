# Convert Excel Site IDs to KQL Dynamic Array

**Problem:** Production workspace has no write permissions (can't create tables)  
**Solution:** Manually convert Excel site IDs to dynamic array in KQL script

---

## 📊 STEP 1: PREPARE EXCEL DATA

**Open:** `Initial DSGS Site List 2026.xlsx`

**Column A contains Site IDs:**
```
Site Id
400040232
400040229
400037443
400037444
...
(7,700 total rows)
```

---

## 🔧 STEP 2: USE EXCEL FORMULA TO FORMAT

**Add a new column (Column S or any empty column):**

**In cell S2, enter this formula:**
```excel
="    """ & A2 & ""","
```

**What this does:**
- Wraps each site ID in quotes
- Adds comma at the end
- Adds indentation (4 spaces)

**Example output in Column S:**
```
    "400040232",
    "400040229",
    "400037443",
    "400037444",
```

**Drag formula down** to all 7,700 rows

---

## 📋 STEP 3: COPY FORMATTED VALUES

**Select Column S (all 7,700 cells with formula results)**

**Copy** (Ctrl+C)

**Result in clipboard:**
```
    "400040232",
    "400040229",
    "400037443",
    ... (7,700 lines)
    "400099999",
```

---

## 📝 STEP 4: PASTE INTO KQL SCRIPT

**Open:** `DSGS_2026_April_Extraction_MODIFIED.kql`

**Find line 48-54:**
```kql
let dsgs_site_list = dynamic([
    "400040232",
    "400040229",
    "400037443"
    // TODO: Paste all 7,700 site IDs here
]);
```

**Replace with:**
```kql
let dsgs_site_list = dynamic([
    // PASTE ALL 7,700 LINES HERE
    "400040232",
    "400040229",
    "400037443",
    "400037444",
    ... (paste all 7,700 lines)
    "400099999"  // ← Note: LAST line has NO comma!
]);
```

**IMPORTANT:** Remove comma from last site ID!

---

## ⚠️ COMMON ISSUES & FIXES

### **Issue 1: Comma on last item**

**Wrong:**
```kql
let dsgs_site_list = dynamic([
    "400040232",
    "400099999",  // ← Extra comma causes error!
]);
```

**Correct:**
```kql
let dsgs_site_list = dynamic([
    "400040232",
    "400099999"  // ← No comma on last item ✅
]);
```

**Fix:** Manually remove comma from very last line before pasting

---

### **Issue 2: File too large**

**Symptom:** Script file becomes huge (multiple MB)

**Workaround:**
```kql
// Split into chunks of 1000 sites each

let dsgs_site_list_1 = dynamic([
    "400040232",
    ... (sites 1-1000)
]);

let dsgs_site_list_2 = dynamic([
    "400041000",
    ... (sites 1001-2000)
]);

// ... continue for all chunks

let dsgs_site_list = 
    array_concat(
        dsgs_site_list_1,
        dsgs_site_list_2,
        dsgs_site_list_3,
        dsgs_site_list_4,
        dsgs_site_list_5,
        dsgs_site_list_6,
        dsgs_site_list_7,
        dsgs_site_list_8
    );
```

---

### **Issue 3: Query timeout (too many sites)**

**Symptom:** KQL query times out with 7,700 sites

**Workaround:** Process in batches

```kql
// Batch 1: Sites 1-2500
let dsgs_site_list = dynamic([
    "400040232",
    ... (first 2,500 sites)
]);

// Run full script for Batch 1
// Export results

// Then change to Batch 2: Sites 2501-5000
let dsgs_site_list = dynamic([
    "400050000",
    ... (next 2,500 sites)
]);

// Run again for Batch 2
// Combine CSV files afterward
```

---

## 🎯 ALTERNATIVE: USE EXCEL CONCATENATE

**If formula approach is too slow:**

### **Method 1: Excel CONCATENATE**

**Column S2:**
```excel
=CONCATENATE("    """, A2, """,")
```

**Drag down to all rows**

---

### **Method 2: Excel TEXTJOIN (Modern Excel)**

**Single cell formula to generate entire array:**

**In cell S2:**
```excel
=TEXTJOIN(CHAR(10), TRUE, "    """ & A2:A7702 & """,")
```

**Result:** Entire dynamic array in one cell (copy and paste)

---

### **Method 3: Python Script (If you're comfortable)**

**Create:** `excel_to_kql.py`

```python
import pandas as pd

# Read Excel
df = pd.read_excel('Initial DSGS Site List 2026.xlsx')

# Get Site Id column
site_ids = df['Site Id'].astype(str).tolist()

# Format for KQL
kql_array = 'let dsgs_site_list = dynamic([\n'
for i, site_id in enumerate(site_ids):
    if i == len(site_ids) - 1:  # Last item
        kql_array += f'    "{site_id}"\n'
    else:
        kql_array += f'    "{site_id}",\n'
kql_array += ']);'

# Write to file
with open('site_list.kql', 'w') as f:
    f.write(kql_array)

print(f'Generated KQL array with {len(site_ids)} sites')
```

**Run:**
```bash
python excel_to_kql.py
```

**Output:** `site_list.kql` file with formatted dynamic array

---

## ✅ VALIDATION

**After pasting into script, test with small subset first:**

```kql
// Test with first 10 sites
let dsgs_site_list = dynamic([
    "400040232",
    "400040229",
    "400037443",
    "400037444",
    "400037445",
    "400037446",
    "400037447",
    "400037448",
    "400037449",
    "400037450"
]);

// Check count
print site_count = array_length(dsgs_site_list)
// Expected: 10

// Expand array to see values
print dsgs_site_list
```

**If test works, replace with full 7,700 sites**

---

## 📊 FINAL RESULT

**Your script will have:**

```kql
// Line 48-7750: Site list (7,700 lines)
let dsgs_site_list = dynamic([
    "400040232",
    "400040229",
    "400037443",
    ... (7,697 more lines)
    "400099999"
]);

// This array is then used to filter Asset Registry
let meterId =
    goldAdtPropertyMinMaxLatestViewV2
    ...
    | where siteId in (dsgs_site_list)  // ← Filters to Excel sites
    ...
```

---

## ⏱️ ESTIMATED TIME

- **Excel formula approach:** 5-10 minutes
- **Python script approach:** 15 minutes (if you know Python)
- **Manual typing:** DON'T DO THIS! (too error-prone)

---

## 🎯 RECOMMENDATION

**Best approach:** Excel formula method (simple, fast, no coding needed)

**Steps:**
1. Add formula in Column S: `="    """ & A2 & ""","`
2. Drag down to all 7,700 rows (5 seconds)
3. Copy Column S (Ctrl+C)
4. Paste into KQL script (Ctrl+V)
5. Remove comma from last line
6. Done! ✅

**Total time: ~10 minutes**
