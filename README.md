

#**FinShare** — Group Expense & Micro-Credit Management System

A DBMS project (UCS310) modeling group expense splitting and peer-to-peer micro-loans — like Splitwise, with added lending and penalty tracking. Built on Oracle (PL/SQL) with a Streamlit dashboard frontend.

Features


Group-based expense tracking with automatic equal splitting
Net balance calculation per user per group (paid vs. owed)
Settlements to clear outstanding balances
Peer-to-peer micro-loans with due dates and auto-calculated overdue penalties
Audit logging via triggers
Streamlit dashboard for groups, balances, loans, and users


Tech Stack

Oracle (PL/SQL, triggers, procedures, functions, cursors) · Oracle APEX REST endpoints · Streamlit · Pandas · Requests

Database

8 tables: Users, FinGroups, Memberships, Expenses, Expense_Split, Loans, Settlements, Audit_Log — with foreign keys and check constraints enforcing business rules (positive amounts, no self-loans, unique splits, etc.).

Views: v_net_balance, v_active_loans, v_group_summary

PL/SQL: add_expense (split logic via cursor), settle_debt, process_overdue_loans, get_net_balance, calculate_penalty, plus triggers for audit logging, overdue flagging, and penalty updates.
