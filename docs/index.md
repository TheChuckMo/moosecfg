# The Moose Configurator

A python application configuration manager.

## Features

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

## Quick Start

1. Install moosecfg
    - global: `python -m pip install moosecfg`
    - user: `python -m pip install --user moosecfg`
2. Create yaml configuration files
    - system: `/etc/appname/appname.cfg`
    - user: `$HOME/.config/appname/appname.cfg`
    - local: `<cwd>/appname.cfg`
3. Read the configuration

    ```
    cfg = MooseConfigurator('appname')
    print(f'configuration object: {cfg.obj}')
    ```


## Usage

```python
from moosecfg.config import MooseConfigurator

MooseConfigurator.SYSTEM_OVERRIDE = True

cfg = MooseConfigurator('coolapp')

server = cfg.obj.get('servername')
proxy = cfg.obj.get('proxy')
ptqmax = cfg.obj.get('ptq_max')

...
```