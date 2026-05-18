In the current design, the connectors pull the real-time telemetry from the OEM cloud, using the vendor provided APIs. The real-time telemetry falls short of the data quality required for settlement purposes. Gaps in data, duplicates and incorrect readings among others are some of the data quality issues. For settlement purposes, the data needs to adhere to SQMD standards.

The real-time telemetry data from the connectors are persisted in the silverCommDataSite table in Kusto (Microsoft Fabric). 

The proposal is to create a batch job, which runs nightly, and pulls the telemetry from the  silverCommDataSite table into the sqTelemetry (Settlement quality telemetry) table. Only the relevant metrics of interest for settlement are pulled into the sqTelemetry table. 

Data in the sqTelemetry table is also updated once every 2 weeks to account for corrections made to the telemetry by the OEMs and for filling gaps. Based on our current rate limits, we will be able to accommodate telemetry updates for only SolarEdge, Tesla, Enphase and Qcells. Solax does not have sufficient rate limits to perform these bi-weekly updates, unless we negotiate higher limits with Solax.  Rate limits are documented here 
OEM API Rate limits and backfill constraints
 

Once every 2 weeks, after the data update, the data in the sqTelemetry table goes through Validation, Estimation and Editing. 

 

Validation
The requirements for validation are documented here 
[VPP-6] Data Validation Rules: VEE Validation Checks Business Requirement
 

The sqTelemetry table goes through a series of validations which includes the following:

Gaps in data

Duplicates

Statistical outliers

Abnormality (ex: power readings greater than nameplate capacity)

Sum of Incremental data should equal to Cumulative data

Based on the validation, a data label is assigned to each metric as Valid, Suspect or Invalid.

 

Estimation and Editing
The validated data then goes through the process of estimation and editing. The requirements are documented here 
Data Estimation & Editing Procedures
 

 

Versioning
After the data is estimated and edited to confirm to the SQMD standards, it gets versioned. The latest version of the data is used for settlement. If the settlement data gets corrected for any reason, it’s versioned again. All the vintages of the settlement data are persisted.

 

Tasks


Nightly batch job @Jagan Mohan Reddy Murikinati @Sanjeev Lakkaraju 

Bi-weekly updates @Jagan Mohan Reddy Murikinati @Sanjeev Lakkaraju 

Data Validation @Sachin Ingale 

Data Estimation and Editing (TBD)