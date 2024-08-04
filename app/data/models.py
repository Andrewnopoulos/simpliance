from dataclasses import dataclass, astuple as tup, fields as fiel


@dataclass
class RootObject():
    def astuple(self):
        return tup(self)
    def fields(self):
        return tuple([f.name for f in fiel(self)])
    
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
    name: str
    id: str

    @staticmethod
    def row_factory(cursor, row):
        return User(*row)
    
    @staticmethod
    def table():
        return "users"
