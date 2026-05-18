# Step 1: Understanding the Ticket

## Ticket #13277
**Task:** Add External Reference ID to the Fabric function `getAllVppSitesByUserId`

---

## What Does This Mean?

### Parent Ticket Context:
- Frontend team is adding a new column "External Reference ID" in Resources page
- They need backend to send this data in API response
- Users want to see external reference IDs to identify and reconcile assets

### Your Task:
- Modify the KQL function `getAllVppSitesByUserId` 
- Add a new field called `external_reference_id` to the JSON response
- This field should show the account number from asset registration info

---

## Key Information from Naveen:

**External Reference ID = Account Number**

Example from asset data:
```json
"assetRegistrationInfo": {
    "accountNumber": "APPTPO-2501513034"
}
```

This `accountNumber` is what we need to add to the function output.

---

## What You're Doing:
1. Understanding the ticket ✅ (You are here)
2. Understanding the function (Next step)
3. Implementing the code change
4. Testing the change

---

## Requirements:
- When `accountNumber` exists → Show the value (e.g., "APPTPO-2501513034")
- When `accountNumber` doesn't exist → Show "-"
- Field name in response: `external_reference_id`

---

**Next:** Move to `02_UNDERSTANDING_FUNCTION.md`

