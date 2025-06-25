# lab_gitlab

## Environment

- Assuming you have installed python 3.12 on a linux machine

```
python3.12 -m ensurepip --upgrade
python3.12 -m pip install --user pipenv
pipenv install
```

## Development Environment: Tests, Type safety, Linting...

```
pipenv install --dev
pipenv run pytest -v
mypy .                 # this will use the ignores etc. from mypy.ini
```
