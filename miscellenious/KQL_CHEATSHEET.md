# KQL Quick Reference Cheat Sheet

**Companion to:** KQL_LEARNING_GUIDE.md  
**Purpose:** Quick lookup for SQL → KQL conversions

---

## 🔥 **Most Common Operations**

| Operation | SQL | KQL |
|-----------|-----|-----|
| **Select columns** | `SELECT col1, col2 FROM table` | `table \| project col1, col2` |
| **Select all** | `SELECT * FROM table` | `table` |
| **Filter** | `WHERE age > 25` | `\| where age > 25` |
| **Sort** | `ORDER BY col DESC` | `\| order by col desc` |
| **Limit rows** | `LIMIT 10` / `TOP 10` | `\| take 10` |
| **Count all** | `SELECT COUNT(*) FROM table` | `table \| count` |
| **Count distinct** | `COUNT(DISTINCT col)` | `dcount(col)` |
| **Group by** | `GROUP BY dept` | `summarize ... by dept` |
| **Equality** | `col = 'value'` | `col == 'value'` |
| **Not equal** | `col != 'value'` | `col != 'value'` |
| **In list** | `IN ('A', 'B')` | `in ('A', 'B')` |
| **Pattern match** | `LIKE '%text%'` | `contains 'text'` |
| **Yesterday** | `DATEADD(day, -1, GETDATE())` | `ago(1d)` |
| **Add column** | `SELECT *, col*2 AS new FROM t` | `t \| extend new = col*2` |

---

## 📊 **Aggregations**

```kql
// Count by group
table
| summarize count() by department

// Multiple aggregations
table
| summarize 
    total_count = count(),
    avg_salary = avg(salary),
    max_salary = max(salary),
    min_salary = min(salary)
    by department

// Filter after aggregation (HAVING)
table
| summarize avg_sal = avg(salary) by department
| where avg_sal > 50000
```

---

## ⏰ **Time Functions**

```kql
// Current time
now()

// Time ago
ago(1d)    // 1 day ago
ago(7d)    // 7 days ago
ago(2h)    // 2 hours ago
ago(30m)   // 30 minutes ago

// Start/End of time periods
startofday(now())       // Today 00:00:00
startofweek(now())      // This week Sunday
startofmonth(now())     // 1st of this month
endofday(now())         // Today 23:59:59

// Yesterday's full day
startofday(ago(1d))     // Yesterday 00:00:00
startofday(now())       // Today 00:00:00

// Round/bin time
bin(timestamp, 15m)     // Round to 15 minutes
bin(timestamp, 1h)      // Round to 1 hour
bin(timestamp, 1d)      // Round to 1 day

// Date parts
datetime_part('year', timestamp)
datetime_part('month', timestamp)
datetime_part('day', timestamp)
datetime_part('hour', timestamp)

// Date difference
datetime_diff('day', end_date, start_date)
datetime_diff('hour', end_time, start_time)
```

---

## 🔤 **String Functions**

```kql
// Pattern matching
| where name contains 'John'        // LIKE '%John%'
| where name startswith 'John'      // LIKE 'John%'
| where name endswith 'Smith'       // LIKE '%Smith'
| where name has 'John'             // Word boundary match

// Case insensitive
| where name contains_cs 'john'     // Case sensitive
| where name !contains 'John'       // NOT contains

// String manipulation
| extend upper_name = toupper(name)
| extend lower_name = tolower(name)
| extend trimmed = trim(' ', name)
| extend replaced = replace('old', 'new', text)
| extend length = strlen(name)

// Concatenation
| extend full_name = strcat(first_name, ' ', last_name)
```

---

## 🔢 **Math & Type Conversion**

```kql
// Convert types
todouble(value)
toint(value)
tolong(value)
tostring(value)
tobool(value)
todatetime(value)

// Math
| extend rounded = round(value, 2)
| extend floored = floor(value)
| extend ceiled = ceiling(value)
| extend absolute = abs(value)

// Null handling
| extend result = coalesce(col1, col2, 'default')
| where isnull(column)
| where isnotnull(column)
| where isempty(column)    // For strings
```

---

## 🔗 **Joins**

```kql
// Inner join
table1
| join kind=inner (table2) on key_column

// Left join
table1
| join kind=leftouter (table2) on key_column

// Join with different column names
table1
| join kind=inner (table2) on $left.id == $right.user_id

// Cross-database join
table1
| join kind=inner (database("otherDB").table2) on key
```

---

## 🎯 **Filtering Patterns**

```kql
// Comparison operators
| where age > 25
| where age >= 25
| where age < 40
| where age <= 40
| where age == 25         // Equality (double ==)
| where age != 25         // Not equal

// Logical operators
| where age > 25 and salary > 50000
| where dept == 'IT' or dept == 'HR'
| where not (age < 18)

// Range
| where age between (25 .. 40)
| where salary !between (30000 .. 50000)

// List membership
| where dept in ('IT', 'HR', 'Finance')
| where dept !in ('Sales', 'Marketing')

// NULL checks
| where isnull(manager_id)
| where isnotnull(manager_id)
| where isempty(description)  // For empty strings
```

---

## 📝 **Data Modification**

```kql
// Insert data
.set-or-append table <|
source_table
| where condition
| project columns

// Delete data
.delete table table_name records <|
table_name
| where condition

// Clear all data
.clear table table_name data

// Drop table
.drop table table_name

// Create table (auto-infer schema)
.set table_name <|
source_query
```

---

## 🎨 **Advanced Patterns**

### **Top N per Group:**

```kql
// Top 3 salaries per department
employees
| order by salary desc
| summarize top_earners = take_any(name, 3) by department
```

### **Pivot (SQL: PIVOT):**

```kql
sales
| summarize total = sum(amount) by product, month
| evaluate pivot(month, sum(total))
```

### **Running Totals:**

```kql
orders
| order by order_date asc
| serialize running_total = row_cumsum(amount)
```

### **Window Functions:**

```kql
employees
| order by salary desc
| serialize rank = row_number()
```

---

## 💡 **Key KQL Concepts**

### **1. Pipe Operator `|`**
Chains operations together (like Unix pipes)

### **2. Order Matters**
Operations execute top to bottom

### **3. `extend` vs `project`**
- `extend`: Add columns (keeps all existing)
- `project`: Select columns (drops others)

### **4. `==` for Equality**
Not `=` (which is for assignment/alias)

### **5. Lowercase Keywords**
`and`, `or`, `not` (not AND, OR, NOT)

---

## 🚀 **Common Recipes**

### **Daily Summary:**
```kql
table
| where timestamp >= startofday(ago(1d))
  and timestamp < startofday(now())
| summarize count(), avg(value) by bin(timestamp, 1h)
```

### **Distinct Count:**
```kql
table
| summarize unique_users = dcount(user_id)
```

### **Latest Record per ID:**
```kql
table
| summarize arg_max(timestamp, *) by id
```

### **Copy Yesterday's Data:**
```kql
.set-or-append target_table <|
source_table
| where timestamp >= startofday(ago(1d))
  and timestamp < startofday(now())
```

---

**Happy Querying!** 🎯
