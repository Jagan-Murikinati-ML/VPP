# Immediate Next Actions - Do These NOW

**Updated:** After conversations with Jim, Juan, Naveen  
**Status:** Waiting for clarifications, but can start exploring  

---

## 🚀 ACTION 1: Send Clarification Message (5 minutes)

### Where: ADO Ticket Comments
### Message Template:

```
Hi @Shaun Roach @Sanjeev Lakkaraju @cecilia.zhou @Ayub Shirgaonkar,

I've connected with Jim Avery (database access) and Juan Pablo (Kusto). I have DEV database access now and ready to proceed, but need a few clarifications:

1. DATA TYPES (CRITICAL):
   Jim asked: Is auto_enrollment a boolean? Please confirm data types for all 4 columns:
   - auto_enrollment: Boolean? VARCHAR? Nullable?
   - utility_meter_id: VARCHAR(255)? INT? Nullable?
   - utility_meter_serial_number: VARCHAR(255)? Nullable?
   - site_owner_authorization: Boolean? VARCHAR? Nullable?

2. KUSTO FUNCTIONS & REPOSITORY:
   - Original ticket mentions getAllVppSitesV2()
   - Juan showed me es-eventhouse repo with getAllVppRegisteredSitesByUserId and getVppSiteListView
   - @Shaun Roach - Which function(s) should I actually modify?
   - Is es-eventhouse the correct repo, or is there a different VPP-specific repo?

3. POSTGRES MIGRATIONS:
   - Is there a GitHub repo for Postgres migration scripts?
   - If not, should I attach SQL change scripts directly to this ticket?

4. DATA PIPELINES:
   @Shaun Roach mentioned updating silverProgramInfo and silverProgramSiteInfo pipelines.
   - Where are these pipelines located? (Azure Data Factory? Repo?)
   - Do I need to update them, or will someone else handle this?

5. DEPLOYMENT PROCESS:
   - Jim has DEV database access only
   - For QA/Prod deployment, should I provide SQL scripts for DevOps team?

Current Status:
✅ DEV database access (from Jim)
✅ Can explore es-eventhouse repo (from Juan)
⏳ Need above clarifications to proceed with implementation

Please advise. Thanks!
```

**DO THIS NOW!** ⬆️

---

## 🔐 ACTION 2: Get Database Password from Jim (2 minutes)

### Where: Slack DM to Jim Avery

### Message:

```
Hi Jim,

Thanks for the database info! Could you please share the password for:
- Host: assetregistry-us-es-dev-postgre.postgres.database.azure.com
- User: esadmin

I'll test the connection and start exploring the tables.

Thanks!
```

---

## 💻 ACTION 3: Clone the Kusto Repository (5 minutes)

### Open PowerShell and run:

```powershell
# Navigate to a workspace folder
cd C:\Users\murikinati_j\Desktop\

# Clone the repo
git clone https://github.com/qcells-hqct/es-eventhouse.git

# Navigate into it
cd es-eventhouse

# Checkout develop branch
git checkout develop

# Open in VS Code
code .
```

---

## 🔍 ACTION 4: Explore the Kusto Functions (15 minutes)

### Once repo is cloned:

1. **Navigate to the functions folder:**
   ```
   gen3-api/database/eventhouse/data/functions/API Functions/
   ```

2. **Open these files:**
   - `getAllVppRegisteredSitesByUserId.kql`
   - `getVppSiteListView.kql`

3. **Search for other VPP functions:**
   - Press `Ctrl+Shift+F` in VS Code
   - Search for: `getAllVppSitesV2`
   - Search for: `getAllVppSites`
   - Search for: `VppSite`

4. **Understand the structure:**
   - What tables do they query?
   - What columns do they return?
   - How are they joined?

5. **Share findings with me:**
   - Tell me what you found
   - I'll help you understand which to modify

---

## 🗄️ ACTION 5: Install Database Tool (10 minutes)

### Option A: DBeaver (Recommended)

1. Download: https://dbeaver.io/download/
2. Install it
3. Create new connection:
   - Database: PostgreSQL
   - Host: `assetregistry-us-es-dev-postgre.postgres.database.azure.com`
   - Port: `5432`
   - Database: `assetregistry` (or ask Jim)
   - User: `esadmin`
   - Password: (from Jim)

