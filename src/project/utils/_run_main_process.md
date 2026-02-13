# **_run_main_process.md**

This file exports a single function.

That function is reusable... it can be used for any pipeline we define in this project, as long as it satisfies a few things:
- The pipeline must use our `Config` model.
- The database must have the two tables set up correctly.

The function accepts two parameters:
- `config_file_path`
- `transform_data`

In terms of ETL:
- `E` and `L` depend on `config_file_path`
- `T` depends on `transform_data`

---
