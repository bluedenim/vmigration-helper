# Initialize Project

## Prerequisites
- Install Docker & Compose

## Build Docker Image
```
git clone https://github.com/bluedenim/vmigration-helper.git
cd vmigration-helper
docker compose build
docker compose run --rm app uv run python manage.py migrate
```

## Adding New Dependencies
```
docker compose run --rm --user root app /bin/bash
uv add ...
```

## Build Package
```
rm -rf dist
docker compose run --rm app uv build
```

Verify the package has all the files expected (and none you don't expect):
```
tar tvzf dist/vmigration_helper-<version>.tar.gz
```

## Publish

### TestPyPI
- Double-check **version** in `pyproject.toml`. Rebuild if necessary (see above).
- Ensure that there is a section in `pyproject.toml` defining the `testpypi` index. **This should already be the case.**
    ```
    [[tool.uv.index]]
    name = "testpypi"
    ...
    ```
- Run:
    ```
    docker compose run --rm app uv publish --index testpypi --user __token__ --password {API token}
    ```

You will need credentials (API Token) for this. Set one up in https://test.pypi.org/ as needed.

### PyPI
- Double-check **version** in `pyproject.toml`. Rebuild if necessary (see above).
- Run:
    ```
    docker compose run --rm app uv publish --user __token__ --password {API token}
    ```

You will need credentials (API Token) for this. Set one up in https://pypi.org/ as needed.
