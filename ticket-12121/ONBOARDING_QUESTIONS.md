# Onboarding Questions Checklist - VPP Site Table Extension

**Date:** Today  
**Purpose:** Get all information needed to complete the ticket  
**Attendees:** [Fill in names during the call]

---

## 📍 SECTION 1: REPOSITORY & CODE LOCATION

### Q1: Where is the source code?
- [ ] What is the GitHub/Azure DevOps repository URL?
- [ ] Which branch should I work on? (main, develop, feature branch?)
- [ ] Do I need access permissions? If yes, who grants them?

### Q2: Repository structure
- [ ] Where are the database-related files located in the repo?
  - Example: `/database/migrations/`, `/src/models/`, `/sql/`
- [ ] Is there a README or documentation I should read first?

---

## 🗄️ SECTION 2: POSTGRES DATABASE

### Q3: How do I access the Postgres database?
- [ ] What is the database server hostname/connection string?
- [ ] Do I have credentials for:
  - [ ] Development environment
  - [ ] Staging environment
  - [ ] Production environment (read-only?)
- [ ] What tool do you use to connect? (pgAdmin, DBeaver, Azure Data Studio, VS Code extension?)

### Q4: Where are these tables located?
- [ ] Database name: `______________`
- [ ] Schema name: `asset` (confirmed?)
- [ ] Can you show me where these tables are:
  - `asset.tb_bas_program_info`
  - `asset.tb_bas_site`
  - `asset.tb_opr_program_site_info`

### Q5: **CRITICAL: How do I make database changes?**

**Option A: Direct SQL Execution**
- [ ] Do I write SQL and execute it directly on the database?
- [ ] If yes, do I need approval before running it?
- [ ] Should I create a SQL script file and commit it to the repo?

**Option B: Migration Scripts (Recommended approach)**
- [ ] Do you use a migration tool? Which one?
  - [ ] Flyway
  - [ ] Liquibase
  - [ ] Entity Framework Migrations
  - [ ] Alembic (Python)
  - [ ] Other: `______________`
- [ ] Where are existing migration files stored in the repo?
- [ ] What is the naming convention for migration files?
- [ ] How do I run migrations? (command/script)

