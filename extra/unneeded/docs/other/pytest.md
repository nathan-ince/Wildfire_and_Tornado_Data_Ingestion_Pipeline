
---

**`Command`**

```
pytest --version
```

This command will display the installed version of `pytest`

---

**`Command`**

```
pytest
```

This command will run pytest for the `tests` directory.

---

**`Command`**

```
pytest file
```

- `file` should be the path of a file in `tests`

This command will run pytest for the specified file.

---

**`Flag`**
```
--cov
```

This flag will show a coverage report after running tests.

**`Example`**

```
pytest --cov
```

**`Example`**

```
pytest file --cov
```

- `file` should be the path of a file in `tests`

---

**`Flag`**

```
-s
```

This flag will display `print` statements in the console while running tests.

**`Example`**

```
pytest -s
```

---

**`Command`**

```
pytest -o log_cli=true -o log_cli_level=level
```

- `level` should be a valid logging level, like `INFO` or `DEBUG`

This command will show `logger` statements in the console while running tests.

**`Example`**

```
pytest -o log_cli=true -o log_cli_level=INFO
```

**`Example`**

```
pytest -o log_cli=true -o log_cli_level=DEBUG
```

---
