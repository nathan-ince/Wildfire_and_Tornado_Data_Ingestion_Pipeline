# **Environment**

This note contains information about our environment variables and settings configuration.

---

### **Environment Variables**

We have our environment variables stored in a file call `.env`.

This file is listed in `.gitignore` because it contains sensitive information.

We have a file called `.env.example` that is not in `.gitignore` that serves as a template for `.env`.

This file essentially lists all teh environment variables we need to define in `.env`.

---

### **Settings Configuration**

At the beginning of each of our scripts, we process our environment variables.

The purpose of doing this is to ensure that all the necessary environment variables are defined and valid as early as possible.

There are some benefits to doing this:
- we can ensure that all the necessary environment variables are present
- we can ensure that all the necessary environment variables are valid
- we can access all out environment variables by exporting one object that contains them all
- when we access environment variables from the settings object, they have the correct datatypes as they have already been processed

If any of the necessary environment variables are missing or invalid, the script will fail early and some helpful information will be logged.

---
