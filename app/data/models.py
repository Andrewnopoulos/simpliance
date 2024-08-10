from itertools import count
from dataclasses import dataclass, astuple as tup, fields as fiel, field
from typing import Any, ClassVar, Optional

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
        return ['id']

@dataclass
class AuthKeys(RootObject):
    _table = "auth_keys"

    id: str
    role_id: str
    external_id: str
    user_id: str


@dataclass
class Report(RootObject):
    _table = "reports"

    id: str
    process_state: str
    datetime_started: str
    datetime_completed: str
    benchmark: str
    user_id: str
    auth_key_id: int

@dataclass
class User(RootObject):
    _table = "users"

    id: str
    name: str
    email: str
    disabled: bool = field(default=False)
    hashed_password: Optional[str] = field(default=None, repr=False)

    # @property
    # def password(self) -> Optional[str]:
    #     return self.hashed_password

    # @password.setter
    # def password(self, value: str):
    #     # Here you could add additional validation or hashing logic
    #     print("TODO - hashing password")
    #     print(value)
    #     self.hashed_password = value + "_hashed"

    # def astuple(self):
    #     # First element is _dirty list which we want to ignore, so pop it
    #     list_form = list(tup(self))
    #     list_form.pop(0)
    #     list_form.pop(-1) # Pop last element too (hashed password)
    #     return tuple(list_form)

    # @classmethod
    # def fields(cls):
    #     # Don't include _dirty in fields
    #     return tuple([f.name for f in fiel(cls) if f.name not in ['_dirty', 'hashed_password']])