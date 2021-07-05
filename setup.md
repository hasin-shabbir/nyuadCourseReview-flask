# Flask-MongoDB Example Web App

A simple example of a web app using [pymongo](https://pymongo.readthedocs.io/en/stable/index.html) to interact with a MongoDB database.

It is possible to run this app remotely or locally. Instructions are included for each.

## Run locally

To run this app locally, first clone this repository to your local machine...

`git clone url-to-this-repository`

... and then do the following:

### Set up a Python virtual environment

This command creates a new virtual environment with the name `.venv`:

```bash
python3 -m venv .venv
```

#### Activate the virtual environment

To activate the virtual environment named `.venv`...

On Mac:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate.bat
```

#### Install the dependencies into the virtual environment

The file named, `requirements.txt` contains a list of dependencies - other Python modules that this app depends upon to run.

To install the dependencies into the currently-active virtual environment, use `pip`, the default Python "package manager" - software that takes care of installing the correct version of any module into your in the correct place for the current environment.

```bash
pip3 install -r requirements.txt
```

### Set up a local MongoDB database server

So you must have your app connect to either a cloud hosted database server, such as [MongoDB Atlas](https://www.mongodb.com/cloud/atlas), or download [MongoDB Community Server](https://www.mongodb.com/try/download/community) and run a local database server on your own machine.

### Run the app

1. define two environment variables from the command line: `export FLASK_APP=app.py` and `export FLASK_ENV=development`
1. copy the file named `env.example` into a new file named `.env`, and enter your own MongoDB database connection credentials into that file where indicated.
1. start flask with `flask run` - this will output an address at which the app is running locally, e.g. https://127.0.0.1:5000. Visit that address in a web browser.
1. in some cases, the command `flask` will not be found when attempting `flask run`... you can alternatively launch it with `python3 -m flask run --host=0.0.0.0 --port=10000`.

