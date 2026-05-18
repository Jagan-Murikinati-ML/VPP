heading:- Create Fabric Function to Fetch Site Telemetry Data for Program within Time Range (15-Min Interval)

description :- Develop a Fabric function to retrieve telemetry data for sites mapped to a program based on events generated within a specified time range.

The function should accept Program Name, Site List, Time Zone, Start Time, and End Time as input parameters and return telemetry data for each site at a 15-minute interval between the provided start and end time as per program time zone.

The returned data should include key metrics required for program-level analysis and reporting.

Input Parameters
Program Name
Site List
Start Time
End Time
Time Zone 


Output Fields
Site ID
Interval Start (UTC)
Interval End (UTC)
Site Load (kW)
PV Generation (kW)
Battery Power (kW)
Battery State of Charge (SoC %)

