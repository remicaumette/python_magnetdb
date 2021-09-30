= Magnet Database

Tools for creating and manipulating a database designed for Magnet simulations.
Data may be partly retreived from **Lnmi control and monitoringwebsite**.
See `python_magnetrun` for more details

== Structure

Viewing the database: ``sqlitebrowser`
== Python

Running the app

```
python3 -m python_magnetdb.app
``` 

== API

Running the FastAPI Application:

```
uvicorn main:app --app-dir $PWD/python_magnetdb/ --reload
``` 

== Requirements

* sqlmodel
* fastapi
* uvicorn
* sqlitebrowser

== References

(sqlmodel)[https://sqlmodel.tiangolo.com/tutorial]