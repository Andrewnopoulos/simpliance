from dataclasses import dataclass, astuple as tup, fields as fiel, field

@dataclass
class RootObject():

    _dirty : list = field(default_factory=list, compare=False, repr=False, kw_only=True)

    def astuple(self):
        # First element is _dirty list which we want to ignore, so pop it
        list_form = list(tup(self))
        list_form.pop(0)
        return tuple(list_form)
    def fields(self):
        # Don't include _dirty in fields
        return tuple([f.name for f in fiel(self) if f.name != '_dirty'])
    
    def set(self, field, value):
        try:
            self.__setattr__(field, value)
            print(self._dirty)
            if field not in self._dirty:
                self._dirty.append(field)
        except AttributeError:
            print(f"{field} not found in object")

    def get(self, field: str):
        try:
            return self.__getattribute__(field)
        except AttributeError:
            return None
    
    @staticmethod
    def row_factory(cursor, row):
        print("Base row factory whoopsie")
        return row

    @staticmethod
    def table():
        return "ERROR"

@dataclass
class AuthKeys(RootObject):
    role_id: str
    external_id: str
    user_id: str

    @staticmethod
    def row_factory(cursor, row):
        return AuthKeys(*row)
    
    @staticmethod
    def table():
        return "auth_keys"
    

@dataclass
class Report(RootObject):
    id: str
    process_state: str
    datetime_started: str
    datetime_completed: str
    user_id: str

    @staticmethod
    def row_factory(cursor, row):
        return Report(*row)
    
    @staticmethod
    def table():
        return "reports"

@dataclass
class User(RootObject):
    id: str
    name: str

    @staticmethod
    def row_factory(cursor, row):
        return User(*row)
    
    @staticmethod
    def table():
        return "users"
