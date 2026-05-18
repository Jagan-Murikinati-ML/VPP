# Azure DevOps Ticket Analysis - Site Table Extension

**Ticket Assigned:** Sunday (Recent)  
**Status:** New Assignment from Cross-Team  
**Your Background:** Previously worked on Fabric, unfamiliar with this team's codebase

---

## 📋 TICKET SUMMARY

**Objective:** Extend Postgres and Kusto database schemas to include additional site metadata for VPP (Virtual Power Plant) sites.

---

## 🎯 WHAT NEEDS TO BE DONE

### 1. **Postgres Database Changes**

You need to add new columns to THREE existing tables:

#### Table 1: `asset.tb_bas_program_info` (Program-level attributes)
- **New Column:** `auto_enrollment` (likely BOOLEAN or VARCHAR)

#### Table 2: `asset.tb_bas_site` (Site-level attributes)
- **New Column:** `utility_meter_id` (likely VARCHAR/TEXT)
- **New Column:** `utility_meter_serial_number` (likely VARCHAR/TEXT)

#### Table 3: `asset.tb_opr_program_site_info` (Program-Site relationship attributes)
- **New Column:** `site_owner_authorization` (likely BOOLEAN or VARCHAR)

### 2. **Kusto (Azure Data Explorer) Changes**

- Modify the Kusto function `getAllVppSitesV2()` to include these new properties
- **Question in ticket:** Should they use `getAllVppSitesV2()` or `getAllVppSites()`?
  - This needs clarification from Shaun Roach

---

## 🔍 WHAT YOU NEED TO FIND OUT

### Critical Questions to Ask:

1. **Where is the actual codebase?**
   - Is there a GitHub/Azure DevOps repository with the database migration scripts?
   - Do they use a migration tool (Flyway, Liquibase, Entity Framework, etc.)?

2. **What is the deployment process?**
   - Do you write SQL migration scripts directly?
   - Is there an ORM (Object-Relational Mapping) that needs updating?
   - Are there code-first models that generate the database schema?

3. **Where are the Kusto functions located?**
   - Azure Data Explorer cluster name?
   - Database name?
   - Are Kusto functions stored in a repository or managed directly in Azure?

4. **Data types for new columns?**
   - What should be the exact data types for each new column?
   - Should any columns be nullable or have default values?
   - Are there any constraints (unique, foreign keys, etc.)?

5. **Testing requirements?**
   - Do you need to update existing tests?
   - Are there integration tests for the Kusto functions?

6. **Data migration?**
   - Are there existing rows in these tables?
   - Do existing rows need default values for new columns?

---

## 🏗️ LIKELY IMPLEMENTATION APPROACH

### Scenario A: SQL Migration Scripts (Most Common)

If they use migration scripts, you'll need to:

1. Create a new migration file (e.g., `V1.2.3__Add_Site_Metadata_Columns.sql`)
2. Write ALTER TABLE statements:

```sql
-- Migration script example
ALTER TABLE asset.tb_bas_program_info 
ADD COLUMN auto_enrollment BOOLEAN DEFAULT FALSE;

ALTER TABLE asset.tb_bas_site 
ADD COLUMN utility_meter_id VARCHAR(255),
ADD COLUMN utility_meter_serial_number VARCHAR(255);

ALTER TABLE asset.tb_opr_program_site_info 
ADD COLUMN site_owner_authorization BOOLEAN DEFAULT FALSE;
```

3. Update any ORM models/entities in the codebase
4. Update the Kusto function to query these new columns

### Scenario B: Code-First Approach

If they use Entity Framework or similar:

1. Update C# entity classes with new properties
2. Generate migration using EF tools
3. Apply migration to database
4. Update Kusto ingestion/sync logic

---

## 📊 KUSTO FUNCTION UPDATE

The `getAllVppSitesV2()` function likely looks something like this:

```kql
.create-or-alter function getAllVppSitesV2() {
    VppSites
    | join kind=inner ProgramInfo on ProgramId
    | join kind=inner ProgramSiteInfo on SiteId, ProgramId
    | project 
        SiteId,
        SiteName,
        ProgramId,
        ProgramName,
        // NEW FIELDS TO ADD:
        AutoEnrollment,
        UtilityMeterId,
        UtilityMeterSerialNumber,
        SiteOwnerAuthorization,
        // ... other existing fields
}
```

---

## 🚦 NEXT STEPS (Action Plan)

### Immediate Actions:

1. **Reply to the ticket** asking for:
   - Repository location (GitHub/Azure DevOps URL)
   - Database migration process documentation
   - Kusto cluster and database details
   - Data type specifications for new columns
   - Clarification on `getAllVppSitesV2()` vs `getAllVppSites()`

2. **Schedule a call** with:
   - Shaun Roach (mentioned in ticket)
   - Cecilia Zhou, Ayub Shirgaonkar, Krutika Jain, or Sanjeev Lakkaraju
   - Ask for a 15-minute onboarding/handoff session

3. **Request access** to:
   - Source code repository
   - Database (dev/staging environment)
   - Azure Data Explorer/Kusto cluster
   - Any relevant documentation

### Once You Have Access:

4. **Explore the codebase**:
   - Find existing migration scripts
   - Locate the Kusto function definitions
   - Review similar past changes

5. **Create a development plan**:
   - Write migration scripts
   - Update application code (if needed)
   - Update Kusto functions
   - Test in dev environment

6. **Get code review** before deploying to production

---

## 💡 SENIOR PM PERSPECTIVE

### Why This Ticket Exists:

This is a **data model extension** to support new VPP program features. The new fields suggest:

- **`auto_enrollment`**: Programs can now auto-enroll sites (vs manual enrollment)
- **`utility_meter_id` & `utility_meter_serial_number`**: Better tracking of physical utility meters at sites
- **`site_owner_authorization`**: Compliance/permission tracking for site participation

### Business Context:

VPP programs aggregate distributed energy resources (solar + batteries). These new fields likely support:
- Streamlined onboarding (auto-enrollment)
- Utility integration (meter tracking)
- Legal compliance (owner authorization)

### Your Position:

- You're new to this team's codebase
- This is a straightforward schema extension (low risk)
- Perfect opportunity to learn their development workflow
- Don't hesitate to ask questions - you were just assigned this

---

## ⚠️ RED FLAGS TO WATCH FOR

- **No documentation** on deployment process
- **Direct production database access** (should use migrations)
- **No testing environment** available
- **Unclear data type requirements**
- **No rollback plan** for migrations

---

## 📞 COMMUNICATION TEMPLATE

**Sample message to send:**

> Hi team,
>
> I've been assigned this ticket to extend the Site tables in Postgres and Kusto. Since I'm new to this codebase (coming from Fabric), I need some context to get started:
>
> 1. Where is the source code repository for the database migrations?
> 2. What's the process for making schema changes (migration tool, manual SQL, etc.)?
> 3. Where can I find the Kusto function `getAllVppSitesV2()`?
> 4. What are the exact data types for the new columns?
> 5. Is there a dev/staging environment I can use for testing?
>
> @Shaun Roach - The ticket mentions choosing between `getAllVppSitesV2()` and `getAllVppSites()`. Which should I modify?
>
> Happy to jump on a quick call if that's easier. Thanks!

---

**Document Created:** For reference and planning  
**Next Update:** After receiving codebase access and clarifications

