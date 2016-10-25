# MIMINANI
## An Introduction

**MIMINANI** is a genealogical mapper that computatively charts out a users lineage. It is currently a personal, but openly developed project that I started in late 2016. Inspired by my own need to trace my roots as far back and out as I could, I found myself disappointed by available methods to automate the data collection, computation and representation. Which then led me to first design then develop this app.

MIMINANI is a Kiswahili portmanteau of two words, **_"Mimi Nani?"_** A question that means **_"Who Am I?"_**

## Usage
Usage will be dictated by the chosen user interface. Currently, this app is designed to run as a GraphQL-based web service written in Python and developed under Python's Flask web framework. There are two user interfaces I'm currently focussing on (in order of execution):
- Browser-based web app (using KnockoutJS and Bootstrap frameworks)
- Interactive E-mail service

The application currently has 3 deployment configurations. Assign the deployment type by setting the system environment variable, `MIMINANI_CONFIG` to:
- 'development'
- 'testing'
- 'production'

If not set to any of the above, the app will default to a development configuration.

The following command line options are available:
```
usage: manage.py [-?] {test,db,forge,shell,runserver} ...

positional arguments:
  {test,db,forge,shell,runserver}
    test                Run the unit tests.
    db                  Perform database migrations
    forge               Seed fake family tree data
    shell               Runs a Python shell inside Flask application context.
    runserver           Runs the Flask development server i.e. app.run()

optional arguments:
  -?, --help            show this help message and exit
```

To start the app with Flask's Werkzeug development webserver, run `./manage.py runserver`. GraphiQL, GraphQL's API explorer and debugger can then be accessed by navigating to `localhost:5000/graphiql`.

## Changelog
- v0  - Database models based on graph nodes and edges.
- v0a - GraphQL integration