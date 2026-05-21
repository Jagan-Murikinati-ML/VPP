# Sorting Test Plan - All Sortable Fields

## Supported Sort Fields (from code lines 182-188):

| Field Name | Data Type | Line | Notes |
|------------|-----------|------|-------|
| `site_number` | String (numeric) | 182 | Uses padded sorting |
| `site_name` | String | 183 | Simple string |
| `state` | String | 184 | Simple string (2 chars) |
| `zipPostalCode` | String | 185 | Simple string (5 chars) |
| `external_reference_id` | String | 186 | Simple string (accountNumber) |
| `program_name` | **Array** | 187 | **🔴 Uses tostring() - POTENTIAL BUG** |
| `oem_name` | String | 188 | Simple string |

---

## 🎯 Test Strategy

### **Already Tested:**
- ✅ `program_name` ASC - Works (sort of)
- ✅ `program_name` DESC - **BUG FOUND** (empty arrays first)

### **Need to Test:**
- ❓ `site_number` ASC/DESC
- ❓ `site_name` ASC/DESC
- ❓ `state` ASC/DESC
- ❓ `zipPostalCode` ASC/DESC
- ❓ `external_reference_id` ASC/DESC
- ❓ `oem_name` ASC/DESC

---

## 📋 Test Queries

### Test 1: site_number

**Ascending:**
```kusto
getAllVppSitesByUserIdV2(
    inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", 
    page_index=0, 
    page_size=10,
    sorting=dynamic([{"field": "site_number", "direction": "asc"}])
)
```

**Descending:**
```kusto
getAllVppSitesByUserIdV2(
    inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", 
    page_index=0, 
    page_size=10,
    sorting=dynamic([{"field": "site_number", "direction": "desc"}])
)
```

**Expected Result:** Smallest to largest (ASC), Largest to smallest (DESC)

---

### Test 2: site_name

**Ascending:**
```kusto
getAllVppSitesByUserIdV2(
    inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", 
    page_index=0, 
    page_size=10,
    sorting=dynamic([{"field": "site_name", "direction": "asc"}])
)
```

**Descending:**
```kusto
getAllVppSitesByUserIdV2(
    inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", 
    page_index=0, 
    page_size=10,
    sorting=dynamic([{"field": "site_name", "direction": "desc"}])
)
```

**Expected Result:** A-Z (ASC), Z-A (DESC)

---

### Test 3: state

**Ascending:**
```kusto
getAllVppSitesByUserIdV2(
    inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", 
    page_index=0, 
    page_size=10,
    sorting=dynamic([{"field": "state", "direction": "asc"}])
)
```

**Descending:**
```kusto
getAllVppSitesByUserIdV2(
    inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", 
    page_index=0, 
    page_size=10,
    sorting=dynamic([{"field": "state", "direction": "desc"}])
)
```

**Expected Result:** A-Z (ASC), Z-A (DESC)

---

### Test 4: oem_name

**Ascending:**
```kusto
getAllVppSitesByUserIdV2(
    inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", 
    page_index=0, 
    page_size=10,
    sorting=dynamic([{"field": "oem_name", "direction": "asc"}])
)
```

**Descending:**
```kusto
getAllVppSitesByUserIdV2(
    inputUserId="81ab4c51-a8d9-ef11-8eea-00224809f11c", 
    page_index=0, 
    page_size=10,
    sorting=dynamic([{"field": "oem_name", "direction": "desc"}])
)
```

**Expected Result:** Enphase, SolarEdge, Tesla (ASC), Tesla, SolarEdge, Enphase (DESC)

---

## 🎯 What to Check in Results

For each test, verify:

1. **ASC Order:**
   - Empty/null values appear **FIRST**
   - Values are in alphabetical order (A → Z or 0 → 9)
   
2. **DESC Order:**
   - Empty/null values appear **LAST**
   - Values are in reverse alphabetical order (Z → A or 9 → 0)

3. **Consistency:**
   - First record in ASC should be last record in DESC (if same data)
   - Last record in ASC should be first record in DESC

---

## 📊 Results Template

| Field | ASC Works? | DESC Works? | Notes |
|-------|------------|-------------|-------|
| site_number | ✅/❌ | ✅/❌ | |
| site_name | ✅/❌ | ✅/❌ | |
| state | ✅/❌ | ✅/❌ | |
| zipPostalCode | ✅/❌ | ✅/❌ | |
| external_reference_id | ✅/❌ | ✅/❌ | |
| program_name | ⚠️ | ❌ | Empty arrays first in DESC |
| oem_name | ✅/❌ | ✅/❌ | |

---

## 🔍 Expected Findings

**Hypothesis 1:** Only `program_name` has issues (because it's an array)
- Other fields use simple strings → should work fine

**Hypothesis 2:** All DESC sorts have issues (general sorting logic bug)
- If true, the problem is in the rank calculation logic (lines 191-196)

**Hypothesis 3:** Only `program_name` DESC has issues (array + DESC combination)
- If true, the problem is specifically line 187 with tostring()

---

## Next Steps

1. Run tests for site_name and oem_name first (simple strings)
2. If those work → Bug is specific to program_name (array handling)
3. If those fail → Bug is in general DESC sorting logic
4. Document findings
5. Create fix based on root cause
