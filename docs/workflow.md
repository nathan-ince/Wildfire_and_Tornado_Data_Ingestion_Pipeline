
---

## **When you sit down to code**

- run `git fetch`

---

## **When you pull a remote branch**

- run `pip install -r requirements.txt`

---

## **When you want to create a local branch**

- run `git switch -c branchname`
  - `branchname` should be a name for your branch

---

## **When you want to push a local branch to the remote**

- ensure you are on the correct local branch
  - you can check by running `git branch`
  - you can switch by running `git switch branchname`
    - `branchname` should be the name of a local branch
- run `git push -u origin branchname`
  - `branchname` should be the name of the local branch you are currently on

---

## **When you want to delete a remote branch**

- run `git push origin --delete branchname`
  - `branchname` should be the name of the remote branch you want to delete
  - you can display a list of the existing remote branches by running `git branch -r`

---

## **When you want to delete a local branch**

- ensure you are not on the branch you want to delete
  - you can check by running `git branch`
  - you can switch by running `git switch branchname`
    - `branchname` should be the name of the branch you want to switch to
- run `git branch {-d | -D} branchname`
  - `branchname` should be the name of the local branch you want to delete
  - `-d` will delete the branch gracefully
  - `-D` will delete the branch forcefully

---

## **When you want to pull your feature branch into the master branch**

- Create a pull request on `GitHub`
- Confirm the pull request.

Once you confirm the pull request and it's successful, you can delete the old branch.

#### Check the Master Branch

- run `git switch master`
- run `git pull`

#### Delete the Old Remote Branch

- run `git push origin --delete branchname`
  - `branchname` should be the name of the old remote branch
- you can run `git branch -r` to see the updated list of remote branches

#### Delete the Old Local Branch

- run `git branch -d branchname
  - `branchname` should be the name of the old local branch
- you can run `git branch` to see the updated list of local branches

- you can run `git branch -a` to see a list of all branches, both local and remote.

---
