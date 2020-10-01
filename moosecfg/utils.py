"""Moose Configurator Utilities."""

import os

from xdg.BaseDirectory import (xdg_config_home, xdg_data_home, xdg_cache_home, xdg_data_dirs, xdg_config_dirs)

import logging

logger = logging.getLogger()

_ENV_PRE: str = 'MOOSE'
_CWD: str = os.path.abspath(os.getcwd())
_SYSTEM_CONFIG: str = os.path.abspath('/etc')
_SYSTEM_DATA: str = os.path.abspath('/var/run')
_SYSTEM_CACHE: str = os.path.abspath('/tmp')


class MooseDirs:
    """Moose Locations."""
    __slots__ = ['name', 'append']
    _joins: list = []

    config_ext: str = 'cfg'
    data_ext: str = 'db'
    cache_ext: str = 'cache'
    local_hidden: bool = True

    _system_config: str = os.getenv(f'{_ENV_PRE}_SYSTEM_CONFIG', _SYSTEM_CONFIG)
    """System configuration location for application."""

    _system_data: str = os.getenv(f'{_ENV_PRE}_SYSTEM_DATA', _SYSTEM_DATA)
    """System data location for application."""

    _system_cache: str = os.getenv(f'{_ENV_PRE}_SYSTEM_CACHE', _SYSTEM_CACHE)
    """System cache location for application."""

    user_home: str = os.path.expanduser('~')
    """User home location."""

    _user_config: str = os.getenv(f'{_ENV_PRE}_USER_CONFIG', xdg_config_home)
    """User configuration location."""

    _user_data: str = os.getenv(f'{_ENV_PRE}_USER_DATA', xdg_data_home)
    """User data location."""

    _user_cache: str = os.getenv(f'{_ENV_PRE}_USER_CACHE', xdg_cache_home)
    """User cache location."""

    local_config: str = os.getenv(f'{_ENV_PRE}_LOCAL_CONFIG', _CWD)
    """Local configuration location."""

    local_data: str = os.getenv(f'{_ENV_PRE}_LOCAL_DATA', os.path.join(_CWD, 'data'))
    """Local data location."""

    local_cache: str = os.getenv(f'{_ENV_PRE}_LOCAL_CACHE', os.path.join(_CWD, '.cache'))
    """Local cache location."""

    config_dirs: list = xdg_config_dirs
    """Alternative config locations."""

    data_dirs: list = xdg_data_dirs
    """Alternative data locations."""

    def __init__(self, name: str, append: [str, list] = None):
        """Moose Dir init."""
        self.name = name
        self._joins.append(name)

        if append:
            self._joins.append(append)

    def _join(self, location) -> str:
        """Join location."""
        for _join in self._joins:
            location = os.path.join(location, _join)

        return location

    @property
    def system_config(self) -> str:
        """System config location."""
        return self._join(self._system_config)

    @property
    def system_config_file(self) -> str:
        """System config file."""
        return os.path.join(self.system_config, f'{self.name}.{self.config_ext}')

    @property
    def system_data(self) -> str:
        """System data location."""
        return self._join(self._system_data)

    @property
    def system_data_file(self) -> str:
        """System data file."""
        return os.path.join(self.system_data, f'{self.name}.{self.data_ext}')

    @property
    def system_cache(self) -> str:
        """System cache location."""
        return self._join(self._system_cache)

    @property
    def system_cache_file(self) -> str:
        """System cache file."""
        return os.path.join(self.system_cache, f'{self.name}.{self.cache_ext}')

    @property
    def user_config(self) -> str:
        """User config location."""
        return self._join(self._user_config)

    @property
    def user_config_file(self) -> str:
        """User config file."""
        return os.path.join(self.user_config, f'{self.name}.{self.config_ext}')

    @property
    def user_data(self) -> str:
        """User data location."""
        return self._join(self._user_data)

    @property
    def user_data_file(self) -> str:
        """User data file."""
        return os.path.join(self.user_data, f'{self.name}.{self.data_ext}')

    @property
    def user_cache(self) -> str:
        """User cache location."""
        return self._join(self._user_cache)

    @property
    def user_cache_file(self) -> str:
        """User cache file."""
        return os.path.join(self.user_cache, f'{self.name}.{self.cache_ext}')

    @property
    def local_config_file(self) -> str:
        """Local config file."""
        _filename: str = f'{self.name}.{self.config_ext}'
        if self.local_hidden:
            _filename = f'.{_filename}'

        return os.path.join(self.local_config, _filename)

    @property
    def local_data_file(self) -> str:
        """Local data file."""
        return os.path.join(self.local_data, f'{self.name}.{self.data_ext}')

    @property
    def local_cache_file(self) -> str:
        """Local cache file."""
        return os.path.join(self.local_cache, f'{self.name}.{self.cache_ext}')

