# **Schema**

This note contains information about our database schema.

---

## **Data Tables**

We process two datasets in this project.

For each dataset, we have four tables.
- accepted stage
- rejected stage
- accepted final
- rejected final

---

## **General Data Table Information**

The accepted tables are for accepted records.

The rejected tables are for rejcted records.

The stage tables are for staging records, before merging into the final tables.

---

## **Specific Data Table Information (accepted)**

The accepted stage table consists of:
- all data fields
- batch_process_id
- content_hash

The accepted final table consists of:
- all data fields
- batch_proccess_id
- id (surrogate key)
- content_hash

---

## **Specific Table Information (rejected)**

The rejected stage table consists of:
- all data fields
- batch_process_id
- content_hash
- rejected_reason

The rejected final table consists of:
- all data fields
- batch_process_id
- id (surrogate key)
- content_hash
- rejected_reason

---

## **Additional Tables (meta)**

We have two tables that are shared by all the datasets in our project.
- main_process
- batch_process

The main process table consists of records for each pipeline process we invoke.

The batch process table consists of records for each source that we process.

These tables are used to track each main process we invoke, which sources/batches were processed during each main process, and which sources/batches each record from our data tables came from.

---

## **Honorable Mention**

I'm not sure if "functional key" is a real term.

---

## **Surrogate Key and Functional Key**

For each dataset and respective set of tables, since there are no individual candidate keys:
- Our primary key is a surrogate key, which is an auto-generated integer.
- We have a composite unique constraint consisting of several fields, which serves as a functional key.

To determine whether or not a record exists in our table, we use the functional key.
- If we find a record that satisfies the constraint, we can check whether or not the content has changed based on the content hash.
- The content hash is a hash computed by aggreating specific columns and hashing that combination.

We use the stage table and then merge it into the final table so that Postgres will handle the upsert.

When we merge the records from the stage table into the final table, there are three scenarios:
- the functional key is matched and the content hash is matched
  - leave existing record alone / do nothing
- the functional key is matched and the content hash is not matched
  - update existing record
- the functional key is not matched
  - insert new record

---
