"""The Moose Configurator core."""
import json
import logging
import os

from moosecfg.utils import MooseDirs, _ENV_PRE
from moosecfg.sources import MooseYamlSource, MooseConfiguratorSource

logger = logging.getLogger()


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
    environment : str, default=None
        Application environment.
    version : str, default=None
        Application version.
    extension : str, default='cfg'
        Extension for configuration filenames.
    defaults : dict, default=None
        Name/value pairs to set as defaults.
    """
    _name: str = __name__
    _environment: str = None
    _version: str = None
    _extension: str = os.getenv(f'{_ENV_PRE}_EXTENSION', 'cfg')
    _obj: dict = {}
    _defaults: dict = {}

    dirs: MooseDirs = MooseDirs()
    """MooseDirs: directories for system and user locations."""

    sources: dict = {
        'system': [MooseYamlSource],
        'user': [MooseYamlSource],
        'local': [MooseYamlSource]
    }
    """Configurator sources config."""

    system: MooseConfiguratorSource = None
    """MooseConfiguratorSource: System configuration source."""

    user: MooseConfiguratorSource = None
    """MooseConfiguratorSource: User configuration source."""

    local: MooseConfiguratorSource = None
    """MooseConfiguratorSource: Local configuration source."""

    UPDATE_CFG_AT_INIT: bool = os.getenv(f'{_ENV_PRE}_UPDATE_CFG_AT_INIT', True)
    """bool: Configuration updated from sources on init."""

    UPDATE_DIRS_AT_INIT: bool = os.getenv(f'{_ENV_PRE}_UPDATE_DIRS_AT_INIT', True)
    """bool: Append app information to dirs."""

    SYSTEM_OVERRIDE: bool = os.getenv(f'{_ENV_PRE}_SYSTEM_OVERRIDE', False)
    """bool: System configuration source overrides all sources."""

    LOCAL_FILE_READ: bool = os.getenv(f'{_ENV_PRE}_LOCAL_FILE_READ', True)
    """bool: Read local configuration if True."""

    LOCAL_FILE_HIDDEN: bool = os.getenv(f'{_ENV_PRE}_LOCAL_FILE_HIDDEN', True)
    """bool: Seek hidden file for configuration."""

    def __init__(self, name: str = None, environment: str = None, version: str = None, extension: str = None,
                 defaults: dict = None):
        if name:
            self._name = name
            logger.info(f'name: {name}')

        if environment:
            self._environment = environment
            logger.info(f'environment: {environment}')

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

        if self.UPDATE_DIRS_AT_INIT:
            self._init_dirs()
            logger.info(f'initialized dirs objects.')

        self._init_sources()
        """initialize sources."""
        logger.info(f'initialized configuration sources.')

        self.read()
        """read source configurations."""
        logger.info(f'configuration files loaded.')

        if self.UPDATE_CFG_AT_INIT:
            self.update()
            """update configuration object from sources."""
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
    def environment(self) -> str:
        """Application environment."""
        return self._environment

    @property
    def version(self) -> str:
        """Application version."""
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
    def system_location(self) -> str:
        """System Configuration file full path."""
        _location: str = os.path.abspath(os.path.join(self.dirs.system_config, self.filename))
        if len(self.sources.get('system')) > 1:
            _location = self.sources.get('system')[1]
        return _location

    @property
    def user_location(self) -> str:
        """User configuration file full path."""
        return os.path.abspath(os.path.join(self.dirs.user_config, self.filename))

    @property
    def local_location(self) -> str:
        """Local configuration file full path."""
        _filename: str = self.filename
        if self.LOCAL_FILE_HIDDEN:
            _filename = f'.{_filename}'

        return os.path.abspath(os.path.join(self.dirs.local_config, _filename))

    def _init_dirs(self) -> None:
        """Initialize MooseDirs."""
        self.dirs = MooseDirs(name=self.name, environment=self.environment, version=self.version)

    def _init_system_source(self) -> None:
        """Initialize system configuration source."""
        self.system = self.sources.get('system')[0](name='system', location=self.system_location)

    def _init_user_source(self) -> None:
        """Initialize user configuration source."""
        self.user = self.sources.get('user')[0](name='user', location=self.user_location)

    def _init_local_source(self) -> None:
        """Initialize local configuration source."""
        self.local = self.sources.get('local')[0](name='local', location=self.local_location)

    def _init_sources(self) -> None:
        """Initialize sources."""
        self._init_system_source()
        self._init_user_source()
        self._init_local_source()

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

        if self.local.is_readable and self.LOCAL_FILE_READ:
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

    def write(self) -> None:
        """Write configuration sources."""
        if self.system.is_writable:
            self.system.write()

        if self.user.is_writable:
            self.user.write()

        if self.local.is_writable and self.LOCAL_FILE_READ:
            self.local.write()

        logger.info(f'configuration sources written.')

