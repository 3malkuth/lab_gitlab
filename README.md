# lab_gitlab

## Goals
- Fetch GitLab issues by label and output them as a single Markdown file.


## Environment

- Prerequisites: Python 3.12, Poetry, GitLab API token
- Setup Poetry:
```
curl -sSL https://install.python-poetry.org | python3.12 -
export PATH="$HOME/.local/bin:$PATH" # write this into your .bashrc file
poetry install

# If you want to use the poetry shell, you need to explicityl install it
poetry self add poetry-plugin-shell

```
- Setup GitLab API token and other environment variables:
  - Create a personal access token in GitLab with `api` scope.
  - Set the token as an environment variable
- Example .ENV bash script you can use to set up your environment variables
```
#!/bin/bash
# To add these to your current shell run:
# source .ENV

export GITLAB_API_TOKEN=your_token_here
export GITLAB_URL=your_gitlab_url_here # no trailing slash
export GITLAB_PROJECT_PATH=your_project_path_here # no start / trailing slash
export GITLAB_LABELS=your_labels_here # use commas to separate multiple labels
```

## Development Environment: Tests, Type safety, Linting...
- Install dependencies
```
# Access the virtual shell
# https://python-poetry.org/docs/managing-environments/#activating-the-environment
poetry shell # activates the environment in a new subshell and updates your prompt

poetry env activate # just sets the environment path internally, meant more for scripting or IDE integration.
# it just tells Poetry which environment to associate with your project.
# So running poetry env activate by itself doesn't actually "enter" the environment — that's why you don't see a prompt change.

# Check if using env python
which python

# Disable the virtual environment and use the system based python env
poetry env use /usr/bin/python3.12 # direct path to system's python
poetry env use system # this should work, but I didn't get it to work

# Run pylint
poetry run pylint src/issue_fetcher

# Check type safety
poetry run mypy src/issue_fetcher

# Run tests
poetry run pytest
```
