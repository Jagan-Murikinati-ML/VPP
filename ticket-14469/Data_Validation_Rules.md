Heading:- VPP-6 Data Validation Rules: VEE Validation Checks Business Requirement


[VPP-6] Data Validation Rules: VEE Validation Checks Business Requirement


NEW

Team Members

Program: @Alexandra Clark @Dongmin Son 

Product: @Cecilia Zhou

Solution Engineering: @Naveen Siddalingaswamy @Sanjeev Lakkaraju 

Operations: @Shuai Zhang

Document Name

Data Validation Business Requirements based on SQMD guidelines

References

 Direct Access Standards for Metering and Meter Data (DASMMD)

https://growingenergylabs.atlassian.net/wiki/x/PABylgIRequest access 

Applicable Systems

Solar inverter telemetry platforms

Battery sub-meter telemetry platforms

All OEM pipeline data

Expansion of this BRD

Historical Data Quality Examples outlining how these data validation issues could be preventable/detectable by following procedures below: 
Historical Data Quality Issues & Validation Control Mapping  

An expansion on data estimation rules + procedures: 
Data Estimation & Editing Procedures
  

Background & Purpose
Accurate, settlement-quality telemetry is foundational to Qcells’ participation in grid services programs, incentive programs, and performance-based reporting.

To ensure consistent data integrity, auditability, and reuse across programs, Qcells applies standardized data validation rules aligned with CPUC Settlement Quality Meter Data (SQMD) principles, which represent the prevailing metering and data quality standard for all of the US.

This BRD defines the business requirements for data validation only. Separate standards govern estimation and editing.

2. Scope
In Scope for Data Validation:
Interval-based solar production telemetry

Interval-based battery operational telemetry

Data used for:

Grid services programs

Settlement and incentive calculations

Performance analytics and forecasting

3. Guiding Standards
The data validation rules defined in this BRD are based on:

CPUC Settlement Quality Metering Data (SQMD) principles

DASMM validation practices

IOU-accepted data quality standards

(As listed above in References)

4. Success Criteria:
Data Validation Goals

Related Data Validation Check

All data is attributable to a known asset and site

Channel mapping, Meter Identity

All intervals are temporally accurate and complete

Interval Completeness, Time Integrity

All values are physically and statistically plausible

Spike Detection, High/Low Usage

All validation outcomes are traceable and auditable

Sum Check

 

5. Data Inputs
Data Type

Description

Solar Telemetry

Inverter-level production data

Battery Telemetry

Sub-metered charge/discharge data/SoC

Grid Import/Export Data

Received from OEM APIs

Consumption Data

Calculated field from OEM/Qcells data

Enrollment Metadata

Asset ID, site ID, capacity, etc

Time Reference

Timezone-aware system time

6. Required Validation Checks (Summary)
Validation Check

Technical Summary

Minimally Acceptable Method 

Estimated Difficulty to Implement

Interval Completeness

Verify presence of all expected 15-minute intervals (96 per day, DST-adjusted)

Perform a quick check to check that are 96 intervals per day per site ID. Flag if not equal to 96.

Easy

Sum Check

Verify internal consistency across channels and scaling factors

Compare interval-summed energy with expected total energy. 

Easy

High / Low Usage

Compare interval values against historical distributions

Excel check: compare against system nameplate or historical max/min using

TBD

Spike Detection

Identify single-interval deviations exceeding statistically reasonable bounds

If higher output than nameplate capacity, flag as suspect

Easy

Channel Mapping

Ensures telemetry channels are currently mapped to physical power flows (charge vs. charge, import vs. export)

Cross-check telemetry channels 

TBD

Time Integrity

Validate interval timestamps align correctly within event windows + temporal reporting boundaries

Sort intervals by timestamps and confirm 15-minute increments using =A2-A1 check. Should equal 00:15. Flag if intervals deviate from 15.

Medium

Meter Identity

Confirm meter/service account mapping has not changed

Compare telemetry meter ID/device ID and site ID against enrollment list. Use vlookup/xlookup.

Easy

7. Validation Rules (Detailed Requirements)
7.1 Interval Completeness Validation
Rule Objective

Rule Definition

Ensure all expected settlement or reporting intervals are present and accounted for.

For each asset and calendar day, the system shall verify the presence of all expected intervals based on:

Configured interval length

Daylight Saving Time adjustments

Expected interval counts must be dynamically calculated and not assumed to be constant.

Validation Criteria

Failure Conditions

All intervals are present for the applicable day type

Missing intervals not attributable to DST

Intervals aligned to the configured time grid

Duplicate intervals without unique temporal identifiers

Duplicate or missing intervals are explicitly identified

Misaligned interval boundaries

Failure Scenario Examples:

A daily telemetry set contains fewer than the expected number of 15-minute intervals after accounting for Daylight Saving Time adjustments.

One missing interval is silently ignored, causing daily energy totals to understate actual production or dispatch performance.

7.2 Sum and Internal Consistency Validation
Rule Objective

Rule Definition

Ensure mathematical consistency across reported values, channels, and units.

Reported power, energy, and net values must reconcile according to physical and mathematical relationships.

Validation Criteria

Failure Conditions

Energy equals power multiplied by interval duration

kWh values inconsistent with kW and interval length

Net values equal the sum of component channels

Net totals not reconcilable with components

Scaling factors and unit conversions are consistent

