# The Moose Configurator

The Moose Configurator.

- Manage Application Configurations in PyYaml.
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
