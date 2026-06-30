# FinShare — Group Expense & Micro-Credit Management System

FinShare is a relational database project that models how a group of people split shared expenses and lend small amounts of money ("micro-credit") to each other — similar to apps like Splitwise, but with an added peer-to-peer loan and penalty system. The project was built as a DBMS course assignment (UCS310) to demonstrate schema design, multi-table joins, views, and PL/SQL procedures, functions, cursors, and triggers, with a live Streamlit dashboard on top.

## Features

- **Group expense tracking** — users can be members of multiple groups, and expenses paid within a group are split (equally, for now) among all active members.
- **Automatic expense splitting** — a PL/SQL procedure calculates and inserts equal splits across all active group members whenever an expense is added.
- **Net balance calculation** — for every user in every group, the system computes how much they've paid vs. how much they owe, producing a net balance (positive = owed money, negative = owes money).
- **Settlements** — users can record payments to each other to settle outstanding balances, which marks related expense splits as settled.
- **Micro-credit / peer loans** — users can lend money directly to other group members, with due dates, statuses (active/repaid/overdue), and automatically calculated late penalties.
- **Automated overdue handling** — triggers automatically flag loans as overdue past their due date and recalculate penalty amounts.
- **Audit logging** — every expense insertion and settlement is automatically logged via triggers/procedures for traceability.
- **Dashboard** — a Streamlit frontend (dark-themed) presents group summaries, net balances, active loans, and registered users, pulling live data from an Oracle APEX REST API.

## Tech Stack

| Layer | Technology |
|---|---|
| Database | Oracle (via Oracle APEX) |
| Backend logic | PL/SQL (procedures, functions, triggers, cursors) |
| Data access | Oracle APEX auto-generated REST endpoints |
| Frontend | Streamlit (Python) |
| Data handling | Pandas, Requests |

## Database Design

The schema consists of 8 tables modeling the full expense-and-credit lifecycle:

- **Users** — registered users
- **FinGroups** — expense-sharing groups
- **Memberships** — many-to-many relationship between users and groups, with roles (admin/member) and status
- **Expenses** — financial events paid by a user within a group
- **Expense_Split** — how each expense is divided among group members, with settlement status
- **Loans** — peer-to-peer micro-credit between users within a group, with due dates and penalty tracking
- **Settlements** — records of repayments between users
- **Audit_Log** — system-wide audit trail of key actions

Referential integrity is enforced throughout with foreign keys, and business rules (positive amounts, no self-loans, no self-settlements, unique group membership, unique expense splits) are enforced with `CHECK` constraints.

### Views

Three views simplify common queries for the application layer:

- `v_net_balance` — per-user, per-group balance (total paid vs. total owed)
- `v_active_loans` — loan details joined with lender/borrower names and computed days overdue
- `v_group_summary` — per-group member count, expense count, total spend, and average expense

### PL/SQL Logic

- **Procedures**: `add_expense` (validates and splits a new expense across active members via a cursor), `settle_debt` (records a settlement and marks splits as settled), `process_overdue_loans` (batch-recalculates penalties for all overdue loans via an explicit cursor)
- **Functions**: `get_net_balance` (computes a user's net balance in a group), `calculate_penalty` (computes accrued penalty on an overdue loan at 2%/day)
- **Triggers**: auto-audit-logging on new expenses, auto-flagging loans as overdue past due date, auto-recalculating penalty on loan updates

## Project Structure

```text
01_schema.sql        -- table definitions, constraints, foreign keys
02_sample_data.sql    -- sample users, groups, expenses, loans, settlements
03_queries.sql        -- example analytical queries (joins, aggregates, subqueries)
04_views.sql          -- reusable views for the application layer
05_plsql.sql          -- procedures, functions, triggers, cursors
app.py                -- Streamlit dashboard
db.py                 -- REST API client for Oracle APEX
requirements.txt       -- Python dependencies
```

## Setup & Running

### 1. Database setup (Oracle APEX)

Run the SQL scripts in order against your Oracle APEX workspace:

```sql
01_schema.sql
02_sample_data.sql
04_views.sql
05_plsql.sql
```

Then expose `users`, `groups` (via `v_group_summary`), `balances` (via `v_net_balance`), and `loans` (via `v_active_loans`) as RESTful Data Services / ORDS endpoints under your APEX workspace, matching the endpoint names used in `db.py`.

### 2. Frontend setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

Update `BASE_URL` in `db.py` to point to your own Oracle APEX REST endpoint.

## Example Queries

`03_queries.sql` includes example analytical SQL such as:

- Total spend and average expense per group
- Each user's contribution across groups
- Users who are members of more than one group
- Users who have never paid for an expense ("freeloaders")
- Groups with total spending above a threshold
- All currently overdue loans with days overdue

## Future Improvements

- Support custom (non-equal) expense splits
- Add interest accrual on active loans, not just penalties on overdue ones
- Add authentication so each user only sees their own groups
- Move from Oracle APEX REST to a dedicated backend (e.g., FastAPI) for more control over business logic
