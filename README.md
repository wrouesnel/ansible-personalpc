# Ansible Personal PC

This is my personal PC setup and homogenization library.

## New Workstation Deployment Process

New Workstations consist of a bare Ubuntu Install running Cinnamon.

Before the first run, copy `inventory/group_vars/all/local.yml.example` to
`local.yml` in the same directory and fill in the settings for this machine
(GitHub token, desktop environment, network domain...). `local.yml` is
git-ignored; keep secrets and internal names there.

The desktop environment is chosen by the `desktop_environment` variable
(default `cinnamon`, also `mate`) - set it in `local.yml` or with
`-e desktop_environment=mate`.

## Commit hooks

Run `./autogen.sh` to install the git hooks. The pre-commit hook scans staged
changes with [gitleaks](https://github.com/gitleaks/gitleaks), which
`gitleaks.yml` installs.

## Usage

This library is now based on `uv`.