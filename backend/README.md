# Setting up python virtual environment

Change to the backend directory `cd backend``

Python virtual environment (venv) is a tool that helps manage dependencies for a project by creating an isolated environment with its own installed packages. This ensures that dependencies for different projects do not interfere with each other.

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Install pre-commit hook
`pip install pre-commit`

If you have missing import errors from pylance select the appropriate interpreter for your the venv environment
`ctrl+shift+P` --> Python: Select Interpreter

### Troubleshooting issues with missing import errors in VsCode due to venv

Your VsCode / other IDE's might show errors for imports sometimes due the interpreter not being correctly set to match the venv.

If it's not showing up there create `.vscode` folder in root with `settings.json` file inside of it and include:
`"python.defaultInterpreterPath": "{PATH_TO_VENV_PYTHON}"`

eg: `"python.defaultInterpreterPath": "/Users/example_user/coding/unmatched/backend/.venv/bin/python"`

If you face similar issues with `Pylint` or `mypy` or similar tools add to the settings to allow them to locate the modules:

```
  "pylint.args": ["--init-hook", "import sys; sys.path.insert(0, './backend/src')"],
  "mypy-type-checker.args": ["--python-path", "./backend/src"]
```

# Generating requirements

```
pip install pipreqs
pipreqs ./ --ignore .venv
```

# Running db setup script

Make sure you have postgres or postgress app running

`bash ./src/scripts/run-populate-db.sh`

Then create .env file inside of the root and add development database URL

```
DATABASE_URL=postgresql+psycopg2://dev_user:dev_password@localhost:5432/unmatched_dev
```

# Seeding db with csv data

Files taken from https://www.umleague.net/fighterstats are stored in data folder these are then used to seed the db data

`bash src/scripts/run-populate-db.sh`

# Running tests

Backend test suite is setup using pytest run it:

`pytest`

Tests with coverage

```
coverage run -m pytest
coverage report
```

Or to see it on the browser
`coverage html`

Then open htmlcov/index.html in your browser

# Starting up the API routes

```
fastapi dev src/main.py
```

This should start up the backend with hot reloading

View docs at
`http://127.0.0.1:8000/docs`
