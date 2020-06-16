class MooseSecretSourceBase:
    """Moose secret source base class."""
    _source: str = 'base'

    def __str__(self):
        return f'{self.source}'

    @property
    def source(self):
        """secrets source."""
        return self._source

    def read(self, key: str) -> object:
        """read a secret from source."""
        return False

    def create(self, key: str, value: str, update: bool = False) -> bool:
        """create a secret at source."""
        return False

    def delete(self, key: str) -> bool:
        """delete a secret at source."""
        return False


class MooseSecretBase:
    """Moose config secret manager base."""
    _key: str = None
    _source: str = None
    _value: str = None