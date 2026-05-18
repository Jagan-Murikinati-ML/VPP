# Quick Reference Card - Onboarding Call Today

**Print this or keep it open during your call!**

---

## 🎯 THE #1 MOST IMPORTANT QUESTION

### **"Do I edit code in a repository, or do I directly execute SQL on the database?"**

This determines your entire workflow!

**Answer A: "Edit code in repository"**
→ You'll write migration scripts, commit to Git, create PR, deploy via pipeline

**Answer B: "Execute SQL directly"**
→ You'll write SQL, run it on database, maybe save script to repo for documentation

**Answer C: "Both"**
→ You'll update code (models/entities), generate migrations, then deploy

---

## 📋 TOP 10 CRITICAL QUESTIONS (In Priority Order)

### 1. **Repository Access**
"What's the repository URL and how do I get access?"

### 2. **Database Access**
"How do I connect to the Postgres database? (Dev environment)"

### 3. **Migration Approach**
"Do you use migration scripts (Flyway/Liquibase) or code-first (Entity Framework)?"

### 4. **Data Types**
"What are the exact data types for these 4 new columns?"
- `auto_enrollment`: ?
- `utility_meter_id`: ?
- `utility_meter_serial_number`: ?
- `site_owner_authorization`: ?

### 5. **Kusto Function Location**
"Where is `getAllVppSitesV2()` located? In repo or directly in Kusto?"

### 6. **Which Function to Modify**
"Should I modify `getAllVppSitesV2()` or `getAllVppSites()`?"

### 7. **Data Pipeline**
"How does data flow from Postgres to Kusto? Do I need to update any pipeline config?"

### 8. **Example to Follow**
"Can you show me a previous PR where someone added database columns?"

### 9. **Testing Environment**
"Where should I test these changes before production?"

### 10. **Who Reviews My Work**
"Who should review my PR and approve the changes?"

---

## 📝 WHAT TO WRITE DOWN

### Repository Info
```
URL: _________________________________
Branch to use: _______________________
Path to migrations: __________________
```

### Database Connection
```
Host: ________________________________
Database name: _______________________
Username: ____________________________
Tool to use: _________________________
```

### Kusto Info
```
Cluster URL: _________________________
Database: ____________________________
Function to modify: __________________
```

### Data Types (CRITICAL!)
```
auto_enrollment: ____________________
utility_meter_id: ___________________
utility_meter_serial_number: ________
site_owner_authorization: ___________
```

### Workflow
```
1. Create branch from: ______________
2. Make changes in: _________________
3. Test in: _________________________
4. Create PR, tag: __________________
5. Deploy to: _______________________
```

---

## 🚨 RED FLAGS - Ask for Clarification If You Hear:

❌ "Just run the SQL directly in production"
→ Ask: "Is there a dev environment I can test in first?"

❌ "We don't really have a process"
→ Ask: "Can you show me the last time someone made a similar change?"

❌ "The pipeline is complicated, don't worry about it"
→ Ask: "I need to understand it to make sure my changes work end-to-end"

❌ "We'll figure out the data types later"
→ Ask: "I need to know now so I can write the correct migration"

---

## ✅ GOOD SIGNS - You're on the Right Track:

✅ They show you a repository with clear structure
✅ They have a dev/staging environment for testing
✅ They show you an example of a previous similar change
✅ They have clear data type specifications
✅ They explain the deployment process step-by-step
✅ They assign you a mentor/buddy for questions

---

## 🎤 OPENING STATEMENT (Say This First)

"Hi everyone! Thanks for the onboarding. I'm coming from the Fabric team, so this is my first time working with this codebase. 

I've reviewed the ticket and I understand I need to:
1. Add 4 new columns to 3 Postgres tables
2. Update a Kusto function to include these columns
3. Ensure data flows from Postgres to Kusto

To do this efficiently, I need to understand:
- Where the code lives
- How you make database changes
- How the data pipeline works

Can we start with the repository and database access?"

---

## 📊 DECISION TREE - What Approach Are They Using?

