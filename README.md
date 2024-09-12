# TanX - Precommit-hooks

Some out-of-the-box hooks for pre-commit.`<br>`
See also: https://github.com/pre-commit/pre-commit

## Steps to import and use pre-commit-hooks:

1. Create `.pre-commit-config.yaml` in the root directory
2. Select the hooks to use, as shown below

```python
repos:
  - repo: https://github.com/tanx-libs/precommit-hooks
    hooks:
      - id: private_key_check # Checks for private keys
      - id: docker-compose-validate # Docker compose file validator
      - id: hadolint-dockerfile-lint # Dockerfile lint 
      - id: json-lint # Json file lint
      - id: yamllint # Yaml file lint

```

3. Run `pre-commit install` in the root directory 

Now with every new commit, staged files would be checked `<br>`
to run the hook throughout the existing codebase, run `pre-commit run --all-files` to check manually.

## Hooks available

### Private keys detector - `id: private_key_check`

- Check for any private keys in the staged files `<br>`
- detects private keys of length `[64,66]`
- private keys can also begin with `0x`,`<br>`
- to skip the checks for a line, use ` # noqa:keycheck`
- Check if the file starts with "# noqa:keycheck-file" or "// noqa:keycheck-file"

```python
PRIVATE_ADDRESS="1a4b0778f...e99fc33fff87c821829" # noqa:keycheck
```

```js
PRIVATE_ADDRESS="1a4b0778f...e99fc33fff87c821829" // noqa:keycheck
```

script - `pre_commit_hooks/private_key_check.py`


### Docker Compose Validator - `id: docker-compose-validate`

- Validates all staged docker compose files using either `docker compose` or `docker-compose`. 

script - `pre_commit_hooks/run_validate_docker_compose.py`

### Hadolint - Dockerfile lint - `id: hadolint-dockerfile-lint`

- Hadolint lints all staged dockerfile, for reference `pre_commit_hooks/config/.hadolint.yaml` consists of all the warning / error codes wit h description.
- Runs linter for staged Dockerfile's

script - `pre_commit_hooks/run_hadolint.py`

### Json Lint - `id: json-lint`

- Json Lint lints all staged json files using `jq`.
- Make sure you have jq installed on your system, if not then install it using

```bash
sudo apt install jq -y
```

script - `pre_commit_hooks/run_json_linter.py`

### Yaml Lint - `id: yamllint`

- yamllint lints all the staged files 

script - `pre_commit_hooks/run_yamllint.py`

- If you are using any kind of templating like this, especially for docker make sure it is in a string format.

- Incorrect Format
```yaml
image: {IMAGE-1-NAME}:{IMAGE-1-TAG}
```

- Correct Format
```yaml
image: "{IMAGE-1-NAME}:{IMAGE-1-TAG}"
```