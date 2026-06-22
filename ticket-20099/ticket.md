Currently, it takes 3-4 seconds on average to load a single page of 10 records. While the first-page load time has improved significantly and we no longer display outdated cached telemetry data, a 3-4 second delay is still very noticeable. Modern applications should load in under a second.

We should create 2 new endpoints to improve performance:
lighter version of existing getAllVppSitesByUserIdV2. It should work the same but include only:
site ID
site name
external reference ID
state 
program name
Move all the rest of the fields into 2nd function. I.e. so that we can query by IDs to patch already loaded data

It will let UI to load page by page much faster, the rest of the data will be fetched asynchronously




