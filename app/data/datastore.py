import sqlite3
from typing import Type
from models import RootObject, User, AuthKeys, Report
import pendulum

DEFAULT_DB_PATH = '/code/db/main.db'

def create_schema(db_path=DEFAULT_DB_PATH):
    with sqlite3.connect(db_path) as conn:
        with open('db_setup.sql', 'r') as sql_file:
            sql_script = sql_file.read()
        conn.executescript(sql_script)

class Storage():
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass

    def _execute_modification(self, query: str, item: tuple) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, item)
            conn.commit()
            return cursor.rowcount

    def _execute_query(self, query: str, item: Type[RootObject]) -> list:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = item.row_factory
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
    
    def _execute_single(self, query:str, item: Type[RootObject], parameters: tuple) -> RootObject:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = item.row_factory
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            return cursor.fetchone()
        
    def get_all(self, item: Type[RootObject]) -> list:
        query = f"SELECT * from {item.table()};"
        return self._execute_query(query, item)
    
    def get_one(self, item_type: Type[RootObject], search_dict: dict) -> RootObject:
        # Regular dicts _should_ be ordered, but just in case:
        # Note that we are assuming it's ordered when fetching keys and values
        where_clause = ' AND '.join([f"{field} = ?" for field in search_dict.keys() if field in item_type.fields()])
        item = tuple(search_dict.values())
        if not where_clause:
            return None
        query = f"SELECT * from {item_type.table()} WHERE {where_clause}"
        return self._execute_single(query, item_type, item)
    
    def delete(self, item: RootObject) -> int:
        where_clause = ' AND '.join([f"{field} = ?" for field in item.fields()])
        query = f"DELETE FROM {item.table()} WHERE {where_clause}"
        return self._execute_modification(query, item.astuple())
    
    def update(self, item: RootObject, fields_to_update: list[str] = []) -> int:
        if fields_to_update:
            dirty_fields = fields_to_update.copy()
        else:
            dirty_fields = item._dirty
        all_fields = item.fields()
        update_fields = []
        search_fields = []
        for field in all_fields:
            if field in dirty_fields:
                update_fields.append(field)
                dirty_fields.remove(field)
            else:
                search_fields.append(field)
        if not update_fields:
            print("Updating nothing")
            return

        set_clause = ', '.join([f"{field} = ?" for field in update_fields])
        where_clause = ' AND '.join([f"{field} = ?" for field in search_fields])
        query = f"UPDATE {item.table()} SET {set_clause} WHERE {where_clause}"
        all_values = tuple(item.get(field) for field in update_fields) + tuple(item.get(field) for field in search_fields)
        return self._execute_modification(query, all_values)

    def insert(self, item: RootObject) -> int:
        columns = ', '.join(item.fields())
        placeholders = ', '.join(['?' for _ in item.fields()])
        query = f"INSERT INTO {item.table()} ({columns}) VALUES ({placeholders})"
        return self._execute_modification(query, item.astuple())

def test():

    db_path = 'test.db'
    create_schema(db_path)

    import uuid

    with Storage(db_path) as storage:
        u = User(str(uuid.uuid4()), "Andy")
        storage.insert(u)
        k = AuthKeys("role", "extern", u.id)
        storage.insert(k)
        all_users = storage.get_all(u)
        print(all_users)
        all_keys = storage.get_all(AuthKeys)
        print(all_keys)

        reports = storage.get_all(Report)
        for r in reports:
            storage.delete(r)
        
        reports = storage.get_all(Report)
        print(f"reports: {len(reports)}")

        r = Report(str(uuid.uuid4()), "in-progress", pendulum.now().to_iso8601_string(), '', u.id)
        storage.insert(r)

        reports = storage.get_all(Report)
        print(reports)

        r.datetime_completed = pendulum.now().to_iso8601_string()

        # r.datetime_completed = pendulum.now().to_iso8601_string()
        print(r._dirty)
        modified_count = storage.update(r)
        print(f"modified rows: {modified_count}")
        print(r._dirty)

        reports = storage.get_all(Report)
        print(reports)


        k = AuthKeys("doasifj", "osdijf", u.id)
        storage.delete(k)

        for k in all_keys:
            storage.delete(k)

        all_keys = storage.get_all(AuthKeys)
        print(all_keys)

        for u in all_users:
            storage.delete(u)

        all_users = storage.get_all(u)
        print(all_users)

def test1():
    db_path = 'test.db'
    create_schema(db_path)

    import uuid

    with Storage(db_path) as storage:
        u = User(str(uuid.uuid4()), "Andy")

        print("dirty")
        print(u._dirty)
        print(u)

def test2():
    db_path = 'test.db'
    create_schema(db_path)

    import uuid

    with Storage(db_path) as storage:
        u = User(str(uuid.uuid4()), "Andy")

        storage.insert(u)

        retval = storage.get_one(User, {'name': 'Andy'})
        print(retval)

        retval = storage.get_one(User, {'id': u.id})
        print(retval)

        retval = storage.get_one(User, {})
        print(retval)

        retval = storage.get_one(User, {'id': 'sodifjds'})
        print(retval)

        retval = storage.get_one(User, {'sodifj': 'dsoifj'})
        print(retval)
    


if __name__ == "__main__":
    test2()
