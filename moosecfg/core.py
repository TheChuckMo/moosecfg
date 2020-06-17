"""The Moose Configurator core."""
import json
import logging
import os

from moosecfg.util import MooseYamlSource, MooseConfiguratorSource

logger = logging.getLogger(__name__)

_UPDATE_AT_INIT: bool = os.getenv('MOOSECFG_UPDATE_AT_INIT', True)
_SYSTEM_OVERRIDE: bool = os.getenv('MOOSECFG_SYSTEM_OVERRIDE', False)
_LOCAL_FILE_LOAD: bool = os.getenv('MOOSECFG_LOCAL_FILE_LOAD', True)
_LOCAL_FILE_HIDDEN: bool = os.getenv('MOOSECFG_LOCAL_FILE_HIDDEN', True)

_SYSTEM_CFG_DIR: str = os.getenv('MOOSECFG_SYSTEM_CFG_DIR', os.path.abspath('/etc'))
_USER_CFG_DIR: str = os.getenv('XDG_CONFIG_HOME', os.path.join(os.path.expanduser('~'), '.config'))
_LOCAL_CFG_DIR: str = os.getenv('MOOSECFG_LOCAL_CFG_DIR', os.path.abspath(os.getcwd()))


class MooseConfigurator:
    """The Moose Configurator.

    Manage multiple configuration files.

    Examples
    --------

    cfg = MooseConfigurator('appname')

    cfg = MooseConfigurator(name='appname', extension='cfg', defaults={'server': 'test.example.com'})

    Attributes
    ----------
    name : str, default=__name__
        Application name.
    author : str, default=None
        Application author.
    version : str, default=None
        Application version.
    extension : str, default='yml'
        Extension for configuration filenames.
    defaults : dict, default=None
        Name/value pairs to set as defaults.
    """
    _name: str = __name__
    _author: str = None
    _version: str = None
    _extension: str = 'yml'
    _obj: dict = {}
    _defaults: dict = {}

    system: MooseYamlSource = None
    user: MooseYamlSource = None
    local: MooseYamlSource = None

    UPDATE_AT_INIT: bool = _UPDATE_AT_INIT
    """bool: Configuration updated from sources on init."""

    SYSTEM_OVERRIDE: bool = _SYSTEM_OVERRIDE
    """bool: System configuration source overrides all sources."""

    LOCAL_FILE_LOAD: bool = _LOCAL_FILE_LOAD
    """bool: Load local configuration if True."""

    LOCAL_FILE_HIDDEN: bool = _LOCAL_FILE_HIDDEN
    """bool: Seek hidden file for configuration."""

    SYSTEM_CFG_DIR: str = _SYSTEM_CFG_DIR
    """str: system configuration directory."""

    USER_CFG_DIR: str = _USER_CFG_DIR
    """str: user configuration directory."""

    LOCAL_CFG_DIR: str = _LOCAL_CFG_DIR
    """str: local configuration directory."""

    def __init__(self, name: str = None, author: str = None, version: str = None, extension: str = None,
                 defaults: dict = None):
        if name:
            self._name = name
            logger.info(f'name: {name}')

        if author:
            self._author = author
            logger.info(f'author: {author}')

        if version:
            self._version = version
            logger.info(f'version: {version}')

        if extension:
            self._extension = extension
            logger.info(f'extension: {extension}')

        if defaults:
            self._defaults = defaults
            self.update_from_defaults()
            logger.info(f'defaults: {defaults}')

        self._init_sources()
        """initialize sources."""

        self.read()
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
    def defaults(self) -> dict:
        """Configuration defaults."""
        return self._defaults

    def update_from_defaults(self) -> None:
        """Set configuration defaults."""
        for key in self.defaults.keys():
            self._obj_setdefault(key, self.defaults.get(key))

    @property
    def name(self) -> str:
        """Application name."""
        return self._name

    @property
    def author(self) -> str:
        """Application author. (information only)."""
        return self._author

    @property
    def version(self) -> str:
        """Application version. (information only)."""
        return self._version

    @property
    def extension(self) -> str:
        """Configuration file extension."""
        return self._extension

    @property
    def filename(self) -> str:
        """Configuration file name."""
        return f'{self.name}.{self.extension}'

    @property
    def system_full_path(self) -> str:
        """System Configuration file full path."""
        return os.path.abspath(os.path.join(self.SYSTEM_CFG_DIR, self.name, self.filename))

    @property
    def user_full_path(self) -> str:
        """User configuration file full path."""
        return os.path.abspath(os.path.join(self.USER_CFG_DIR, self.name, self.filename))

    @property
    def local_full_path(self) -> str:
        """Local configuration file full path."""
        _filename: str = self.filename
        if self.LOCAL_FILE_HIDDEN:
            _filename = f'.{_filename}'

        return os.path.abspath(os.path.join(self.LOCAL_CFG_DIR, _filename))

    def _init_sources(self) -> None:
        """Initialize sources."""
        self.system = MooseYamlSource(name='system', location=self.system_full_path)
        self.user = MooseYamlSource(name='user', location=self.user_full_path)
        self.local = MooseYamlSource(name='local', location=self.local_full_path)

    def update_from_source(self, source: MooseConfiguratorSource) -> None:
        """Apply source configuration."""
        self._obj_update(source.obj)
        logger.info(f'Configuration source {source.name} applied.')

    def read(self) -> None:
        """Read configuration sources."""
        if self.system.is_readable:
            self.system.read()

        if self.user.is_readable:
            self.user.read()

        if self.local.is_readable and self.LOCAL_FILE_LOAD:
            self.local.read()

        logger.info(f'configuration sources read.')

    def update(self) -> None:
        """Update configuration from sources."""
        self.update_from_source(source=self.system)
        self.update_from_source(source=self.user)
        self.update_from_source(source=self.local)

        if self.SYSTEM_OVERRIDE:
            self.update_from_source(source=self.system)

        logger.info(f'configuration updated from sources.')

    def write(self):
        """Write configuration sources."""
        if self.system.is_writable:
            self.system.write()

        if self.user.is_writable:
            self.user.write()

        if self.local.is_writable and self.LOCAL_FILE_LOAD:
            self.local.write()

        logger.info(f'configuration sources written.')

    # @property
    # def system_cfg(self) -> dict:
    #     """System configuration."""
    #     return self._system_cfg
    #
    # @property
    # def system_cfg_path(self) -> str:
    #     """System configuration path."""
    #     return os.path.join(self.SYSTEM_CFG_DIR, self.name)
    #
    # @property
    # def system_cfg_file(self) -> str:
    #     """System configuration file."""
    #     return os.path.join(self.SYSTEM_CFG_DIR, self.name, self.filename)
    #
    # def system_cfg_load(self) -> None:
    #     """Load system configuration."""
    #     self._system_cfg = self.load_cfg_file(file=self.system_cfg_file)
    #     logger.info(f'System configuration file {self.system_cfg_file} loaded.')
    #     logger.debug(f'system: {json.dumps(self.system_cfg)}')
    #
    # def system_cfg_update(self) -> None:
    #     """Update configuration from system."""
    #     self._obj_update(self.system_cfg)
    #     logger.info(f'Configuration updated from system.')
    #
    # @property
    # def user_cfg(self) -> dict:
    #     """User configuration."""
    #     return self._user_cfg
    #
    # @property
    # def user_cfg_path(self) -> str:
    #     """User configuration path."""
    #     return os.path.join(self.USER_CFG_DIR, self.name)
    #
    # @property
    # def user_cfg_file(self) -> str:
    #     """User configuration file."""
    #     return os.path.join(self.user_cfg_path, self.filename)
    #
    # def user_cfg_load(self) -> None:
    #     """Load user configuration."""
    #     self._user_cfg = self.load_cfg_file(file=self.user_cfg_file)
    #     logger.info(f'User configuration file {self.user_cfg_file} loaded.')
    #     logger.debug(f'user: {json.dumps(self.user_cfg)}')
    #
    # def user_cfg_update(self) -> None:
    #     """Update configuration from user."""
    #     self._obj_update(self.user_cfg)
    #     logger.info(f'Configuration updated from user.')
    #
    # @property
    # def local_cfg(self) -> dict:
    #     """Local configuration."""
    #     return self._local_cfg
    #
    # @property
    # def local_cfg_path(self) -> str:
    #     """Local configuration path."""
    #     return self.LOCAL_CFG_DIR
    #
    # @property
    # def local_cfg_file(self) -> str:
    #     """Local configuration file."""
    #     _filename: str = self.filename
    #     if self.LOCAL_FILE_HIDDEN:
    #         _filename = f'.{_filename}'
    #
    #     return os.path.join(self.local_cfg_path, f'{_filename}')
    #
    # def local_cfg_load(self) -> None:
    #     """Load local configuration."""
    #     self._local_cfg = self.load_cfg_file(file=self.local_cfg_file)
    #     logger.info(f'Local configuration file {self.local_cfg_file} loaded.')
    #     logger.debug(f'local: {json.dumps(self.local_cfg)}')
    #
    # def local_cfg_update(self) -> None:
    #     """Update configuration from local."""
    #     self._obj_update(self.local_cfg)
    #     logger.info(f'Configuration updated from local.')
    #
    # def read(self) -> None:
    #     """Read configuration sources."""
    #     self.system = MooseYamlSource(name='system', source=self.system_source)
    #     self.system.read()
    #
    #     self.user = MooseYamlSource(name='user', source=self.user_source)
    #     self.user.read()
    #
    #     self.local = MooseYamlSource(name='local', source=self.local_source)
    #     if self.LOCAL_FILE_LOAD:
    #         self.local.read()
    #     logger.info(f'configuration sources read.')
    #
    # def apply(self) -> None:
    #     """Apply configuration sources."""
    #     self.apply_source_cfg(source=self.system)
    #     self.apply_source_cfg(source=self.user)
    #     self.apply_source_cfg(source=self.local)
    #
    #     if self.SYSTEM_OVERRIDE:
    #         self.apply_source_cfg(source=self.system)
    #
    #     logger.info(f'configuration updated.')

    # @staticmethod
    # def load_cfg_file(file: str = None) -> dict:
    #     """Load a configuration file."""
    #     _data: dict = {}
    #     if os.path.isfile(file):
    #         with open(file, 'r') as fh:
    #             _data = yaml.safe_load(fh.read())
    #     return _data
