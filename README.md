# The Moose Configurator

## QuickStart

`python -m pip install --user moosecfg`

## Features

- Yaml based configuration files.
- Set defaults for missing configuration items.
- Three levels of configuration.
  - System: /etc/sample/sample.yml
  - User: ~/.config/sample/sample.yml
  - Local: `cwd`
- Configuration load and read customization.
  - Force system configuration override.
  - Ignore local configuration.
  - User hidden local configuration (dot-file).
- XDG specification directory locations.