Scaling or unit mismatches

Failure Scenario Examples:

Reported interval energy does not equal reported power multiplied by the interval duration.

Scaling errors cause aggregated kWh values to diverge from summed kW intervals, leading to incorrect reporting and settlement disputes.

7.3 High / Low Usage Validation
Rule Objective

Rule Definition

Detect sustained values that are statistically or physically implausible

Intervals shall be evaluated against:

Asset nameplate and operational constraints

Historical distributions for the same asset and time-of-day

This rule targets prolonged anomalies rather than isolated spikes.

Validation Criteria

Failure Conditions

Output remains within physical limits

Prolonged output exceeding capacity constraints

Sustained behavior aligns with historical patterns

Extended flatlining or constant values indicative of sensor failure

 

Sustained deviations outside historical bounds

Failure Scenario Examples:

Sustained interval values remain within absolute capacity limits but fall outside historical distributions for the same asset and time-of-day.

A sensor becomes stuck at a constant output level, masking true operational behavior and overstating performance over time.

7.4 Spike Detection Validation
Rule Objective

Rule Definition

Identify isolated interval values that are not representative of real system behavior

Single-interval deviations shall be evaluated relative to:

Adjacent interval values

Statistically derived bounds based on historical behavior

Asset-specific ramp-rate and capacity constraints

Spikes are defined as abrupt, non-sustained deviations that immediately return to baseline behavior.

Validation Criteria

Failure Conditions

Interval-to-interval changes fall within plausible ramp limits

Single-interval excursions significantly exceeding expected variability

Values remain within statistically reasonable deviation thresholds

Output changes are inconsistent with known asset response characteristics

Failure Scenario Examples:

A single 15-minute interval reports power output that exceeds the asset’s historical statistical bounds while adjacent intervals remain within normal operating ranges.

A transient telemetry glitch produces one extreme interval value that inflates aggregated production totals if it is not flagged and excluded.

7.5 Channel Mapping Validation
Rule Objective

Rule Definition

Ensure that all reported power and energy values are associated with the correct physical flow and channel definition.

Each telemetry channel must map unambiguously to a defined physical meaning:

Solar: production/export channels represent the generated power

Battery: charge and discharge channels represent distinct operational states

Net power calculations must use consistent sign conventions and channel-aggregation logic.

Validation Criteria

Failure Conditions

Channel definitions match enrollment and configuration records

Inverted sign conventions 

Charge, discharge, import, and export are not inverted or co-mingled

Charge data reported as discharge (or vice versa)

Net values reconcile correctly to component channels

Export/import channels swapped or netted incorrectly 

Failure Scenario Examples:

A battery inverter reports discharge power on a charge-designated telemetry channel due to incorrect channel configuration, resulting in an inverted net power sign.

Battery discharge is recorded as charging because charge and discharge channels are swapped, causing downstream systems to treat real output as non-performance.

7.6 Time Integrity Validation
Rule Objective

Rule Definition

Ensure interval timestamps accurately reflect real elapsed time and remain aligned with system time references.


Telemetry timestamps shall be validated against a trusted time reference to detect excessive clock drift.

Validation Criteria

Failure Conditions

Timestamps are timezone-aware and include UTC offset

Drift exceeding the accepted tolerance thresholds (to be defined)

Clock drift remains within the to be defined tolerance

Intervals shifted outside expected temporal windows

Temporal ordering of intervals is consistent

Inconsistent or unstable clock behavior

Failure Scenario Examples:

Interval timestamps drift from system time by more than the accepted tolerance, resulting in misalignment with defined temporal boundaries.

Valid discharge occurs during an event window but is timestamped earlier due to device clock drift, leading to disallowed or misattributed performance.

7.7 Meter Identity Validation
Rule Objective

Rule Definition

Ensure telemetry is attributed to the correct physical asset and service location

Each interval must be associated with:

A valid site or service account (definition may be specificied by Ops/Dev team)

Validation Criteria

Failure Conditions

Device identifiers match enrollment records

Unknown or mismatched device identifiers

Telemetry timestamps fall within authorized operational windows

Conflicting device-to-site mappings

No unauthorized device substitutions occur

 

Failure Scenario Examples:

Telemetry is received from a device identifier that does not match the enrolled asset mapped to the service account.

A device replacement occurs without updating enrollment records, causing data to be attributed to the wrong asset.

8. Validation Outcomes Requirements:
Each interval should be assigned a validation status indicating:  

Valid (eligible for downstream use)  

Suspect (requires estimation or review)  

Invalid (excluded from use)

 

Notes on Auditability: 
The validation framework must support:

Interval-level traceability

Reproducibility of validation outcomes

Historical retention of validation flags and reasons

Sampling-based audits by internal or external parties

This is the standard required for nearly all VPP programs.

9. Timeline & Milestones
Milestone

Date

 

Data Validation methods are actively in place

May 1, 2025

 

10. Stakeholders
Team

Responsibility

Contact

Team

Responsibility

Contact

G&ES Dev

Implementing these validation techniques

@Naveen Siddalingaswamy@Sanjeev Lakkaraju 

G&ES Program

BRD

Process Examples & Clarifications

@Alexandra Clark @Dongmin Son 

 

G&ES Product

Product Delivery

@Cecilia Zhou

 

G&ES Ops

Added improvements/notes on what will work best for Dev team

@Shuai Zhang

@Kaifeng Xu