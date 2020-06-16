import os

import yaml

from moosecfg.secrets.base import MooseSecretSourceBase


class MooseSecretSourceFile(MooseSecretSourceBase):
    """read secrets from file source."""
    _source = 'file'

    def read(self, key: str) -> object:
        """read secret from file."""
        _value = False
        if os.path.isfile(key):
            with os.open(key, 'r') as fh:
                _value = yaml.safe_dump(fh.read())

        return _value


class MooseSecretSourceLocal(MooseSecretSourceBase):
    """Moose secret local source."""
    _source = 'local'
    _secrets_file: str = os.path.join(os.getcwd(), '.moose_secrets.yml')
    _secrets_db: dict

    def __init__(self, file: str = None):
        if file:
            self._secrets_file = file

        self.load_secrets_file()

    @property
    def keys(self):
        """local secret keys."""
        return self._secrets_db.keys()

    def read(self, key: str) -> object:
        """read a local secret."""
        return self._secrets_db.get(key, False)

    def create(self, key: str, value: str, update: bool = False) -> bool:
        """create a local secret."""
        if key in self._secrets_db and not update:
            return False

        self._secrets_db.update({key: value})
        self.write_secrets_file()
        return True

    def delete(self, key: str) -> bool:
        """delete a local secret."""
        self._secrets_db.remove(key)
        self.write_secrets_file()
        return True

    def load_secrets_file(self):
        """load data from secrets file."""
        with os.open(self.source, "r") as fh:
            self._secrets_db = yaml.safe_load(fh.read())

    def write_secrets_file(self):
        """write data to secrets file."""
        with os.open(self.source, 'w') as fh:
            fh.write(yaml.safe_dump(self._secrets_db))