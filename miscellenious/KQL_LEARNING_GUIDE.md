# KQL Learning Guide for SQL Users

**Author:** Jagan Murikinati  
**Date:** 2026-04-25  
**Purpose:** Learn KQL (Kusto Query Language) by comparing with SQL

---

## 📚 **Table of Contents**

1. [Basic Concepts](#basic-concepts)
2. [Query Structure](#query-structure)
3. [Selecting Columns](#selecting-columns)
4. [Filtering Rows](#filtering-rows)
5. [Sorting](#sorting)
6. [Aggregations](#aggregations)
7. [Joins](#joins)
8. [Time Functions](#time-functions)
9. [String Functions](#string-functions)
10. [Advanced Operations](#advanced-operations)
11. [Data Modification](#data-modification)
12. [Common Patterns](#common-patterns)

---

## 🎯 **Basic Concepts**

### **Philosophy Difference:**

| SQL | KQL |
|-----|-----|
| **Declarative:** You specify WHAT you want | **Pipeline:** You specify HOW to transform data |
| Clauses: SELECT, FROM, WHERE, GROUP BY | Operators: Pipe `\|` chains operations |
| Query planner optimizes | Order matters (top to bottom) |

### **Example:**

**SQL:**
```sql
SELECT name, age 
FROM users 
WHERE age > 25 
ORDER BY name;
```

**KQL:**
```kql
users
| where age > 25
| project name, age
| order by name asc
```

<!-- In SQL, the engine decides the logical order (FROM → WHERE → SELECT → ORDER BY).

In KQL, you explicitly chain operators with |. -->

**Key Difference:** KQL reads like a pipeline - start with table, then transform step-by-step.

---

## 📋 **Query Structure**

### **Basic Pattern:**

**SQL:**
```sql
SELECT columns
FROM table
WHERE condition
GROUP BY columns
HAVING condition
ORDER BY columns
LIMIT number;
```

**KQL:**
```kql
table
| where condition
| summarize aggregation by columns
| where condition
| order by columns
| take number
```

### **Flow:**

**SQL:** All clauses in one statement  
**KQL:** Chain operators with pipe `|`

---

## 🔍 **1. Selecting Columns (PROJECT)**

### **Select Specific Columns:**

**SQL:**
```sql
SELECT name, id, salary 
FROM employees;
```

**KQL:**
```kql
employees
| project name, id, salary
```

---

### **Select All Columns:**

**SQL:**
```sql
SELECT * 
FROM employees;
```

**KQL:**
```kql
employees
```

---

### **Rename Columns (Alias):**

**SQL:**
```sql
SELECT 
    name AS employee_name,
    salary * 12 AS annual_salary
FROM employees;
```

**KQL:**
```kql
employees
| project 
    employee_name = name,
    annual_salary = salary * 12
```

**Note:** KQL uses `=` (reverse of SQL `AS`)

---

### **Add Calculated Columns:**

**SQL:**
```sql
SELECT 
    name,
    salary,
    salary * 1.1 AS increased_salary
FROM employees;
```

**KQL:**
```kql
employees
| extend increased_salary = salary * 1.1
| project name, salary, increased_salary
```

**Key:** `extend` adds columns, `project` selects columns

---

### **Exclude Columns:**

**SQL:**
```sql
-- Not easy in SQL, need to list all columns except unwanted ones
SELECT id, name, salary -- (manually exclude 'address')
FROM employees;
```

**KQL:**
```kql
employees
| project-away address
```

**Advantage:** KQL can easily exclude columns!

---

## 🎯 **2. Filtering Rows (WHERE)**

### **Basic Filter:**

**SQL:**
```sql
SELECT * 
FROM employees 
WHERE salary > 50000;
```

**KQL:**
```kql
employees
| where salary > 50000
```

---

### **Multiple Conditions (AND):**

**SQL:**
```sql
SELECT * 
FROM employees 
WHERE salary > 50000 AND age < 40;
```

**KQL:**
```kql
employees
| where salary > 50000 and age < 40
```

**Note:** KQL uses lowercase `and`, `or`, `not`

---

### **OR Condition:**

**SQL:**
```sql
SELECT * 
FROM employees 
WHERE department = 'IT' OR department = 'HR';
```

**KQL:**
```kql
employees
| where department == 'IT' or department == 'HR'
```

**Note:** KQL uses `==` for equality (not single `=`)

---

### **IN Clause:**

**SQL:**
```sql
SELECT * 
FROM employees 
WHERE department IN ('IT', 'HR', 'Finance');
```

**KQL:**
```kql
employees
| where department in ('IT', 'HR', 'Finance')
```

---

### **NOT IN:**

**SQL:**
```sql
SELECT * 
FROM employees 
WHERE department NOT IN ('IT', 'HR');
```

**KQL:**
```kql
employees
| where department !in ('IT', 'HR')
```

---

### **LIKE (Pattern Matching):**

**SQL:**
```sql
SELECT * 
FROM employees 
WHERE name LIKE 'John%';
```

**KQL:**
```kql
employees
| where name startswith 'John'
```

**KQL Pattern Matching:**
- `startswith` = SQL `LIKE 'value%'`
- `endswith` = SQL `LIKE '%value'`
- `contains` = SQL `LIKE '%value%'`
- `matches regex` = SQL regex functions

---

### **BETWEEN:**

**SQL:**
```sql
SELECT * 
FROM employees 
WHERE salary BETWEEN 30000 AND 50000;
```

**KQL:**
```kql
employees
| where salary between (30000 .. 50000)
```

---

### **NULL Checks:**

**SQL:**
```sql
SELECT * 
FROM employees 
WHERE manager_id IS NULL;
```

**KQL:**
```kql
employees
| where isnull(manager_id)
```

**Or:**
```kql
employees
| where isempty(manager_id)  // For empty strings
```

---

