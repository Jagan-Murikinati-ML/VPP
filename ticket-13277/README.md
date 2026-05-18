# Ticket #13277 - Implementation Guide

**Task:** Add External Reference ID to getAllVppSitesByUserId function

---

## 📁 Files in This Folder

### Original Ticket Files:
- `ticket.md` - Your ticket
- `parent-ticket.md` - Parent ticket with business context
- `getAllVPPSitesByUserId_function.csv` - Current function code
- `getsiteproperties_function.csv` - Helper function code

### Implementation Guide (Read in Order):
1. `01_UNDERSTANDING_TICKET.md` - What the ticket asks for
2. `02_UNDERSTANDING_FUNCTION.md` - How the function works
3. `03_IMPLEMENTATION.md` - What to change (2 lines!)
4. `04_HOW_TO_EDIT_FUNCTION.md` - How to edit KQL functions
5. `05_COMPLETE_MODIFIED_FUNCTION.md` - Full code with changes
6. `06_TESTING.md` - How to test
7. `07_DEPLOYMENT.md` - Deployment process

---

## 🎯 Quick Summary

### What You're Doing:
Adding a new field `external_reference_id` to the JSON response of `getAllVppSitesByUserId` function.

### The Change:
**Add ONLY 2 lines of code:**

**Line 1:** Extract accountNumber
```kql
accountNumber = tostring(assetRegistrationInfo['accountNumber'])
```

**Line 2:** Add to JSON
```kql
'external_reference_id', coalesce(accountNumber, '-'),
```

### Why It's Simple:
- `assetRegistrationInfo` is already fetched by `GetSiteProperties()`
- Just extract the `accountNumber` from it
- No new queries or joins needed!

---

## ⏱️ Time Estimate: 2-3 hours

---

## 🚀 Start Here:

**If you're new:** Read files 01 → 07 in order

**If you just want the code:** Jump to `05_COMPLETE_MODIFIED_FUNCTION.md`

**If you need help editing:** Read `04_HOW_TO_EDIT_FUNCTION.md`

---

## 📝 Key Information

**External Reference ID =** Account Number from assetRegistrationInfo

**Example value:** "APPTPO-2501513034"

**When empty:** Show "-"

**Field name in response:** `external_reference_id`

---

## ✅ Success Criteria

- [ ] Function runs without errors
- [ ] `external_reference_id` appears in JSON response
- [ ] Shows account number when available
- [ ] Shows "-" when not available
- [ ] Pagination still works
- [ ] Frontend team can consume the data

---

**Start with:** `01_UNDERSTANDING_TICKET.md`

**Good luck!** 🎉

