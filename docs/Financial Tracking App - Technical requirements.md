## 1. Financial Tracking App
## 2. Team

- **Eldos Baktybek uulu** - fullstack developer, UI/UX designer, devops.
- **Erkin Tursunov** - database management, Q/A.
## 3. Brief Description

##### Main goal is to provide a simple and fast system to track expenses from any device.

A financial tracking application that allows users to manage their income and expenses efficiently. The app supports budgeting, goal tracking, spending analytics, and multiple account management. Users can receive notifications, access real-time exchange rates, and export financial reports in various formats.

## 4. Target Audience
- Individuals tracking personal finances
- Families managing shared expenses
- Small business owners
- Freelancers and independent contractors

## 5. Competitive Advantages
- Intuitive UI with customizable categories
- Multi-account support
- Sharing and family accounts
- Advanced analytics with graphical reports
- Real-time exchange rate updates
- Secure data handling with role-based access
- Fully free
- Real-time synchronization across all devices.

## 6. Functional Description

- **Income & Expense Management:** Add, edit, categorize transactions
- **Budgeting & Savings Goals:** Set financial goals and track progress
- **Graphical Reports & Spending Analytics:** Pie charts, bar graphs, monthly comparisons
- **Export Reports:** Generate CSV, PDF, XLSX reports
- **Notifications & Reminders:** Payment due, budget exceeded alerts, no transactions for long period of time.
- **Real-Time Exchange Rates:** Fetch currency data from an API
- **Multi-Account Support:** Track multiple wallets/bank accounts
- **Read-Only Sharing:** Share finances without edit permissions
- **Family Accounts:** Multi-user access with defined roles

![[Functional diagram.jpg]]
## 7. User Roles & Permissions

### **Roles**

- **User**: Add/edit own transactions, manage personal settings
- **Family Member**: Access shared accounts with limited permissions
- **Guest (Read-Only)**: View shared financial data

### **Use Case Diagram (UML)**
![[Use cases.png]]
## 8. Technology Stack

### **Frontend:**
- **Telegram Mini App:** Vue.js / Nuxt.js
- **For UI styling:** TailwindCSS, Primevue/NuxtUI.
- **For analytics visualization:** Chart.js / D3.js.

### **Backend:**
- Django Rest Framework (API layer)
- Celery (for scheduled tasks like reminders)
- PostgreSQL (database)

### **Third-party APIs & Integrations:**
- For exchange rates: nbkr.kg, valuta.kg

### **Infrastructure & DevOps:**
- Docker (for containerization)
- Nginx (for reverse proxy)
- AWS/GCP (for hosting and cloud services)
- PostgreSQL (for relational data storage)
- Redis (caching, message queue)

### **Testing:**
- Pytest - unit tests on the backend, database
- Jest - unit tests on the frontend
- Postman - backend API-integration tests
- Selenium/playwright - frontend UI-integration tests

### **Documentation:**
- Postman - API documentation
- Notion - project documentation

### **Task management:**
- Trello - kanban board for task management
## **9. General System Architecture**
![[Sysdesign.jpg]]

## **10. Database Schema**

![[Database ER diagram.png]]
## **1. User Operations**

### ✅ **Upsert (Insert or Update) User**

- **Action:** Create or update a user if they already exist.
- **SQL:**
    
    ```sql
    INSERT INTO users (id, full_name, username, created_at) 
    VALUES (1, 'John Doe', 'johndoe', NOW())
    ON CONFLICT (username) 
    DO UPDATE SET full_name = EXCLUDED.full_name, created_at = NOW();
    ```
    
- **Edge Cases & Fixes:**
    - **Username Conflict:** Solved by `ON CONFLICT (username) DO UPDATE`.
    - **Case Sensitivity:** Use `LOWER(username)`.
    - **Missing Required Fields:** Enforce `NOT NULL` constraints.

### 📖 **Read User Profile**

- **SQL:**
    
    ```sql
    SELECT * FROM users WHERE LOWER(username) = LOWER('JohnDoe');
    ```
    
