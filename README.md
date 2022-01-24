# Simple invoices store API

This Project implements a simple invoices store API, with mongodb as backend.
It allows operations:
* On create validate invoice with predefined schema and check for duplicates
* Update contacts in invoices
* contact Partiel search 

Tech stack
* Taskfile -> A makefile alike runner/build tool
* Python 3.8 -> Flask framework to serve API
* docker-compose 1.28.5 -> for local run and development, py-unit-tests

## Run And test the app locally

Make sure you have [`task`](https://taskfile.dev/#/installation) and `docker-compose` installed

Application local developpement run and unit tests are in docker, so no other dependencies needed.

run app locally: ```task local.dev ```

Unit-tests run: ```task unit-tests```

e2e-tests run: ```task e2e-tests```

## Development iterations

For the local development, Run with `task local.dev`, befind the scene the application run in a docker container, its dependency to a standalone mongodb is defined in the docker-compose file. The docker container mounts the current project as a volume, the python app run with `FLASK_ENV: development`, it automatically refresh when code changes.

Tests written in pytest, it uses pytest-mongodb to mock mongodb call, I wrote tests for the controller, run with `task unit-tests`. Befind the scene the pytests run in a docker container with code mount as volume.


### Application design

The application requirement consist of two parts
1. Invoices creation and contact update
2. Data suggestion and anormaly detection

Current solution implements everything under one single component, Invoices creation and contact update map to mongodb document creation and updates, data suggestion use simple mongodb text search feature with scoring.

If I have more time I would design the application differently with 3 components:
1. An API endpoint serve as data collector, it ingests invoice data into a queuing system(e.g Kafka).
2. A Kafka consumer transform and offload invoices data to S3 as parquet format for data analytic usage and machine learning purpose to build anormaly detection and data suggestion model; another kafka consumer transform and offload data to mongodb or a relational db for client-end usage(transational updates, web application etc) it allows seperation of data-lake and transational data store. 
3. An API endpoint to serve persisted model produced by data science team for anormaly detection and data suggestion
