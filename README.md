# Ansible Personal PC

This is my personal PC setup and homogenization library.

## New Workstation Deployment Process

New Workstations consist of a bare Ubuntu Install running Cinnamon.

The desktop environment is chosen by the `desktop_environment` variable
(default `cinnamon`, also `mate`) - set it in `inventory/group_vars/all/local.yml`
or with `-e desktop_environment=mate`.

## Usage

This library is now based on `uv`.