**Option C: Code-First Approach**
- [ ] Do you use an ORM (Object-Relational Mapping)?
  - [ ] Entity Framework (C#)
  - [ ] Hibernate (Java)
  - [ ] SQLAlchemy (Python)
  - [ ] Other: `______________`
- [ ] Where are the entity/model classes?
- [ ] Do I update the code and generate migrations automatically?

### Q6: Data types and constraints
For each new column, I need to know:

**`asset.tb_bas_program_info.auto_enrollment`**
- [ ] Data type: `______________` (BOOLEAN, VARCHAR, INT?)
- [ ] Nullable: YES / NO
- [ ] Default value: `______________`
- [ ] Any constraints: `______________`

**`asset.tb_bas_site.utility_meter_id`**
- [ ] Data type: `______________` (VARCHAR(255)? TEXT? INT?)
- [ ] Nullable: YES / NO
- [ ] Default value: `______________`
- [ ] Unique constraint: YES / NO

**`asset.tb_bas_site.utility_meter_serial_number`**
- [ ] Data type: `______________`
- [ ] Nullable: YES / NO
- [ ] Default value: `______________`
- [ ] Any constraints: `______________`

**`asset.tb_opr_program_site_info.site_owner_authorization`**
- [ ] Data type: `______________` (BOOLEAN, VARCHAR, INT?)
- [ ] Nullable: YES / NO
- [ ] Default value: `______________`
- [ ] Any constraints: `______________`

### Q7: Existing data
- [ ] Are there existing rows in these tables?
- [ ] If yes, approximately how many rows in each table?
- [ ] Do existing rows need default values for new columns?
- [ ] Is there a data backfill requirement?

---

## 📊 SECTION 3: KUSTO (AZURE DATA EXPLORER)

### Q8: Where is Kusto located?
- [ ] Azure Data Explorer cluster URL: `______________`
- [ ] Database name: `______________`
- [ ] Do I need access? How do I get it?

### Q9: Where is the `getAllVppSitesV2()` function?
- [ ] Is it stored in the Kusto database directly?
- [ ] OR is it in a code repository as a `.kql` file?
- [ ] If in repo, what is the file path?

### Q10: **CRITICAL: Which function should I modify?**
- [ ] `getAllVppSitesV2()` ← Modify this one?
- [ ] `getAllVppSites()` ← Or this one?
- [ ] Both?
- [ ] What's the difference between them?

### Q11: How do I update Kusto functions?
- [ ] Do I edit the `.kql` file in the repo and deploy?
- [ ] Do I run the query directly in Azure Data Explorer?
- [ ] Is there a deployment pipeline/process?

### Q12: How does data flow from Postgres to Kusto?
- [ ] Is there an automated sync/ETL process?
- [ ] How often does it run? (real-time, hourly, daily?)
- [ ] Do I need to update the sync configuration?
- [ ] Where is the sync/ETL code located?

---

## 🔄 SECTION 4: DEPLOYMENT & PIPELINE

### Q13: What does "pipeline" mean in this context?

**Data Pipeline (ETL/Data Flow):**
- [ ] Is there an Azure Data Factory pipeline?
- [ ] Is there an Apache Airflow DAG?
- [ ] Is there a custom sync service?
- [ ] Where is the pipeline configuration?

**CI/CD Pipeline (Deployment):**
- [ ] Is there an Azure DevOps pipeline for deployments?
- [ ] Is there a GitHub Actions workflow?
- [ ] Do I need to update the pipeline configuration?

### Q14: Deployment process
- [ ] How do database changes get deployed?
  - [ ] Automatically via CI/CD
  - [ ] Manually by running scripts
  - [ ] Through a deployment tool
- [ ] What environments exist?
  - [ ] Dev
  - [ ] Staging/QA
  - [ ] Production
- [ ] In what order should I deploy? (Dev → Staging → Prod?)

### Q15: Testing requirements
- [ ] Are there unit tests I need to update?
- [ ] Are there integration tests?
- [ ] How do I run tests locally?
- [ ] Do I need to write new tests for these columns?

---

## 🛠️ SECTION 5: DEVELOPMENT WORKFLOW

### Q16: What is the development workflow?
1. [ ] Create a feature branch from: `______________`
2. [ ] Make changes (migration scripts, code, Kusto functions)
3. [ ] Test in: `______________` environment
4. [ ] Create Pull Request / Merge Request
5. [ ] Get approval from: `______________`
6. [ ] Merge to: `______________` branch
7. [ ] Deploy to: `______________` environment

### Q17: Code review process
- [ ] Who should review my PR?
- [ ] Are there specific reviewers I should tag?
- [ ] What's the typical review turnaround time?

### Q18: Rollback plan
- [ ] If something goes wrong, how do we rollback?
- [ ] Are there rollback migration scripts?
- [ ] Who has authority to rollback in production?

---

## 📝 SECTION 6: DOCUMENTATION & EXAMPLES

### Q19: Can you show me a similar past change?
- [ ] Is there a previous PR/commit where columns were added?
- [ ] Can you walk me through an example?

### Q20: Documentation
- [ ] Is there a developer wiki or documentation?
- [ ] Are there architecture diagrams?
- [ ] Is there a data dictionary or schema documentation?

---

## 👥 SECTION 7: CONTACTS & SUPPORT

### Q21: Who can I ask for help?
- [ ] Database/Schema questions: `______________`
- [ ] Kusto questions: `______________`
- [ ] Pipeline/ETL questions: `______________`
- [ ] Code review: `______________`
- [ ] Deployment/DevOps: `______________`

### Q22: Communication channels
- [ ] What Slack/Teams channel should I use for questions?
- [ ] Are there daily standups I should join?

---

## ⏱️ SECTION 8: TIMELINE & EXPECTATIONS

### Q23: Timeline
- [ ] When is this expected to be completed?
- [ ] Are there any dependencies or blockers?
- [ ] Is this blocking other work?

### Q24: Scope confirmation
- [ ] Is the scope ONLY adding these 4 columns?
- [ ] Are there any other related changes needed?
- [ ] Should I update any API endpoints or application code?

---

## 🎯 SUMMARY CHECKLIST

After the onboarding call, I should have:
- [ ] Repository access
- [ ] Database access (dev environment at minimum)
- [ ] Kusto access
- [ ] Clear understanding of: Edit code vs. Run SQL directly
- [ ] Data types for all 4 new columns
- [ ] Example of a similar past change
- [ ] Contact person for questions

---

## 📋 NOTES SECTION

**Use this space during the call to write down important details:**

### Repository Info:
```
URL: 
Branch: 
Path to migrations: 
```

### Database Info:
```
Connection string (dev): 
Tool to use: 
Migration approach: 
```

### Kusto Info:
```
Cluster URL: 
Database: 
Function to modify: 
```

### Data Types:
```
auto_enrollment: 
utility_meter_id: 
utility_meter_serial_number: 
site_owner_authorization: 
```

### Next Steps After Call:
1. 
2. 
3. 

---

**Good luck with your onboarding! 🚀**




