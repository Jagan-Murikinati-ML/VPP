# Email to Naveen's Team - ADO-12654

---

Hi @Naveen @Sanjeev @Juan Pablo Culebro,

I've completed my analysis of **ADO-12654** (data discrepancy in VPP event reporting). I've identified the root causes and have some questions to help me propose the correct fix.

## Summary

**Bug:** Past Events List shows **2.3 kWh / 3 sites**, but Site-Level Performance shows **2.9 kWh / 4 sites** for event "Prg -20260318-85e2".

## What I Found

### Event Structure
The event consists of **3 child events:**
- **Event1** (03:20-03:35): charge strategy, 4 sites with commands
- **Event2** (03:52-03:55): charge strategy, 4 sites with commands  
- **Event3** (03:39-03:50): self consumption, 3 sites with commands

### Key Issues Discovered

**1. Data Source Mismatch:**
- The `getVPPDispatchSummary` function counts sites from `silver_dispatch_result_dto` (command-based)
- But calculates energy from `silverCommDataSite` (telemetry-based)
- Result: Sites that got commands but didn't perform are counted with 0 energy

**2. Site 400005226 - The "Ghost" Site:**
- Received `CHARGE_FROM_GRID_AND_SOLAR` commands in Event1 & Event2
- But dispatch window was 0 minutes (start time = end time: 03:21 to 03:21)
- Contributed 0 kWh but may be counted in site participation

**3. Event2 Data Missing:**
- `getVPPDispatchSummary("fdf0e836-...")` returns **NO DATA**
- But site-level performance shows Event2 HAS data (0.7 kWh charged)
- This could explain part of the energy gap

**4. Function Results:**
| Event | Energy (Net) | Sites |
|-------|--------------|-------|
| Event1 | 1.7 kWh | 4 |
| Event2 | NO DATA ❌ | ? |
| Event3 | -0.4 kWh | 3 |

---

## Questions I Need Answered

### 1. Event ID Mapping
**Which event ID(s) does the Past Events List query to get 2.3 kWh?**
- A parent event ID?
- All 3 child events aggregated?
- Just Event1?

### 2. Event2 Missing Data
**Why does the summary function return no data for Event2?**
- Event2 has performance data and commands sent
- Is there a data sync issue?

### 3. Site Counting Rule
**Should "Sites Dispatched" count:**
- A) Sites that received commands (4 sites) ← current behavior
- B) Sites that actually performed with telemetry (3 sites)

### 4. Strategy Filtering
**Should "self consumption" events (Event3) be included in total energy?**
- With Event3: 2.9 kWh
- Without Event3: 3.5 kWh

### 5. Code Location
**Where is the Past Events List API endpoint?**
- Which service/file?
- Does it call `getVPPDispatchSummary` or something else?

---

## What I Need

1. **Answers to the above questions** (or point me to who can answer them)
2. **Access to the Past Events API code** (repo + file path)
3. **Confirmation:** Is the Site-Level Performance data the source of truth?

---

## Next Steps

Once I get this info, I can:
✅ Pinpoint the exact bug  
✅ Propose the correct fix  
✅ Write tests  
✅ Submit PR for review

---

**All supporting data/queries are in:** `ticket-12654/FINAL_ANALYSIS_FOR_NAVEEN.md`

Let me know if you need any clarification or want me to investigate specific areas further!

Thanks,  
Jagan


