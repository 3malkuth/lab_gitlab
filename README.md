# pylab_gitlab

## Environment

- Assuming you have installed python 3.12 on a linux machine

```
python3.12 -m ensurepip --upgrade
python3.12 -m pip install --user pipenv
pipenv install
```

## Tests, Type safety and Linting

```
pipenv run pytest -v
mypy .                 # this will use the ignores etc. from mypy.ini
```
