# Setting up python virtual environment

Python virtual environment (venv) is a tool that helps manage dependencies for a project by creating an isolated environment with its own installed packages. This ensures that dependencies for different projects do not interfere with each other.

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If you have missing import errors from pylance select the appropriate interpreter for your the venv environment
`ctrl+shift+P` --> Python: Select Interpreter

# Generating requirements

```
pip install pipreqs
pipreqs ./ --ignore .venv
```

# Running db setup script

`sh ./src/scripts/setup-db.sh`
