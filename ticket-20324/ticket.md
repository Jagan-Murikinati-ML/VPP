Program name is not displayed in the resources page for some sites


Function names:
getAllVppSitesByUserIdV2
new functions created in this story should not have this issue: User Story 20099: [Fabric] optimize performance for resources table endpoint


Update:- 

Root Cause: Investigated the issue and found that site IDs 100003610 and 400062473 are missing from GetLatestProgramSiteInfo (source: goldProgramSiteInfo). As a result, the API is returning an empty program_name for these sites.

