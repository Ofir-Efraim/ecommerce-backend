from abc import ABC, abstractmethod
from typing import Optional


class BaseDBUtils(ABC):
    def __init__(self, host: str, username: str, password: str, port: Optional[int] = None,
                 db_name: Optional[str] = None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db_name = db_name

    def __new__(cls, is_singleton: bool = True, *args, **kwargs):
        if is_singleton:
            if not hasattr(cls, 'instance'):
                cls.instance = super(BaseDBUtils, cls).__new__(cls)
            return cls.instance
        return super(BaseDBUtils, cls).__new__(cls)

    @abstractmethod
    def _connect(self):
        pass

    @abstractmethod
    def _disconnect(self):
        pass
