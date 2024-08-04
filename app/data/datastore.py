import sqlite3
from typing import Type
from models import RootObject, AuthKeys, Report, User

def create_schema(db_path):
    with sqlite3.connect(db_path) as conn:
        with open('db_setup.sql', 'r') as sql_file:
            sql_script = sql_file.read()
        conn.executescript(sql_script)

class Storage():
    def __init__(self, db_path: str):
        self.db_path = db_path

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass

    def _execute_modification(self, query: str, item: RootObject) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, item.astuple())
            conn.commit()
            return cursor.rowcount

    def _execute_query(self, query: str, item: Type[RootObject]) -> list:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = item.row_factory
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        
    def get_all(self, item: Type[RootObject]) -> list:
        query = f"SELECT * from {item.table()};"
        return self._execute_query(query, item)
    
    def delete(self, item: RootObject) -> int:
        where_clause = ' AND '.join([f"{field} = ?" for field in item.fields()])
        query = f"DELETE FROM {item.table()} WHERE {where_clause}"
        print (query)
        print(item)
        return self._execute_modification(query, item)

    def insert(self, obj: RootObject) -> int:
        columns = ', '.join(obj.fields())
        placeholders = ', '.join(['?' for _ in obj.fields()])
        query = f"INSERT INTO {obj.table()} ({columns}) VALUES ({placeholders})"
        return self._execute_modification(query, obj)

if __name__ == "__main__":

    db_path = 'test.db'
    create_schema(db_path)

    import uuid

    with Storage(db_path) as storage:
        u = User("Andy", str(uuid.uuid4()))
        storage.insert(u)
        k = AuthKeys("role", "extern", u.id)
        storage.insert(k)
        all_users = storage.get_all(u)
        print(all_users)
        all_keys = storage.get_all(AuthKeys)
        print(all_keys)

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