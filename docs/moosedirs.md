# Moose Directories

XDG standards based directory locations.

## Usage

```python
import os
from moosecfg.utils import MooseDirs

dirs = MooseDirs(name="app")

data_file = f'{os.path.join(dirs.user_data, "app.dat")}'

print(data_file)
```

`/home/user/.local/share/app/app.dat`

## MooseDirs directories

MooseDirs               | XDG                | Directory
:-----                  | :-:                | :------
obj.system_config (str) | XDG_CONFIG_DIRS[0] | `/etc/app`
obj.system_data (str)   | XDG_DATA_DIRS[0]   | `/var/run/app`
obj.system_cache (str)  | -                  | `/tmp/app`
obj.user_home (str)     | -                  | `$HOME`
obj.user_config (str)   | XDG_CONFIG_HOME    | `$HOME/.config/app`
obj.user_data (str)     | XDG_DATA_HOME      | `$HOME/.local/share/app`
obj.user_cache (str)    | XDG_CACHE_HOME     | `$HOME/.cache/app`
obj.local_config (str)  | -                  | `<cwd>`
obj.local_data (str)    | -                  | `<cwd>/data`
obj.local_cache (str)   | -                  | `<cwd>/.cache`
obj.config_dirs (list)  | XDG_CONFIG_DIRS    | `$HOME/.config,/etc/xdg`
obj.data_dirs (list)    | XDG_DATA_DIRS      | `$HOME/.local/share,/usr/local/share,/usr/share`

## Override

Base directory locations can be altered before creation of the object.

```python
import os
from moosecfg.utils import MooseDirs

MooseDirs.system_config = "/opt"
MooseDirs.user_data = "/data"

dirs = MooseDirs(name="app")

syscfg_file = f'{os.path.join(dirs.system_config, "app.cfg")}'
data_file = f'{os.path.join(dirs.user_data, "app.dat")}'

print(syscfg_file)

print(data_file)
```

`/opt/app/app.cfg`

`/data/app/app.dat`
