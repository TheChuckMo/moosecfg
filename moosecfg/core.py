"""Moose Config core."""
import logging
import os

import yaml
import json

logger = logging.getLogger(__name__)

_MOOSE_CFG_FILE_EXTENSION: str = 'yml'
_MOOSE_SYSTEM_OVERRIDE: bool = False
_MOOSE_LOAD_LOCAL_CFG: bool = True
_MOOSE_UPDATE_AT_INIT: bool = False


class MooseConfigurator:
    """The Moose Configurator."""
    _name: str = __name__
    _extension: str = _MOOSE_CFG_FILE_EXTENSION

    _defaults: dict = {}
    _system_cfg: dict = {}
    _user_cfg: dict = {}
    _local_cfg: dict = {}

    _obj: dict = {}

    # System configuration overrides user and local if True.
    SYSTEM_OVERRIDE: bool = _MOOSE_SYSTEM_OVERRIDE

    # Load local configuration if True.
    LOAD_LOCAL_CFG: bool = _MOOSE_LOAD_LOCAL_CFG

    # Configuration updated on init if True.
    UPDATE_AT_INIT: bool = _MOOSE_UPDATE_AT_INIT

    def __init__(self, name: str = None, extension: str = None, defaults: dict = None):
        if name:
            self._name = name
        logger.info(f'name: {name}')

        if extension:
            self._extension = extension
        logger.info(f'extension: {extension}')

        if defaults:
            self._defaults = defaults
        logger.info(f'defaults: {defaults}')

        # load configuration files
        self.load()
        logger.info(f'configuration files loaded.')

        if self.UPDATE_AT_INIT:
            self.update()
            logger.debug(f'configuration: {json.dumps(self.obj)}')
            logger.info(f'configuration updated.')

    @property
    def obj(self) -> dict:
        """The configuration object."""
        return self._obj

    def _obj_update(self, obj: dict, **kwargs) -> None:
        """Update configuration object."""
        self._obj.update(obj, **kwargs)
        logger.info(f'Configuration object updated.')
        logger.debug(f'update obj: {json.dumps(obj)}')

    def _obj_setdefault(self, key: str, value: str = None):
        """Set configuration default."""
        self._obj.setdefault(key, value)
        logger.info(f'Configuration default set.')
        logger.debug(f'default key: {key}')
        logger.debug(f'default value: {value}')

    @property
    def name(self) -> str:
        """Configuration name."""
        return self._name

    @property
    def extension(self) -> str:
        """Configuration file extension."""
        return self._extension

    @property
    def file_name(self) -> str:
        """Configuration file name."""
        return f'{self.name}.{self.extension}'

    @property
    def system_cfg(self) -> dict:
        """System configuration."""
        return self._system_cfg

    @property
    def system_cfg_path(self) -> str:
        """System configuration path."""
        return os.path.abspath(f'/etc/{self.name}')

    @property
    def system_cfg_file(self) -> str:
        """System configuration file."""
        return os.path.join(self.system_cfg_path, self.file_name)

    def system_cfg_load(self) -> None:
        """Load system configuration."""
        self._system_cfg = self.load_cfg_file(file=self.system_cfg_file)
        logger.info(f'System configuration file {self.system_cfg_file} loaded.')
        logger.debug(f'system: {json.dumps(self.system_cfg)}')

    def system_cfg_update(self) -> None:
        """Update configuration from system."""
        self._obj_update(self.system_cfg)
        logger.info(f'Configuration updated from system.')

    @property
    def user_cfg(self):
        """User configuration."""
        return self._user_cfg

    @property
    def user_cfg_path(self) -> str:
        """User configuration path."""
        return os.path.abspath(os.path.join(os.path.expanduser('~/.config'), self.name))

    @property
    def user_cfg_file(self) -> str:
        """User configuration file."""
        return os.path.join(self.user_cfg_path, self.file_name)

    def user_cfg_load(self) -> None:
        """Load user configuration."""
        self._user_cfg = self.load_cfg_file(file=self.user_cfg_file)
        logger.info(f'User configuration file {self.user_cfg_file} loaded.')
        logger.debug(f'user: {json.dumps(self.user_cfg)}')

    def user_cfg_update(self) -> None:
        """Update configuration from user."""
        self._obj_update(self.user_cfg)
        logger.info(f'Configuration updated from user.')

    @property
    def local_cfg(self) -> dict:
        """Local configuration."""
        return self._local_cfg
    
    @property
    def local_cfg_path(self) -> str:
        """Local configuration path."""
        return os.path.abspath(os.getcwd())

    @property
    def local_cfg_file(self) -> str:
        """Local configuration file."""
        return os.path.join(self.local_cfg_path, f'.{self.file_name}')

    def local_cfg_load(self) -> None:
        """Load local configuration."""
        self._local_cfg = self.load_cfg_file(file=self.local_cfg_file)
        logger.info(f'Local configuration file {self.local_cfg_file} loaded.')
        logger.debug(f'local: {json.dumps(self.local_cfg)}')

    def local_cfg_update(self) -> None:
        """Update configuration from local."""
        self._obj_update(self.local_cfg)
        logger.info(f'Configuration updated from local.')

    def load(self) -> None:
        """Load configuration files."""
        self.system_cfg_load()

        self.user_cfg_load()

        if self.LOAD_LOCAL_CFG:
            self.local_cfg_load()
            
        logger.info(f'configuration loaded.')

    def update(self) -> None:
        """Update configuration object."""
        self.system_cfg_update()

        self.user_cfg_update()
        self.local_cfg_update()

        if self.SYSTEM_OVERRIDE:
            self.system_cfg_update()
            
        logger.info(f'configuration updated.')

    @staticmethod
    def load_cfg_file(file: str = None) -> dict:
        """Load a configuration file."""
        _data: dict = {}
        if os.path.isfile(file):
            with open(file, 'r') as fh:
                _data = yaml.safe_load(fh.read())
        return _data

