parent-ticket-header:- Display External Reference ID in Resource Page (Enrollment Authorization off platform)

parent-ticket description:- 

As an authorized user, I should be able to view the External Reference ID for each site so that I can easily identify, search, and reconcile assets using the partner’s internal reference identifiers.

A new column “External Reference ID” shall be added to the Resources grid.
The column should be positioned next to the “Site Type” column.
The External Reference ID value should be displayed when available; if no value is received from the backend, a “-” should be shown.
The column must support - Search, Filter and Sort [consistent with other sortable columns in the grid (existing implementation)]
Assumption -
As discussed and agreed during the VPP working session on Mar 4, 2026, the Avigna team will proceed with the frontend implementation for this field. Since the backend API is not yet available, the field will initially display “-” as a placeholder value. Once the backend API is ready, the frontend will integrate with the API and the field will start displaying the actual data.

Backend Support - 
For each Asset (NOT Site):  Store value in external_reference_id. This stores the unit reference ID from the partner owning the device or managing the site-device relationship.
For existing residential assets onboarded for/by Enfin: Populate external_reference_id using APP-ID.
The frontend will fetch this value from backend API (Fabric / Asset API). 
Display it in the new column 'External Reference ID'  on the resource page 
Impact Analysis - 

External Reference ID value will be fetched from Backend API / Fabric.
Frontend will consume and display the data on the Resources grid for the External Reference ID column..

Mockup -
image (16).png

