# **Idempotency**

- created function(s) to compute a hash series for a dataframe
- altered the transform function for each pipeline to include a content hash field in each dataframe
  - the choice to put it here vs in the runner function is a matter of scalability
    - although our datasets use all data fields for the hash, each dataset could specify different fields to include/exclude from the hash
- created db migration `V006` to include the content hash field for each data table

---