- **Edge Cases & Fixes:**
    - **User Not Found:** Return a structured error message.
    - **Deleted Users:** Filter `WHERE deleted_at IS NULL`.

### ✏️ **Update User**

- **SQL:**
    
    ```sql
    UPDATE users SET full_name = 'Johnathan Doe' WHERE id = 1;
    ```
    

### ❌ **Delete User**

- **Edge Cases:** Prevent deletion of users with active accounts.
- **SQL (Soft Delete):**
    
    ```sql
    UPDATE users SET deleted_at = NOW() WHERE id = 1;
    ```
    

---

## **2. Account Operations**

### ✅ **Create or Update Account**

- **SQL:**
    
    ```sql
    INSERT INTO accounts (id, user_id, name, created_at, is_public) 
    VALUES (101, 1, 'Savings', NOW(), false)
    ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, is_public = EXCLUDED.is_public;
    ```
    
- **Edge Cases:**
    - **Ensure user exists:** `FOREIGN KEY (user_id) REFERENCES users(id)`.
    - **Prevent duplicate names:** Add a `UNIQUE(user_id, name)`.

### 📖 **Read User Accounts**

- **SQL:**
    
    ```sql
    SELECT * FROM accounts WHERE user_id = 1;
    ```
    
- **Edge Cases:**
    - **Ensure empty results don’t break queries** → Return empty array in APIs.
    - **Access Control:** Ensure only the user or shared users can view an account.

### ❌ **Delete Account**

- **Edge Cases:**
    
    - Prevent deletion if transactions exist.
    
    ```sql
    DELETE FROM accounts WHERE id = 101;
    ```
    

---

## **3. Transaction Operations**

### ✅ **Create Transaction (Income/Expense)**

- **SQL:**
    
    ```sql
    INSERT INTO transactions (id, category_id, account_id, amount, note, type, created_at) 
    VALUES (1001, 10, 101, 500.00, 'Freelance Payment', 'income', NOW());
    ```
    
- **Edge Cases:**
    - **Prevent negative amounts:** `CHECK (amount > 0)`.

### 📖 **Read Transactions for an Account**

- **SQL:**
    
    ```sql
    SELECT * FROM transactions WHERE account_id = 101 ORDER BY created_at DESC;
    ```
    
- **Edge Cases:**
    - **Filter by time range**:
        
        ```sql
        SELECT * FROM transactions WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31';
        ```
        
    - **Summarize transactions:**
        
        ```sql
        SELECT type, SUM(amount) FROM transactions WHERE account_id = 101 GROUP BY type;
        ```
        

### ❌ **Delete Transaction**

- **SQL:**
    
    ```sql
    DELETE FROM transactions WHERE id = 1001;
    ```
    
- **Edge Cases:**
    - **Ensure balance remains accurate after deletion.**

---

## **4. Transfer Operations**

### ✅ **Create Transfer**

- **SQL:**
    
    ```sql
    INSERT INTO transfers (id, from_account_id, to_account_id, amount, note, date, created_at) 
    VALUES (2001, 101, 102, 200.00, 'Rent Payment', NOW(), NOW());
    ```
    
- **Edge Cases:**
    - **Prevent transfers between the same account.**
    - **Ensure accounts belong to the same user or are shared.**

### 📖 **Read Transfers**

- **SQL:**
    
    ```sql
    SELECT * FROM transfers WHERE from_account_id = 101 OR to_account_id = 101;
    ```
    

---

## **5. Category Operations**

### ✅ **Create Category**

- **SQL:**
    
    ```sql
    INSERT INTO categories (id, user_id, name, type, parent_id) 
    VALUES (10, 1, 'Groceries', 'expense', NULL);
    ```
    
- **Edge Cases:**
    - **Ensure `type` is only 'income' or 'expense'.**

### 📖 **Read Categories**

- **SQL:**
    
    ```sql
    SELECT * FROM categories WHERE user_id = 1;
    ```
    
- **Edge Cases:**
    - **Retrieve nested categories:**
        
        ```sql
        SELECT * FROM categories WHERE parent_id = 10;
        ```
        