### Option B: Azure Data Studio

1. Download: https://aka.ms/azuredatastudio
2. Install PostgreSQL extension
3. Connect using Jim's credentials

### Option C: pgAdmin

1. Download: https://www.pgadmin.org/download/
2. Install and connect

---

## 🔍 ACTION 6: Explore Database Tables (Once Connected)

### Tables to find:

1. `asset.tb_bas_program_info`
   - Look at current columns
   - Look at data types used
   - See if there are similar boolean/varchar columns

2. `asset.tb_bas_site`
   - Look at current columns
   - See what data types are used for IDs and serial numbers

3. `asset.tb_opr_program_site_info`
   - Look at current columns
   - Check for similar authorization/boolean fields

### What to note:

- Current column naming conventions
- Data types they typically use
- Nullable vs NOT NULL patterns
- Any indexes or constraints

---

## 📊 ACTION 7: Create a Summary Document (While Waiting)

### Create a file with your findings:

```markdown
# Database Exploration Summary

## Tables Found:

### asset.tb_bas_program_info
Current columns:
- [list them]

Suggested data type for auto_enrollment: [based on similar columns]

### asset.tb_bas_site
Current columns:
- [list them]

Suggested data types:
- utility_meter_id: [based on similar ID columns]
- utility_meter_serial_number: [based on similar serial columns]

### asset.tb_opr_program_site_info
Current columns:
- [list them]

Suggested data type for site_owner_authorization: [based on similar columns]
```

---

## ⏰ TIMELINE

### Today (Next 2 Hours):
- [ ] Send clarification message to ADO ticket
- [ ] Get password from Jim
- [ ] Clone es-eventhouse repo
- [ ] Explore Kusto functions
- [ ] Install database tool
- [ ] Connect to database
- [ ] Explore tables

### Tomorrow:
- [ ] Receive clarifications from team
- [ ] Write SQL migration scripts
- [ ] Update Kusto functions
- [ ] Test in DEV
- [ ] Submit for review

---

## 📝 CHECKLIST

**Before End of Day:**
- [ ] Clarification message sent to ADO ticket
- [ ] Database password received from Jim
- [ ] es-eventhouse repo cloned
- [ ] Database connection tested
- [ ] Tables explored and documented
- [ ] Kusto functions reviewed

**Waiting For:**
- [ ] Data types confirmation
- [ ] Which Kusto function(s) to modify
- [ ] Postgres repo location (or confirmation to use scripts)
- [ ] Pipeline update process

---

## 🎯 WHAT YOU CAN DO WITHOUT WAITING

### 1. Explore the Database
- Connect and look at tables
- Understand current schema
- Propose data types based on patterns

### 2. Explore Kusto Functions
- Find all VPP-related functions
- Understand their structure
- Identify which ones query the relevant tables

### 3. Draft SQL Scripts
- Write draft ALTER TABLE statements
- Use placeholder data types
- Update once confirmed

### 4. Draft Kusto Updates
- Identify where to add new columns
- Prepare the changes
- Wait for confirmation on which function

---

## 💬 KEEP ME UPDATED

### Share with me:

1. **After cloning repo:**
   - "I cloned the repo, here's what I found in the functions folder..."

2. **After connecting to database:**
   - "I connected to the database, here are the current table structures..."

3. **After getting responses:**
   - "They confirmed the data types are..."
   - "They said to modify these functions..."

### I'll help you:
- Understand the code structure
- Write the SQL migrations
- Update the Kusto functions
- Test everything

---

## 🆘 TROUBLESHOOTING

### Can't clone repo?
- Check GitHub access
- Ask Juan for permissions
- Try HTTPS vs SSH

### Can't connect to database?
- Verify password from Jim
- Check if VPN is needed
- Try different database tools

### No response to clarifications?
- Wait 24 hours
- Ping again
- Escalate to Naveen

---

## ✅ SUCCESS CRITERIA FOR TODAY

By end of day, you should have:
- ✅ Sent clarification message
- ✅ Database access working
- ✅ Kusto repo cloned and explored
- ✅ Understanding of current table structures
- ✅ Draft plan for changes

**You're doing great! Keep moving forward!** 🚀

---

**Next:** Start with ACTION 1 (send the message), then do the rest in parallel while waiting for responses!

