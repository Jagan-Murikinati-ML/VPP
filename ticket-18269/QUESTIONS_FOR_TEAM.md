# Questions for Naveen & Sanjeev - Ticket 18269

## Quick Summary
Analyzed the Asset Onboarding report data (33,510 sites). Need clarification on a few points before proceeding.

---

## Questions:

### 1. Type 0 vs Type 1 - What's the difference?

The ticket mentions "type 0 asset" and "type 1 asset" but I don't see these fields in the current data.

**Is it:**
- Type 0 = Solar inverter only (no battery)
- Type 1 = Battery/Hybrid inverter

**Or something else?**

---

### 2. Battery Flag - How to determine?

We need to add a battery flag. How should we identify if a site has batteries?

**Option A:** Use `productInfo_prodSubType` field?
- HybridInverter = has battery
- BatteryInverter = has battery
- NULL/other = no battery

**Option B:** Use `wMaxRtg` field (battery capacity)?
- wMaxRtg > 0 = has battery
- wMaxRtg = NULL/0 = no battery

**Option C:** Some other logic?

**Note:** 36% of sites have NULL product info - should these show "No Battery" or "Unknown"?

---

### 3. Type 1 Asset - What oem_name and oem_siteId?

For Type 1 assets, what values should we show?

**Example site:**
- site_id: 400061892
- Current oem_name: Tesla
- Current oem_siteId: e324135f-d738-4591-bf03-b84bb6b9ac10

**For Type 1, should we show:**
- Same oem_name (Tesla) or battery manufacturer name?
- Same oem_siteId or a different battery component ID?
- Is there a separate field in the source data for battery OEM info?

---

### 4. Current Report - Data Source?

**What is the current report pulling from?**
- Which table/function?
- Is there already a Type 0/Type 1 distinction in the source?
- Can you share the current query or data model?

This will help me understand what fields are available.

---

## Data Summary

**Current data exported:**
- 33,510 sites total
- OEMs: Qcells (40%), SolarEdge (31%), Tesla (18%), Enphase (11%)
- 17,612 have Inverter data
- 17,543 marked as HybridInverter
- 11,994 sites (36%) have NULL product type

Ready to proceed once these are clarified!

Thanks,
Jagan
