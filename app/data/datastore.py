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
        
    def get_all(self, item: Type[RootObject]) -> list:
        query = f"SELECT * from {item.table()};"
        return self._execute_query(query, item)
    
    def delete(self, item: RootObject) -> int:
        where_clause = ' AND '.join([f"{field} = ?" for field in item.fields()])
        query = f"DELETE FROM {item.table()} WHERE {where_clause}"
        return self._execute_modification(query, item.astuple())
    
    def update(self, item: RootObject, fields_to_update: list[str]) -> int:
        update_fields_copy = fields_to_update.copy()
        all_fields = item.fields()
        update_fields = []
        search_fields = []
        for field in all_fields:
            if field in update_fields_copy:
                update_fields.append(field)
                update_fields_copy.remove(field)
            else:
                search_fields.append(field)
        if update_fields_copy:
            print(f"These fields were not found: {update_fields_copy}")
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

if __name__ == "__main__":

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
        modified_count = storage.update(r, ["datetime_completed"])
        print(f"modified rows: {modified_count}")

        reports = storage.get_all(Report)
        print(reports)


        # k = AuthKeys("doasifj", "osdijf", u.id)
        # storage.delete(k)

        # for k in all_keys:
        #     storage.delete(k)

        # all_keys = storage.get_all(AuthKeys)
        # print(all_keys)

        # for u in all_users:
        #     storage.delete(u)

        # all_users = storage.get_all(u)
        # print(all_users)