### ❌ **Delete Category**

- **SQL:**
    
    ```sql
    DELETE FROM categories WHERE id = 10;
    ```
    
- **Edge Cases:**
    - Prevent deletion if linked to transactions.

---

## **6. Exchange Rate Operations**

### ✅ **Insert Exchange Rate**

- **SQL:**
    
    ```sql
    INSERT INTO exchange_rates (id, base_currency, target_currency, rate, updated_at) 
    VALUES (1, 'USD', 'EUR', 0.85, NOW())
    ON CONFLICT (base_currency, target_currency) 
    DO UPDATE SET rate = EXCLUDED.rate, updated_at = NOW();
    ```
    
- **Edge Cases:**
    - **Ensure rates are positive:** `CHECK (rate > 0)`.

### 📖 **Read Exchange Rate**

- **SQL:**
    
    ```sql
    SELECT * FROM exchange_rates 
    WHERE base_currency = 'USD' AND target_currency = 'EUR' 
    ORDER BY updated_at DESC 
    LIMIT 1;
    ```
    

---

## **7. Compute User Balance**

### **Compute Account Balance (Income - Expense)**

- **SQL:**
    
    ```sql
    SELECT 
      a.id AS account_id, 
      a.name AS account_name, 
      COALESCE(SUM(CASE WHEN c.type = 'income' THEN t.amount ELSE 0 END), 0) AS total_income, 
      COALESCE(SUM(CASE WHEN c.type = 'expense' THEN t.amount ELSE 0 END), 0) AS total_expense, 
      (COALESCE(SUM(CASE WHEN c.type = 'income' THEN t.amount ELSE 0 END), 0) - 
      COALESCE(SUM(CASE WHEN c.type = 'expense' THEN t.amount ELSE 0 END), 0)) AS balance 
    FROM accounts a 
    LEFT JOIN transactions t ON a.id = t.account_id
    LEFT JOIN categories c ON c.id = t.category_id
    WHERE a.user_id = 1 
    GROUP BY a.id, a.name;
    ```
    
- **Edge Cases:**
    - Ensure accounts without transactions return `0` balance.

---

### **Summary of Edge Cases**

|**Entity**|**Edge Cases & Fixes**|
|---|---|
|**Users**|Handle username conflicts, prevent duplicates.|
|**Accounts**|Prevent deletion if transactions exist.|
|**Transactions**|Ensure type matches category, prevent negative amounts.|
|**Transfers**|Prevent self-transfers, ensure account ownership.|
|**Categories**|Prevent deletion if linked to transactions.|
|**Exchange Rates**|Ensure rates are positive, avoid outdated values.|

### ✅ **Add Exchange Rate**

- **Action:** Record a currency exchange rate.
- **SQL:**
    
    ```sql
    INSERT INTO exchange_rates (base_currency, target_currency, rate, updated_at) 
    VALUES ('USD', 'EUR', 0.85, NOW());
    ```
    

### 📖 **Get Exchange Rate**

- **Action:** Retrieve the latest exchange rate for a currency pair.
- **SQL:**
    
    ```sql
    SELECT * FROM exchange_rates 
    WHERE base_currency = 'USD' AND target_currency = 'EUR' 
    ORDER BY updated_at DESC 
    LIMIT 1;
    ```
    

### ✏️ **Update Exchange Rate**

- **Action:** Modify an existing exchange rate.
- **SQL:**
    
    ```sql
    UPDATE exchange_rates 
    SET rate = 0.87, updated_at = NOW() 
    WHERE base_currency = 'USD' AND target_currency = 'EUR';
    ```
    

### ❌ **Delete Exchange Rate**

- **Action:** Remove an outdated exchange rate.
- **SQL:**
    
    ```sql
    DELETE FROM exchange_rates 
    WHERE base_currency = 'USD' AND target_currency = 'EUR';
    ```
    

## **11. Frontend Design**

## **12. Backend Endpoints**

## **13. Project Plan (Gantt Chart)**

![[Gantt diagram.png]]