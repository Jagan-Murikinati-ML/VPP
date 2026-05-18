# Step 7: Deployment Process

## Before You Deploy

### 1. Get Approvals
- [ ] Team lead reviewed the code
- [ ] Testing completed in DEV
- [ ] Frontend team notified

### 2. Save Backup
Save the original function to a file before deploying to PROD:
```kql
.show function getAllVppSitesByUserId
```
Copy the output to `backup_original_function.txt`

---

## Deployment Steps

### Environment Order:
```
DEV → Test → QA → Frontend Testing → PROD
```

---

### Step 1: Deploy to DEV

**Action:** Run the modified function in DEV database

**Test:**
```kql
getAllVppSitesByUserId('81ab4c51-a8d9-ef11-8eea-00224809f11c', 0, 5)
```

**Verify:** Check all test cases from `06_TESTING.md`

---

### Step 2: Deploy to QA

**Action:** Run the modified function in QA database

**Test:**
```kql
getAllVppSitesByUserId('13d79b62-cf04-f011-bae2-6045bdf0782b', 0, 5)
```

**Verify:** Frontend team tests integration

---

### Step 3: Deploy to PROD

**IMPORTANT:** Get approval from team lead before this step!

**Action:** Run the modified function in PROD database

**Monitor:** Watch for errors in logs for 24 hours

---

## Rollback Plan

If something goes wrong:

### Immediate Rollback:
1. Open backup file `backup_original_function.txt`
2. Copy the original function
3. Wrap in `.create-or-alter function`
4. Run in Fabric Query Editor
5. Function reverts to original version

**Example:**
```kql
.create-or-alter function getAllVppSitesByUserId(inputUserId:string="", page:int=0, page_size:int=10) {
    // PASTE ORIGINAL FUNCTION BODY FROM BACKUP
}
```

---

## Post-Deployment

### Checklist:
- [ ] Function deployed to all environments
- [ ] Tested in each environment
- [ ] Frontend team confirmed integration works
- [ ] No errors in logs
- [ ] Update ADO ticket with completion notes
- [ ] Close ticket

---

### Update ADO Ticket:

**Title:** Completed - Added External Reference ID to getAllVppSitesByUserId

**Description:**
```
✅ Modified getAllVppSitesByUserId function to include external_reference_id field
✅ Field extracts accountNumber from assetRegistrationInfo
✅ Returns account number when available, "-" when not available
✅ Tested in DEV, QA, and PROD
✅ Frontend team confirmed working
✅ Deployed to production on [DATE]

Changes made:
- Added accountNumber extraction in Step 8 (line 98)
- Added external_reference_id to JSON response (line 107)

No new database queries or joins required - used existing assetRegistrationInfo from GetSiteProperties.
```

---

## Documentation

Save these files for future reference:
- `backup_original_function.txt` - Original function
- `modified_function.txt` - Your modified version
- Screenshots of test results

---

## Timeline:

**Estimated Total Time:** 2-3 hours

| Phase | Time |
|-------|------|
| Understanding ticket & function | 30 min |
| Code changes | 15 min |
| Testing in DEV | 30 min |
| Deploy to QA | 15 min |
| Frontend testing | 30 min |
| Deploy to PROD | 15 min |
| Documentation | 15 min |

---

**Congratulations! Ticket completed!** 🎉

