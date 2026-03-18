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
    docker compose run --rm app uv publish --index testpypi --username __token__ --password {API token}
    ```

You will need credentials (API Token) for this. Set one up in https://test.pypi.org/ as needed.

#### Publish from GitHub Action
A publish to **TestPyPI** can also be done by pushing a tag up to a PR:
- Create a `vX.Y.Z` tag (dev versions are OK e.g. `vX.Y.Z.devN`) on the PR branch.
- Push it up. Example:
  ```
  git tag v1.2.0.dev0
  git push origin v1.2.0.dev0
  ```


### PyPI
- Double-check **version** in `pyproject.toml`. Rebuild if necessary (see above).
- Run:
    ```
    docker compose run --rm app uv publish --username __token__ --password {API token}
    ```

You will need credentials (API Token) for this. Set one up in https://pypi.org/ as needed.

#### Publish from GitHub Release
- Do whatever it takes to get production-quality changes into the branch `master`.
- Make sure `pyproject.toml`'s version is set to a valid semantic version (e.g. `X.Y.Z`).
  - Test using `.devN` release as needed.
  - Use manual publishes as described above for testing.
- Create a [Release](https://github.com/bluedenim/vmigration-helper/releases) using GitHub UI.
  - Use a tag of the format `vX.Y.Z`
  - Set it as latest release.
- Monitor status under the [Deployments](https://github.com/bluedenim/vmigration-helper/deployments).