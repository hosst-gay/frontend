# hosst

This is the source for the best free open sourced sharex image uploader

# Useful Links
Website: https://hosst.gay <br>
Discord: https://discord.gg/sTHv4CwFnG

# Requirements
In order to self-host this on your own machine/vps
There are a few requirements in order too use it.
--------------------------------------------------
- Python version: python3.8 or above
- Flask
- sqlite3 (will not work with basic sqlite but most linux systems come preinstalled with sqlite3


# Self-hosting

**Note: I do not support self-hosting of this service, but however, i will not stop the use of it being self-hosted**

In order to self host, you need to install a few things

First sqlite3 and a python version above python 3.8 (all modules used in this repo require 3.8 or above)

After you have all those installed, Run the following command

```sh
> pip install flask flask_sqlalchemy flask_login flask_bcrypt flask_wtf wtforms email_validator
```

After you run that, go into the python shell and run

```sh
> from server import db
> db.create_all()
```

This should create a few .db files which are the following, image.db, embed.db, and database.db
image.db is responsible for data of an image, embed.db is for embed customization, and database.db is for user logins, etc.

What you can do to make sure it all worked is by typing in

```sh
> sqlite3 database.db
> .table
> .schema
```
note: You might need to do this for all of the .db files to 
a: make sure all tables are there
b: make sure the schema matches the one i the class with db.Model



if the tables shows "user" then it has worked.

Thats essentially all.


# License

Due to The license attached to this repo, i am in no way, liable to anything you use this source for.

This is open sourced for the sole reason to help people make image hosts or for people too look at this code.

Whatever you do is not my problem.

That being said, i do not permit child pornogrohpy or any other illegal materials being uploaded nor this src being used for those reasons.
