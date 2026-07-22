# VPP Project - Qcells Client Work

**Engineer:** Jagan Murikinati  
**Client:** Qcells  
**Project:** Virtual Power Plant (VPP) Platform  

---

## 📁 PROJECT STRUCTURE

### `ticket-12121/` - ✅ COMPLETED
**Ticket:** Extend Postgres Tables with Site Metadata  
**Status:** Completed and deployed to DEV  
**Date:** March 18-20, 2026  

**Summary:**
- Added 4 new columns to Postgres tables in `assetdb`
- Columns: `auto_enrollment`, `utility_meter_id`, `utility_meter_serial_number`, `site_owner_authorization`
- Successfully tested in DEV environment
- Migration script ready for QA/Prod deployment

**Key Files:**
- `postgres_migration_FINAL.sql` - Production-ready migration script
- `migration_results_FINAL.txt` - Verification results from DEV
- All analysis and planning documents

---

### `ticket-12654/` - 🔄 IN PROGRESS
**Ticket:** Bug - Total Energy & Site Count Mismatch in Past Events List  
**Status:** Initial analysis complete, awaiting team response  
**Date:** Started March 20, 2026  

**Summary:**
- Bug: Past Events List shows incorrect total energy and site count
- Issue: Numbers don't match site-level performance data
- Example Event: "Prg -20260318-85e2"
- Root Cause: TBD (investigating data source discrepancy)

**Key Files:**
- `ADO-12654.md` - Ticket description
- `TICKET_ANALYSIS.md` - Detailed analysis and hypotheses
- `MESSAGE_TO_TEAM.md` - Questions for Sanjeev & Juan
- `image-1.png`, `image-2.png`, `image-3.png` - Screenshots from ticket

**Next Steps:**
1. Send message to Sanjeev & Juan
2. Get code locations for both data sources
3. Compare queries and identify bug
4. Propose and test fix

---

## 🔑 KEY INFORMATION

### Database Access (DEV)
```
Host: assetregistry-us-es-dev-postgre.postgres.database.azure.com
Database: assetdb
User: esadmin
Password: es!adminQ123
```

### GitHub Repositories
```
Kusto Functions: https://github.com/qcells-hqct/es-eventhouse
Branch: develop
Path: gen3-api/database/eventhouse/data/functions/API Functions/
```

### Key Contacts
- **Jim Avery** - Database/Postgres expert
- **Juan Pablo Culebro** - Kusto functions expert
- **Sanjeev Lakkaraju** - Team lead
- **Naveen Siddalingaswamy** - Business/requirements
- **Shaun Roach** - Technical lead

---

## 📚 REFERENCE DOCUMENTS

### `vpp_document.md`
Comprehensive guide to VPP concepts:
- DERMS (Distributed Energy Resource Management System)
- Virtual Power Plants
- How energy flows in the grid
- Site-level performance metrics
- Data analytics in energy systems

**Use this to understand domain concepts when working on tickets.**

---

## 🚀 WORKFLOW

### For New Tickets:
1. Create folder: `ticket-{ADO-ID}/`
2. Add ticket description as `ADO-{ID}.md`
3. Create analysis document
4. Document questions and findings
5. Move all related files to ticket folder when complete

### For Database Changes:
1. Connect to DEV using WSL + psql
2. Test changes in DEV first
3. Create migration script with verification queries
4. Document results
5. Attach script to ADO ticket for QA/Prod deployment

### For Code Changes:
1. Clone relevant repo
2. Create feature branch
3. Make changes and test locally
4. Create PR with detailed description
5. Get review and merge

---

## 💡 LESSONS LEARNED

### Ticket #12121:
- ✅ Always verify database name (was `assetdb`, not `postgres`)
- ✅ Use schema-qualified names for ENUMs (`asset.site_authorization_status`)
- ✅ Test firewall access before starting work
- ✅ Stakeholder requirements can change mid-task (column moved to different table)
- ✅ Document all verification steps for audit trail

### Ticket #12654:
- 🔄 Always ask for code locations upfront
- 🔄 Understand data flow before proposing fixes
- 🔄 Use specific event IDs for testing

---

## 🎯 CURRENT STATUS

**Active Ticket:** ADO-12654 (Bug investigation)  
**Completed Tickets:** ADO-12121 (Postgres migration)  
**Next Action:** Send inquiry message to Sanjeev & Juan  

---

**Last Updated:** March 20, 2026

