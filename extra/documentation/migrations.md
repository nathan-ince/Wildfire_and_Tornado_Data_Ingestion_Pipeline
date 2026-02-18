# **Migrations**

We have versioned `SQL` files containing all of our `DDL` statements.

If used correctly, these files can be used to migrate our database from one state/version to the next.

---

## **What is a migration?**

A migration is the process of moving the schema from one state to the next.

Let's say you create a new database.

You create `V001` and write some `DDL` statements.

You run `V001` to migrate your database to `V001`.

At this point, you should never alter `V001` nor run it again.

You create `V002` and write some more `DDL` statements.

You run `V002` to migrate your database from `V001` to `V002`.

At this point, you should never alter `V002` nor run it again. The same rule still applies for `V001` and all previous files in the migration chain.

These migration files build on one another. If you have a schema built with migrations `V001` - `V005` and you want to reproduce that schema. You could create a new database and run each migration file in order from `V001` - `V005`, not just `V005`.

---

## **Our Implementation vs More Sophisticated Options**

We are not using a database migration tool.

Database migration tools such as `Flyway` (I've used it in `Java`) do more than we are doing.

In addition to our versioned `SQL` files,
- which contain mostly if not completely `DDL` statements
- where the order is essential and each one should only be ran only once
- which naturally tracks schema history if used correctly
- which allows schema to be reproduced if used correctly

database tools like `Flyway`
- create a table
  - to track which migrations have ran
  - to track when each migration ran
  - to track who ran each migration
  - to store the checksum of each file
  - to track whether or not each migration succeeded
- will wrap migrations in transactions
- will prevent migration files from being edited
- will protect against concurrent actions / race conditions
- have a rollback strategy
- have CI/CD integration built-in

---

## **What could go wrong?**

Let's say we have `V001` and `V002` and our schema reflects that.

I make a branch and you make a branch.

We both make `V003`.

I run `V003` in my branch, it updates the database successfully.

You run `V003` in your branch. In reality, this should now be `V004`.

With `Flyway` or another database migration tool, having a migration table in our database would prevent you from running your `V003`.

Since we are doing this thing manually, you would be able to run it.

Both of our migraion folders would be out of sync. We should both be on `V004`, but we're each on our own `V003` and beyond if we ran more. To fix it, we would have to figure out who ran `V003` first and make the other `V003` `V004` instead. If we each ran more than one migration, we would have to figure out the right order for all of them.

I imagine if something like that happened, we would need to scrap both of our migration folders and restart.

---

## **Why our implementation is enough...**

In addtion to this not being a requirement of our project,
- our project is not public, so there are no clients who could suffer from our mistakes
- our database is small enough that we could easily fix anything that goes wrong, gets out of sync, etc.
- it's better than nothing, even if we mess it up and the migration files become useless, it would be like we never did it at all
- if we do it right, it can be useful

---

## **Should we mention this in our presentation?**

That's debatable.

In a real-world project, we would most certainly use a migration tool.

Our manual approach is not scalable at all, but it's a little better than not doing it and it's not hard to do.

Our manual approach can be useful in a few cases, but I think the biggest benefit is this...
- it shows that we're aware of the concept of database migrations
- switching from our manual approach to a real database migration tool is definitely in the realm of "future improvements"

---
