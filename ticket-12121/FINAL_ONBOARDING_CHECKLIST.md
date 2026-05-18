# Final Onboarding Checklist - Based on Shaun's Comment

**Updated:** After Shaun's clarification  
**Database:** asset-registry (Postgres)  
**Pipelines:** silverProgramInfo, silverProgramSiteInfo  

---

## 🎯 YOUR COMPLETE TASK SCOPE

### 1. Postgres Changes (asset-registry database)
- [ ] `asset.tb_bas_program_info` → Add `auto_enrollment`
- [ ] `asset.tb_bas_site` → Add `utility_meter_id`
- [ ] `asset.tb_bas_site` → Add `utility_meter_serial_number`
- [ ] `asset.tb_opr_program_site_info` → Add `site_owner_authorization`

### 2. Pipeline Changes
- [ ] Update `silverProgramInfo` → Include `auto_enrollment`
- [ ] Update `silverProgramSiteInfo` → Include `site_owner_authorization`
- [ ] **CLARIFY:** Pipeline for `utility_meter_id` and `utility_meter_serial_number`?

### 3. Kusto Changes
- [ ] Update `getAllVppSitesV2()` → Query all 4 new columns

---

## 📋 TOP 10 QUESTIONS FOR ONBOARDING (PRIORITIZED)

### 🔴 CRITICAL (Must answer today)

#### 1. Repository & Access
**"What's the repository URL and can I get access right now?"**
- Write down: ___________________________________

#### 2. Data Types (CRITICAL!)
**"What are the exact data types for these 4 columns?"**

| Column | Data Type | Nullable? | Default | Constraints |
|--------|-----------|-----------|---------|-------------|
| `auto_enrollment` | _______ | Y/N | _______ | __________ |
| `utility_meter_id` | _______ | Y/N | _______ | __________ |
| `utility_meter_serial_number` | _______ | Y/N | _______ | __________ |
| `site_owner_authorization` | _______ | Y/N | _______ | __________ |

#### 3. Pipeline Locations
**"Where are the `silverProgramInfo` and `silverProgramSiteInfo` pipelines?"**
- [ ] Azure Data Factory?
- [ ] In the repository? (path: _________________)
- [ ] Databricks?
- [ ] Other: ___________________________________

#### 4. Utility Meter Columns Pipeline
**"Shaun mentioned updating 2 pipelines for 2 columns. What about `utility_meter_id` and `utility_meter_serial_number`?"**
- [ ] Is there a `silverSiteInfo` pipeline?
- [ ] Do they auto-sync?
- [ ] Different process?

#### 5. Database Access
**"How do I connect to the asset-registry Postgres database (dev environment)?"**
- Host: ___________________________________
- Database: asset-registry
- Username: ___________________________________
- Password: (will be provided securely)
- Tool: ___________________________________

---

### 🟡 IMPORTANT (Need to know before coding)

#### 6. Pipeline Update Process
**"How do I update a pipeline? Can you show me an example?"**
- [ ] Edit JSON/YAML file?
- [ ] Use Azure portal?
- [ ] Code-based configuration?
- Example file: ___________________________________

#### 7. Migration Approach
**"How do you make database schema changes?"**
- [ ] Flyway migrations
- [ ] Liquibase
- [ ] Entity Framework
- [ ] Manual SQL scripts
- [ ] Other: ___________________________________
- Location in repo: ___________________________________

#### 8. Kusto Access
**"How do I access the Kusto cluster?"**
- Cluster URL: ___________________________________
- Database: ___________________________________
- Where is `getAllVppSitesV2()`: ___________________________________

#### 9. Testing Process
**"How do I test these changes end-to-end?"**
- [ ] Dev environment available?
- [ ] Can I run pipelines in dev?
- [ ] How to verify data flows Postgres → Kusto?

#### 10. Code Review
**"Who should review my PR and what's the approval process?"**
- Reviewers: ___________________________________
- Approval needed from: ___________________________________

---

## 🎤 OPENING STATEMENT FOR THE CALL

**Say this first:**

> "Hi everyone! Thanks for the onboarding. I saw Shaun's comment clarifying that I need to:
> 1. Modify tables in asset-registry Postgres
> 2. Update silverProgramInfo and silverProgramSiteInfo pipelines
> 3. Update the getAllVppSitesV2 Kusto function
>
> I have a few critical questions to get started efficiently. Can we start with repository access and the data types for the new columns?"

---

## 📝 CRITICAL INFO TO WRITE DOWN

### Repository
```
URL: ___________________________________
Branch: ___________________________________
Path to migrations: ___________________________________
Path to pipelines: ___________________________________
Path to Kusto functions: ___________________________________
```

### Database (asset-registry)
```
Connection string (dev): ___________________________________
Tool to use: ___________________________________
Schema: asset (confirmed)
```

