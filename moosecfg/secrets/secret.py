"""Moose config secrets manager."""

import yaml

from moosecfg.secrets.base import MooseSecretBase
from moosecfg.secrets.sources import MooseSecretSourceLocal, MooseSecretSourceFile


class MooseSecret(MooseSecretBase, yaml.YAMLObject):
    """Moose config secrets manager class"""
    yaml_tag = u'!MSecret'

    sources: dict = {'local': MooseSecretSourceLocal(), 'file': MooseSecretSourceFile()}

    def __init__(self, key: str, source: str = 'local'):
        self._key = key
        self._source = source

    def __repr__(self):
        if self._source is not 'local':
            return f'{self.__class__.__name__}(key={self.key}, source={self.source})'
        else:
            return f'{self.__class__.__name__}(key={self.key})'

    @property
    def key(self):
        """secret key."""
        return self._key

    @property
    def source(self):
        """source of secret."""
        return self._source

    @property
    def value(self):
        """content of secret."""
        obj = getattr(self.source, self.sources)
        return obj.read(self.key)
