# OS Config Locations

Uses XDG Spec for everything.

## Free Desktop Spec

$XDG_CONFIG_HOME -default- $HOME/.config
    User configuration directory.

$XDG_CONFIG_DIRS -default- /etc
    Prioritized list of directories to search for config files.

$XDG_DATA_HOME -default- $HOME/.local/share
    User data directory.

$XDG_DATA_DIRS -default- /usr/local/share/:/usr/share/
    Prioritized list of directories to search for data files in.

$XDG_CACHE_HOME -default- $HOME/.cache
    Non-essential user data storage.

$XDG_RUNTIME_DIR -default- None

## Windows

%APPDATA%\appname - user config directory
