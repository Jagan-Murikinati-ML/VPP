OEM API Rate limits and backfill constraints



By Naveen Siddalingaswamy

1 min

8

Add a reaction
Translations
Translations
 

OEM

Rate Limit

Max duration for historical data query per site

No of API calls to fetch Site level data.

Current consumption for real-time telemetry.

No of sites that can be supported for backfill.

Solax

100/min API calls

1 day

1-2

 

Rate limit is an issue here for backfill, unless we can have the rate limits increased.

SEDG

For sites enrolled in Grid services, we use websockets.

So we have 300 calls / site /day available for backfill.

1 month

3

288 calls / site

We have 12 calls / site available for backfill. With 3 calls we can perform backfill for 30 days. With 6 calls we can perform backfill for 60 days.

TESLA

300/min API calls

20 days

1

1 call for all the sites in the monitoring group.

Rate limit should not be an issue here. We can potentially backfill 144,000 sites per day with the current rate limit.

ENPHASE

No Limit

N/A

N/A

 

Rate limit is not an issue here.

QCELLS

N/A

N/A

N/A

 

Rate limit is not an issue here.

 

Tesla

Calculation:

API limit: 300 calls/min

Data per call: 20 days per site

Needed per site: 60 days

Calls needed per site: ceil(60 / 20) = 3

    300 / 3 = 100 sites per minute

Per minute: 100 sites

Per hour: 6,000 sites

Per day: 144,000 sites

 

SolarEdge

Calculation:

Every 15 minutes = 96 pulls/day

3 API calls per pull

Total used per day = 96 × 3 = 288 calls

Available = 300 calls/site/day

Remaining:

300 - 288 = 12 calls per day