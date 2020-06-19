"""The Moose Configurator utilities."""

import os
import yaml
import json
import logging
from urllib.request import Request
from urllib.request import urlopen

logger = logging.getLogger()


class MooseConfiguratorSource:
    """Moose Configurator source base class.

    src = MooseConfiguratorSource(name="system", location="/etc/appname/appname.cfg")

    Parameters
    ----------
    name : str
    location : str
    """
    obj: dict = {}
    meta: dict = {}
    _name: str = None
    _location: str = None

    def __init__(self, name: str, location: str):
        self._name = name
        self._location = location

    def __repr__(self):
        return f'{self.__class__.__name__}(name="{self.name}", location="{self.location}")'

    def __str__(self):
        return f'{self.name}'

    @property
    def name(self) -> str:
        """str: Source name."""
        return self._name

    @property
    def location(self) -> str:
        """str: Source file."""
        return self._location

    @property
    def is_readable(self) -> bool:
        """bool: source is readable."""
        return True

    @property
    def is_writable(self) -> bool:
        """bool: source is writable."""
        return False

    def read(self) -> None:
        """Read from source."""
        pass

    def write(self) -> None:
        """Write to source."""
        pass


class MooseHttpYamlSource(MooseConfiguratorSource):
    """Moose Configurator HTTP yaml source file."""

    def read(self) -> None:
        """Read configuration file."""
        _data: dict = {}
        with urlopen(self.location) as _res:
            if _res.status is 'OK':
                _data = yaml.safe_load(_res.read())
        self.obj = _data.copy()
        logger.info(f'{self.name} source {self.location} read.')

    @property
    def is_readable(self) -> bool:
        """bool: source is readable."""
        _readable: bool = False
        with urlopen(Request(self.location, method='HEAD')) as _res:
            if _res.status is 'OK':
                _readable = True
        return _readable


class MooseHttpJsonSource(MooseConfiguratorSource):
    """Moose Configurator HTTP json source file."""
    _headers: dict = { 'CONTENT-TYPE': 'application/json' }

    def read(self) -> None:
        """Read json configuration from http."""
        _data: dict = {}
        with urlopen(Request(self.location, headers=self._headers)) as _res:
            _data = json.load(_res.read())
        self.obj = _data.copy()
        logger.info(f'{self.name} source {self.location} read.')

    @property
    def is_readable(self) -> bool:
        """bool: source is readable."""
        _readable: bool = False
        with urlopen(Request(self.location, headers=self._headers, method='HEAD')) as _res:
            if _res.status is 'OK':
                _readable = True
        return _readable


class MooseYamlSource(MooseConfiguratorSource):
    """Moose Configurator yaml source from file.

    src = MooseYamlSource(name="system", location="/etc/appname/appname.cfg")

    Parameters
    ----------
    name : str
    location : str
    """
    @property
    def is_readable(self) -> bool:
        """bool: source is readable."""
        _resp: bool = False
        if os.path.exists(self.location):
            if os.path.isfile(self.location):
                if os.access(self.location, os.R_OK):
                    _resp = True
        return _resp

    @property
    def is_writable(self) -> bool:
        """bool: source is readable."""
        _resp: bool = False
        if os.path.exists(self.location):
            if os.path.isfile(self.location):
                if os.access(self.location, os.W_OK):
                    _resp = True
        return _resp

    def read(self) -> None:
        """Read yaml configuration file."""
        _data: dict = {}
        if os.path.isfile(self.location):
            with open(self.location, 'r') as fh:
                _data = yaml.safe_load(fh.read())
        # TODO find, set, and remove moose configurator metadata from import.
        self.obj = _data.copy()
        logger.info(f'{self.name} source file {self.location} read.')

    def write(self) -> None:
        """Write yaml configuration file."""
        _dir: str = os.path.dirname(self.location)
        if not os.path.isdir(_dir):
            os.mkdir(_dir)
            logger.info(f'directory {_dir} created.')

        _data: dict = self.obj.copy()
        _data.update(self.meta)
        with open(self.location, 'w') as fh:
            fh.write(yaml.safe_dump(_data))
            logger.info(f'{self.name} source file {self.location} written.')
