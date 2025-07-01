#!/bin/bash

cd ..

echo "Running pylint..."
poetry run pylint .
# poetry run pylint src # src directory only

echo ""
echo "Running mypy..."
poetry run mypy .
# poetry run mypy src # src directory only

echo ""
echo "Running pytest..."
poetry run pytest -vvvvvv

cd scripts
