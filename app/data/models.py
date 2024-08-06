from dataclasses import dataclass, astuple as tup, fields as fiel, field
from typing import Any, ClassVar

@dataclass
class RootObject():

    _dirty : list = field(default_factory=list, compare=False, repr=False, kw_only=True)
    _table : ClassVar[str] = ""

    def __post_init__(self):
        self._dirty = []

    def astuple(self):
        # First element is _dirty list which we want to ignore, so pop it
        list_form = list(tup(self))
        list_form.pop(0)
        return tuple(list_form)

    @classmethod
    def fields(cls):
        # Don't include _dirty in fields
        return tuple([f.name for f in fiel(cls) if f.name != '_dirty'])
    
    def __setattr__(self, name: str, value: Any) -> None:
        if name != '_dirty':
            try:
                if name not in self._dirty:
                    self._dirty.append(name)
            except AttributeError:
                print("no dirty")
            
        super().__setattr__(name, value)

    def get(self, field: str):
        try:
            return self.__getattribute__(field)
        except AttributeError:
            return None
    
    def dict(self):
        representation = self.__dict__.copy()
        del representation['_dirty']
        return representation
    
    @classmethod
    def row_factory(cls, cursor, row):
        return cls(*row)
    
    @staticmethod
    def primary() -> list[str]:
        return []

@dataclass
class AuthKeys(RootObject):
    _table = "auth_keys"

    role_id: str
    external_id: str
    user_id: str
    
    @staticmethod
    def primary() -> list[str]:
        return ['role_id', 'external_id', 'user_id']
    

@dataclass
class Report(RootObject):
    _table = "reports"

    id: str
    process_state: str
    datetime_started: str
    datetime_completed: str
    user_id: str

    @staticmethod
    def primary() -> list[str]:
        return ['id']

@dataclass
class User(RootObject):
    _table = "users"

    id: str
    name: str
    
    @staticmethod
    def primary() -> list[str]:
        return ['id']
