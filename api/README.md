# API Rest 
Database for applications

## Installation
  - Install [Python](https://www.python.org/downloads/), [Pipenv](https://docs.pipenv.org/) and [Postgres](https://www.postgresql.org/) on your machine

  - Install `pipenv` 
  - Activate the project virtual environment with `$ pipenv shell` command 
  - `install -r requirements.txt` to install dependencies
  - Rename .env.example for .env and configure
  - Start the app with `python run.py`

## Migration
  `python37 manage.py db init`
  `python37 manage.py db migrate`
  `python37 manage.py db upgrade`

## Compatibility
* [Tested on Python 2.7 and 3.6, 3.7]

Notes
=================
