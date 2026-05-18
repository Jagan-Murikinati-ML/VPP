Create the table sqTelemetry in Kusto in the eventHouseVPP database.

Table Schema for sqTelemetry

siteId StringBuffer
assetId StringBuffer
oem StringBuffer
sourceTimestamp DateTime

battery_200_DailyWhExp R64
battery_200_DailyWhImp R64
battery_200_IncWhExp R64
battery_200_IncWhImp R64
battery_200_TotWhExp R64
battery_200_TotWhImp R64
battery_200_W R64
battery_713_SoC R64
battery_713_SoH R64
grid_200_DailyWhExp R64
grid_200_DailyWhImp R64
grid_200_IncWhExp R64
grid_200_IncWhImp R64
grid_200_TotWhExp R64
grid_200_TotWhImp R64
grid_200_W R64
load_200_IncWhExp R64
load_200_IncWhImp R64
load_200_TotWhExp R64
load_200_TotWhImp R64
load_200_W R64
pv_200_DailyWhExp R64
pv_200_IncWhExp R64
pv_200_IncWhImp R64
pv_200_TotWhExp R64
pv_200_TotWhImp R64
pv_200_W R64

For each of the metric above, add a "data label" field. For example, for metric battery_200_DailyWhExp, add a corresponding data label field battery_200_DailyWhExp_dl. The data label field shall be a StringBuffer with potential values (VALID, SUSPECT or INVALID)

SAMPLE DATA

Copy 1 day's worth of data (April 1) from the silverCommDataSite table to the sqTelemetry table.
