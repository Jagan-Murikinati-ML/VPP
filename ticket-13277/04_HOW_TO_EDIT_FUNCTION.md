# Step 4: How to Edit KQL Functions in Fabric

## Important: Functions are NOT in GitHub!

KQL functions are **stored in the database**, not in files or repositories.

You edit them directly in **Fabric Portal** using KQL commands.

---

## Process Overview:

```
1. Open Fabric Portal
2. Go to KQL Database
3. Run: .show function getAllVppSitesByUserId
4. Copy the function body
5. Modify it (add your 2 lines)
6. Wrap in .create-or-alter function
7. Run the modified function
8. Function is updated!
```

---

## Detailed Steps:

### Step 1: Open Fabric Portal
- Go to https://app.fabric.microsoft.com
- Navigate to your Eventhouse workspace
- Open the KQL Database

**Ask your team:** "Which workspace and database should I use for DEV testing?"

---

### Step 2: Open Query Window
- Click on the KQL Database
- Click "Query" or "New Query" button
- This opens the KQL Query Editor

---

### Step 3: View Current Function
Type this in the query window:
```kql
.show function getAllVppSitesByUserId
```
Click **Run**

This shows the current function code in a table.

---

### Step 4: Copy the Function Body
- From the result, find the "Body" column
- Copy the entire function code from that column
- Paste it into a text editor (Notepad, VS Code, etc.)

---

### Step 5: Make Your Changes
In the text editor:
1. Find the `project` clause (around line 98)
2. Add LINE 1 (accountNumber extraction)
3. Find the `pack()` function (around line 107)
4. Add LINE 2 (external_reference_id)
5. Save a backup copy before making changes!

---

### Step 6: Wrap in .create-or-alter function
Add this wrapper around your modified function:

```kql
.create-or-alter function getAllVppSitesByUserId(inputUserId:string="", page:int=0, page_size:int=10) {
    // PASTE YOUR MODIFIED FUNCTION BODY HERE
}
```

---

### Step 7: Deploy the Function
- Copy the entire `.create-or-alter function` command
- Paste it into the KQL Query Editor in Fabric
- Click **Run**
- Wait for "Command completed successfully" message

---

### Step 8: Test the Function
Run this to test:
```kql
getAllVppSitesByUserId('test-user-id', 0, 5)
```

Check if `external_reference_id` appears in the output!

---

## Important Notes:

### ⚠️ Before You Edit:
1. **Ask your team** which environment to use (DEV/QA/PROD)
2. **Save a backup** of the original function
3. **Get approval** from your team lead if modifying PROD

### ✅ Best Practices:
- Always test in DEV first
- Document your changes
- Add comments in the code: `// Added for Ticket #13277`

### 🔄 If You Make a Mistake:
- You can run `.create-or-alter function` again with the old code
- That's why you save a backup!

---

## Example Workflow:

**In Fabric Query Editor:**

1. Get current function:
```kql
.show function getAllVppSitesByUserId
```

2. Copy body → Modify in text editor → Paste back:
```kql
.create-or-alter function getAllVppSitesByUserId(inputUserId:string="", page:int=0, page_size:int=10) {
    // ... entire modified function body ...
}
```

3. Test:
```kql
getAllVppSitesByUserId('81ab4c51-a8d9-ef11-8eea-00224809f11c', 0, 5)
```

---

**Next:** Move to `05_COMPLETE_MODIFIED_FUNCTION.md` to see the full code with changes

