header:- User Story 10357: [Kusto] Resources list - new Azure Function to get paginated results from  Azure Data Explorer (Kusto) with support for filtering, sorting, and global search


description:- Currently, getAllVppSitesByUserId function exist, it supports `page_size`, `page` and responds with `total_count` and `data`.

We need to create a separate function so that UI can use server-side data model for performance optimization.

This pattern will be reused for other Functions, so it should be generic



