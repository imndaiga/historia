# miminani
## An Introduction

### miminani is a Kiswahili portmanteau of two words, **_"Mimi Nani?"_** A question that asks **_"Who Am I?"_**

**miminani** is a web app that computatively graphs a users lineage using their social network connections. The user can then add, modify and share their trees as needed. Submitted data is used for basic research into the genealogical structures that define the over 40 tribes in Kenya. However, this repository's source code can be put to use in other regions. For the purposes of this project, none of the data collected will be shared with any third party without the direct consent of any users (opt-in). Any and all data being collected will also be declared openly. I'm not a fan of terms and conditions, but if this should change at any point please expect an email from me <miminani@squarenomad.com> indicating as much.

Currently, the feature pipeline is as follows:
- Integrate with Facebook's Social Graph API.
- Integrate with Auth0 for frictionless sign-up and registration.
- Allow manual, permissions-based modification of genealogical trees.
- Generate genealogical tree visualisations on demand.
- Integrate graph search algorithms that can span vast and disparate trees for statistical analysis.

## Usage
Developer usage is simple enough and powered by docker. Currently, this app is written and developed in Python's [Flask](http://flask.pocoo.org/) web framework and using [bootstrap](http://getbootstrap.com/). The only requirement for any host environment (Windows, Linux or MacOS) is to have a running installation of [docker](http://www.docker.com/). To locally run, develop or test your own app instance, please run the following commands in your preferred shell environment on your host (I recommend powershell for Windows users):
- ```mkdir miminani && cd miminani```
- ```git clone https://github.com/squarenomad/miminani.git .```
- ```docker build -t miminani:latest .```

The last of these commands will create a docker image that can be used to spin up containers. There are two basic docker container types you can create for this app. The first involves starting up the app as a web application. The second starts up a shell environment loaded with a number of the apps' python modules and helper functions (for debugging purposes). Before starting the containers, please create a file in the miminani directory called .env and populate it the following variables.
```
MAIL_SERVER=<Enter_Value>
MAIL_PORT=<Enter_Value>
MAIL_USERNAME=<Enter_Value>
MAIL_PASSWORD=<Enter_Value>
RECAPTCHA_PUBLIC_KEY=<Enter_Value>
RECAPTCHA_PRIVATE_KEY=<Enter_Value>
MIMINANI_ADMIN=<Enter_Value>
```
These variables will be exported to the docker container environment at build time.

To start up the first container type on a unix host, run ```docker run -p 5000:5000 -d --name minaapp --env-file ./.env -v $(pwd):/app miminani```. To set up the second, run ```docker run -it --name minashell -v $(pwd):/app miminani shell```. A windows host would require one to replace the _$(pwd)_ reference with the absolute path name that points to the miminani directory (e.g. c:/Users/<your-username>/miminani). One can change the docker command flags as needed, but the command configuration I've provided allows for hot-loading, env-setting and port assignment in one swop.

Alternatively, one can choose to run the app outside of docker if they are running on a unix host. By default, the app starts with a development configuration. This can be changed by appropriately setting the environment variable MIMINANI_CONFIG to the required string ('testing','development','production').

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
### 0.1
- Database models based on graph nodes and edges.
- Welcome page with passwordless authentication.
- Transactional Mail functionality.
- db and app testing suite.