```
START: How do you make database changes?
│
├─ "We use Flyway/Liquibase migration scripts"
│  → You'll write SQL migration files
│  → Files like: V1.2.3__Add_Site_Metadata.sql
│  → Commit to repo, pipeline runs migrations
│
├─ "We use Entity Framework / Code-First"
│  → You'll update C# entity classes
│  → Run: dotnet ef migrations add AddSiteMetadata
│  → Commit code, pipeline applies migrations
│
├─ "We write SQL and run it manually"
│  → You'll write SQL scripts
│  → Test in dev, then run in staging, then prod
│  → Save scripts to repo for documentation
│
└─ "We use [other tool]"
   → Ask them to show you an example
   → Follow the same pattern
```

---

## 🔄 DATA FLOW DIAGRAM (Draw This If Needed)

```
┌──────────────┐
│   Postgres   │  ← You add columns here
│   Database   │
└──────┬───────┘
       │
       │ Data Pipeline (Azure Data Factory? Sync Service?)
       │ ← You might need to update this
       ↓
┌──────────────┐
│    Kusto     │
│   Database   │
└──────┬───────┘
       │
       │ Kusto Function: getAllVppSitesV2()
       │ ← You definitely update this
       ↓
┌──────────────┐
│  Analytics   │
│  Dashboard   │
└──────────────┘
```

Ask: "Is this flow correct? What am I missing?"

---

## 💾 SAVE THESE DURING THE CALL

### Access Credentials
- [ ] Repository access granted
- [ ] Database credentials received
- [ ] Kusto access granted
- [ ] VPN/network access (if needed)

### Files to Bookmark
- [ ] Example PR/commit to follow
- [ ] Migration folder location
- [ ] Kusto function file location
- [ ] Pipeline configuration file

### Contacts
- [ ] Primary contact: _______________
- [ ] Database expert: _______________
- [ ] Kusto expert: __________________
- [ ] DevOps/Pipeline: _______________

---

## ⏱️ TIME MANAGEMENT

**If the call is 30 minutes:**
- 5 min: Introductions
- 10 min: Repository & database access walkthrough
- 10 min: Show example of similar change
- 5 min: Q&A and next steps

**If the call is 60 minutes:**
- 10 min: Introductions & context
- 15 min: Repository structure & access
- 15 min: Database & Kusto walkthrough
- 10 min: Pipeline explanation
- 10 min: Live demo of making a change

---

## 🎯 SUCCESS CRITERIA FOR THIS CALL

By the end, you should be able to answer:

✅ Where is the code? (Repository URL)
✅ How do I access the database? (Connection details)
✅ What's the process? (Migration scripts vs. code-first vs. manual SQL)
✅ What are the data types? (Exact types for 4 columns)
✅ Where is the Kusto function? (File path or Kusto cluster)
✅ What's an example? (Link to similar past change)
✅ Who can help me? (Contact names)

**If you can't answer these, ask more questions before the call ends!**

---

## 📞 AFTER THE CALL - IMMEDIATE NEXT STEPS

1. **Test your access**
   - [ ] Clone the repository
   - [ ] Connect to the database
   - [ ] Access Kusto cluster

2. **Find the example**
   - [ ] Review the example PR/commit they showed you
   - [ ] Understand the pattern

3. **Create a plan**
   - [ ] Write down the exact steps you'll take
   - [ ] Estimate time for each step

4. **Send a summary**
   - [ ] Email/message summarizing what you learned
   - [ ] Confirm your understanding
   - [ ] Ask any remaining questions

---

## 🆘 IF YOU GET STUCK

**During the call:**
"Can you show me on your screen? I'm a visual learner."

**After the call:**
"I'm trying to [do X] but getting [error Y]. Based on our call, I thought I should [do Z]. Can you clarify?"

**Always:**
- Ask questions publicly (in Teams/Slack channel)
- Document what you learn
- Don't guess - confirm

---

## 🎓 REMEMBER

- ✅ You're NEW to this codebase - asking questions is EXPECTED
- ✅ This is a SIMPLE task once you have the right info
- ✅ Better to ask "dumb" questions now than break production later
- ✅ Take notes - you'll reference them later

---

**Good luck! You've got this! 🚀**

**Pro tip:** Share your screen and take notes in this document during the call so they can see you're organized and engaged.

