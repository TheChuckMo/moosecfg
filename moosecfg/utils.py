"""Moose Configurator Utilities."""

import os

from xdg.BaseDirectory import (xdg_config_home, xdg_data_home, xdg_cache_home, xdg_data_dirs, xdg_config_dirs)

import logging

logger = logging.getLogger()

_ENV_PRE: str = 'MOOSECFG'
_CWD: str = os.path.abspath(os.getcwd())
_SYSTEM_CONFIG: str = os.path.abspath('/etc')
_SYSTEM_DATA: str = os.path.abspath('/var/run')
_SYSTEM_CACHE: str = os.path.abspath('/tmp')


class MooseDirs:
    """Moose Configurator dirs."""
    name: str = None
    """Name of the application."""

    environment: str = None
    """Environment of application."""

    version: str = None
    """Version of application."""

    system_config: str = os.getenv(f'{_ENV_PRE}_SYSTEM_CONFIG', _SYSTEM_CONFIG)
    """System configuration directory for application."""

    system_data: str = os.getenv(f'{_ENV_PRE}_SYSTEM_DATA', _SYSTEM_DATA)
    """System data directory for application."""

    system_cache: str = os.getenv(f'{_ENV_PRE}_SYSTEM_CACHE', _SYSTEM_CACHE)
    """System cache directory for application."""

    user_home: str = os.path.expanduser('~')
    """User home directory"""

    user_config: str = os.getenv(f'{_ENV_PRE}_USER_CONFIG', xdg_config_home)
    """User configuration directory."""

    user_data: str = os.getenv(f'{_ENV_PRE}_USER_DATA', xdg_data_home)
    """User data directory."""

    user_cache: str = os.getenv(f'{_ENV_PRE}_USER_CACHE', xdg_cache_home)
    """User cache directory."""

    local_config: str = os.getenv(f'{_ENV_PRE}_LOCAL_CONFIG', _CWD)
    """Local configuration directory."""

    local_data: str = os.getenv(f'{_ENV_PRE}_LOCAL_DATA', os.path.join(_CWD, 'data'))
    """Local data directory."""

    local_cache: str = os.getenv(f'{_ENV_PRE}_LOCAL_CACHE', os.path.join(_CWD, '.cache'))
    """Local cache directory."""

    config_dirs: list = xdg_config_dirs
    """Alternative configuration directories."""

    data_dirs: list = xdg_data_dirs
    """Alternative configuration directories."""

    def __init__(self, name: str = None, environment: str = None, version: str = None):
        """Moose Dir init."""
        if name:
            self.append_to_user_dirs(name)
            self.append_to_system_dirs(name)

        if environment:
            self.append_to_user_dirs(environment)
            self.append_to_system_dirs(environment)

        if version:
            self.append_to_user_dirs(version)

    def append_to_system_dirs(self, item: str):
        """Append dir to system dirs."""
        self.system_config = os.path.join(self.system_config, item)
        self.system_data = os.path.join(self.system_data, item)
        self.system_cache = os.path.join(self.system_cache, item)

    def append_to_user_dirs(self, item: str):
        """Append dir to user dirs."""
        self.user_config = os.path.join(self.user_config, item)
        self.user_data = os.path.join(self.user_data, item)
        self.user_cache = os.path.join(self.user_cache, item)
