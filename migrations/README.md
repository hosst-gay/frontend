# hosst

This is the source for the sharex image host "hosst"


# Self-hosting
In order to self host, you need to install a few things

First sqlite3 and a python version above python 3.8 (all modules used in this repo require 3.8 or above)

After you have all those installed, Run the following command

``pip install flask flask_sqlalchemy flask_login flask_bcrypt flask_wtf wtforms email_validator``

After you run that, go into the python shell and run

""from server import db""

""db.create_all()""

That will create the database.db file and make all the characteristics and columns of the DB.

What you can do to make sure it all worked is by typing in

""sqlite3 database.db""
"".table""

if the tables shows "user" then it has worked.

Thats essentially all.


# License

Due to The license attached to this repo, i am in no way, liable to anything you use this source for.

This is open sourced for the sole reason to help people make image hosts or for people too look at this code.

Whatever you do is not my problem.
