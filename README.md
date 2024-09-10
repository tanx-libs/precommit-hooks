# TanX - Precommit-hooks

Some out-of-the-box hooks for pre-commit.`<br>`
See also: https://github.com/pre-commit/pre-commit

## Steps to import and use pre-commit-hooks:

1. Create `.pre-commit-config.yaml` in the root directory
2. Select the hooks to use, as shown below

```python
repos:
  - repo: https://github.com/tanx-libs/precommit-hooks
    rev: v1.0.1  # please check the latest release, under releases
    hooks:
      - id: private_key_check # checkout all hooks under .pre-commit-hooks.yaml

```

3. Run `pre-commit install` in the root directory

Now with every new commit, staged files would be checked `<br>`
to run the hook throughout the exixting codebase, run `pre-commit run --all-files`

## Hooks available

### Private keys detector - `id: private_key_check`

- Check for any private keys in the staged files `<br>`
- detects private keys of length `[64,66]`
- private keys can also begin with `0x`,`<br>`
- to skip the checks for a line, use ` # noqa:keycheck`

```python
PRIVATE_ADDRESS="1a4b0778f...e99fc33fff87c821829" # noqa:keycheck
```

script - `pre_commit_hooks/private_key_check.py`

### Docker Compose Validator

- Validates all staged docker compose files.

### Hadolint - Dockerfile lint

- Runs linter for staged Dockerfile's
- Use the given production hadolint config file `.hadolint.yaml`.
- Use the following script to run `dockerfile` linting for the staged files, also make sure that name of this script is `./scripts/run_hadolint.sh` , because that is what we have used in the .`pre-commit-config.yaml`

### Json Lint

- Make sure you have jq installed on your system, if not then install it using 

```bash
sudo apt install jq -y
```

### Yaml Lint

- Make sure you have `yamllint` installed in your virtual environment, by default the environment location is `.venv`.
- If you have your virtual environment installed elsewhere then modify that location in pre-commit config file and run_yamllint.sh script.
- yamllint requires `.yamllint.yaml` configuration file to run linterm you can find the reference for that in the repository.