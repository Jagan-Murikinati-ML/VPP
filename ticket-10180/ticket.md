MWh Exports = Energy Delivered” widget  returning an empty array

1) Log in to VPP application. 
2) Reach the program list screen 
3) Open program dashboard for a program = "DSGS"
4) Look for MWh Exports widget. 

Actual : 
In the production environment, for the program DSGS, the total charge event value is:

2,272.16 kWh

converting to MWh= 2.272 MWh 

Excepted : 2.272 MWh expected to be visible in the widget .




Ayub Shirgaonkar
commented Thursday


@Jagan.Murikinati @Naveen Siddalingaswamy – Jagan, could you please check this bug? It’s related to the Fabric function which was working previously but has suddenly stopped.
Function: getVPPExportSummaryByProgram