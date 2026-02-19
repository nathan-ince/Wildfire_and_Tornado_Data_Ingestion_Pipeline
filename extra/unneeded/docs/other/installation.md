# **Installation**

---

## **Installing pyenv-win**

I found the manual installation process through the following link.

https://github.com/pyenv-win/pyenv-win/blob/master/docs/installation.md#pyenv-win-zip

I downloaded the zip folder.

I extracted the content of the zip folder.

I deleted everything except for the following.

- `pyenv-win`
	- `bin`
	- `libexec`
	- `.versions_cache`
	- `__init__`
	- `install-pyenv-win`

I created two folders that were absent: `shims` and `versions`.

The folder architecture should resemble the following.

- `pyenv-win`
	- `bin`
	- `libexec`
	- `shims`
	- `versions`
	- `.versions_cache`
	- `__init__`
	- `install-pyenv-win`

I moved `pyenv-win` to where I wanted it.

I created the following environment variables.

| Name | Value |
| - | - |
| `PYENV` | path to `pyenv-win` |
| `PYENV_HOME` | path to `pyenv-win` |
| `PYENV_ROOT` | path to `pyenv-win` |

I added the following values to my `Path` environment variable.

| Value |
| - |
| path to `pyenv-win/bin` |
| path to `pyenv-win/shims` |

---

## **Installing Python**

I recommend you install the latest stable version of `Python`.

You can determine the latest stable version through the following link:

https://www.python.org/downloads/windows/

As of right now, the latest stable version is `3.14.2`.

Run the following command:

``` powershell
pyenv install 3.14.2
```

---
