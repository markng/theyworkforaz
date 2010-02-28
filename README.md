They Work for Arizona
=====================

This is a project for notifications of votes for a constituents Arizona legislature representatives.  It's somewhat inspired by small parts of "theyworkforyou" in the UK.

It can currently only be used as a address > district > representatives checker.  Once you've installed the project, if you run :

    manage.py load_shapes
    manage.py load_house_members
    
you'll get an initial data set.

If you'd like to contribute, this project depends on django.  It also depends on the dependencies of geodjango.  You probably want to run this with a postGIS database.