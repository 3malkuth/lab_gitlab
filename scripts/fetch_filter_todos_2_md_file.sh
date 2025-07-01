#!/bin/bash

cd ..

DIR="build"

if [ -d "$DIR" ]; then
  echo "'$DIR' directory already exists."
else
  echo "'$DIR' not found. Creating..."
  mkdir -p "$DIR"
  echo "'$DIR' directory created."
fi

poetry run python -m issue_fetcher.fetcher_filter_todos > build/issues.md

cd scripts

