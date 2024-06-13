# TanX - Precommit-hooks
Some out-of-the-box hooks for pre-commit.<br>
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
3. Run `pre-commit install` in th root directory

Now with every new commit, staged files would be checked <br>
to run the hook throughout the exixting codebase, run `pre-commit run --all-files`

## Hooks available
### Private keys detector - `id: private_key_check`
 - Check for any private keys in the staged files <br>
 - detects private keys of length `[64,66]`
 - private keys can also begin with `0x`,<br>
 - to skip the checks for a line, use ` # noqa:keycheck`
```python
PRIVATE_ADDRESS="1a4b0778f...e99fc33fff87c821829" # noqa:keycheck
```
script - `pre_commit_hooks/private_key_check.py`
