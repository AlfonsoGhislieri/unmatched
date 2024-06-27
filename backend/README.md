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

Using pipreqs, this method is preferred since it only adds packages that are imported in the codebase. **However it does not add packages that are not imported like `coverage` or `psycopg2`, so these need to be manually added.**

```
pip install pipreqs
pipreqs ./ --ignore .venv
```

**Or** using pip freeze, however this leads to a much larger file, and includes all packages in the venv.

```
pip freeze
```

Add these to requirements.txt

# Manually populating db with csv data

Files are downloaded from https://www.umleague.net/fighterstats and stored in different worksheets in an excel file, which lives in the `src/data` folder, these are used to seed the db data.

**Important:** data is automatically populated into the db from the backend container on startup, but it will only run the script if the file changes (it compares hashes). So if you drop tables/make changes and want a fresh db you need to manually run the following script.

`bash src/scripts/run-populate-db.sh`

# Running tests

Backend test suite uses `testcontainers`, requiring no local setup, just use run it with:

`pytest`

Tests with coverage

```
coverage run -m pytest
coverage report
```

Or to see it on the browser
`coverage html`

Then open htmlcov/index.html in your browser
