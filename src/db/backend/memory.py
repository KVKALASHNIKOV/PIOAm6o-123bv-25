from .base import BaseDB
from .table import Table


class InMemoryDB(Table, BaseDB):
    """База данных в оперативной памяти."""
    pass
