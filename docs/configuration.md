# **Configuration**

---

I created a folder for the project.

---

This command will create a file called `.python-version` in the root folder.

``` powershell
pyenv local 3.14.2
```

---

This command will create a virtual environment as a folder called `venv` in the root folder.

``` powershell
python -m venv venv
```

---

This command will activate the virtual environment.

``` powershell
./venv/Scripts/Activate
```

---

This command will install/upgrade some packages.

``` powershell
python -m pip install --upgrade pip setuptools wheel
```

---

This command will save a list of the installled packages in a file called `requirements.txt`.

``` powershell
pip freeze > requirements.txt
```

---

I created a folder called `src` for source code.

I created a folder called `tests` for unit tests.

I created a folder called `data` for data.

I created a folder called `notes` for notes.

I created a file called `.gitignore`.

I added some stuff to the `.gitignore` file.

I created a file called `README.md`.

I added some stuff to the `README.md` file.

I added some notes in the `notes` folder.

---

I initialized the repository.

``` powershell
git init
```

---

I linked to repository to `GitHub`.

``` powershell
git remote add origin https://github.com/JBProphecy/revature-training-project-01
```

---

I made the initial commit.

``` powershell
git add .
git commit -m "Fresh Start"
git push -u origin master
```

---
