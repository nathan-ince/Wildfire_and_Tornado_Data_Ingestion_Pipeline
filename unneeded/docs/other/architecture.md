
---

## **Current File System Architecture**
- `root`
  - This folder is the root of our project.
  - It's currently named `revature-training-project-01`.
  - `data`
    - This folder is for data.
  - `docs`
    - This folder is for documentation.
  - `src`
    - This folder is for source code.
    - `app`
      - This folder is for business logic.
    - `scripts`
      - This folder is for scripts.
      - In each script is where we should do `from app import configure_logging` and call it.
    - `temp`
      - This folder is for anything that we have not yet organized.
  - `tests`
    - This folder is for test code.
    - `conftest.py` is a special file

---

## **SRC and TESTS**

The `src` and `tests` folder should mirror each other, meaning every folder in `src` should have a `tests` counterpart. For example, we have `app` and `scripts` in `src`, so I pust `test_app` and `test_scripts` in `tests`.

I named them with the prefixed `test_` to avoid module conflicts when importing. For example, we can do `from app import ...` from anywhere in the `tests` folder (configured in `pyproject.toml`). I ran into some issues when trying to import from `app` while in `tests/app`.

---