### Pipelines
```
silverProgramInfo location: ___________________________________
silverProgramSiteInfo location: ___________________________________
[Site pipeline?] location: ___________________________________
How to update: ___________________________________
How to test: ___________________________________
```

### Kusto
```
Cluster URL: ___________________________________
Database: ___________________________________
getAllVppSitesV2 location: ___________________________________
```

---

## ❓ CLARIFICATION TO SEND TO SHAUN

**Before or during the call, ask:**

> Hi @Shaun Roach,
>
> Quick clarification on your comment:
>
> You mentioned updating pipelines for `auto_enrollment` and `site_owner_authorization`. 
>
> What about the other 2 columns (`utility_meter_id` and `utility_meter_serial_number`) being added to `tb_bas_site`?
> - Is there a separate pipeline (e.g., `silverSiteInfo`) I need to update?
> - Or do these sync automatically?
>
> Want to make sure I don't miss anything!
>
> Thanks!

---

## ✅ SUCCESS CRITERIA FOR ONBOARDING CALL

By the end of the call, you MUST have:

- [x] Repository URL and access granted
- [x] Data types for all 4 columns (written down!)
- [x] Database connection details (dev)
- [x] Pipeline locations identified
- [x] Clarification on utility meter columns pipeline
- [x] Example of how to update a pipeline
- [x] Kusto access information
- [x] Name of person to ask questions

**If you don't have these, ask more questions before the call ends!**

---

## 🚀 AFTER THE CALL - IMMEDIATE ACTIONS

### 1. Test Your Access (15 minutes)
- [ ] Clone the repository
- [ ] Connect to asset-registry database
- [ ] Access Kusto cluster
- [ ] Locate the pipeline files

### 2. Share with Me
- [ ] Share repository URL
- [ ] Share what you learned about pipelines
- [ ] I'll help you find everything and write the code

### 3. Send Summary Email
**Template:**

> Hi team,
>
> Thanks for the onboarding! Here's my understanding:
>
> **Postgres Changes:**
> - Add 4 columns to 3 tables in asset-registry database
> - Data types: [list them]
>
> **Pipeline Changes:**
> - Update silverProgramInfo for auto_enrollment
> - Update silverProgramSiteInfo for site_owner_authorization
> - [Clarify utility meter columns]
>
> **Kusto Changes:**
> - Update getAllVppSitesV2() function
>
> **Next Steps:**
> 1. [Your plan]
> 2. [Timeline]
>
> Please correct me if I misunderstood anything!
>
> Thanks!

---

## 🎯 ESTIMATED TIMELINE (After Onboarding)

**Once you have all the info:**

| Task | Time | Status |
|------|------|--------|
| Write Postgres migrations | 1 hour | ⏳ |
| Update pipeline configs | 2 hours | ⏳ |
| Update Kusto function | 30 min | ⏳ |
| Test in dev environment | 2 hours | ⏳ |
| Code review & fixes | 1 hour | ⏳ |
| **TOTAL** | **6-7 hours** | |

**Realistic completion:** 1-2 days after onboarding

---

## 🆘 IF THINGS GO WRONG

### If they can't give you data types:
"I can't write the migrations without knowing the data types. Can someone from the product/business team provide the requirements?"

### If pipelines are complex:
"Can you pair with me for 30 minutes to update the first pipeline together? Then I can do the second one myself."

### If you can't access the database:
"I need dev database access to test my changes. Who can grant this access?"

### If timeline is unclear:
"When do you need this completed? I want to set realistic expectations."

---

## 💡 PRO TIPS

### During the Call:
- ✅ Take notes in this document (share your screen)
- ✅ Ask them to show their screen when explaining
- ✅ Don't pretend to understand - ask for clarification
- ✅ Record the meeting (if allowed)

### After the Call:
- ✅ Test all access immediately
- ✅ Send summary email (creates paper trail)
- ✅ Share repo with me for help
- ✅ Start with the easiest task first (probably Postgres migrations)

### General:
- ✅ Ask questions publicly (Teams/Slack channel)
- ✅ Document everything you learn
- ✅ Better to over-communicate than under-communicate

---

## 📞 FINAL CHECKLIST

**Before the call:**
- [ ] Read this document
- [ ] Read Shaun's comment analysis
- [ ] Prepare to take notes
- [ ] Have questions ready

**During the call:**
- [ ] Get repository access
- [ ] Get data types (CRITICAL!)
- [ ] Understand pipeline update process
- [ ] Clarify utility meter columns
- [ ] Get database/Kusto access info

**After the call:**
- [ ] Test all access
- [ ] Share repo with me
- [ ] Send summary email
- [ ] Start coding!

---

**You're fully prepared! Good luck! 🚀**

**Remember:** You're new to this codebase. Asking questions is expected and professional. Don't guess - confirm everything!

