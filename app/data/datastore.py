import sqlite3
from typing import Type
from .models import RootObject, User, AuthKeys, Report
import pendulum

DEFAULT_DB_PATH = '/code/db/main.db'
DEFAULT_SETUP_PATH = 'db_setup.sql'

def create_schema(db_dest_path=DEFAULT_DB_PATH, db_setup_script_path=DEFAULT_SETUP_PATH):
    with sqlite3.connect(db_dest_path) as conn:
        with open(db_setup_script_path, 'r') as sql_file:
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

    def _execute_query_params(self, query: str, item: Type[RootObject], parameters: tuple) -> list:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = item.row_factory
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            return cursor.fetchall()
    
    def _execute_single(self, query:str, item: Type[RootObject], parameters: tuple) -> RootObject:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = item.row_factory
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            return cursor.fetchone()
        
    def get_all(self, item: Type[RootObject]) -> list:
        query = f"SELECT * from {item._table};"
        return self._execute_query(query, item)
    
    def get_where(self, item_type: Type[RootObject], search_dict: dict) -> list:
        # Regular dicts _should_ be ordered, but just in case:
        # Note that we are assuming it's ordered when fetching keys and values
        where_clause = ' AND '.join([f"{field} = ?" for field in search_dict.keys() if field in item_type.fields()])
        item = tuple(search_dict.values())
        if not where_clause:
            return None
        query = f"SELECT * from {item_type._table} WHERE {where_clause}"
        return self._execute_query_params(query, item_type, item)
    
    def get_one(self, item_type: Type[RootObject], search_dict: dict) -> RootObject:
        # Regular dicts _should_ be ordered, but just in case:
        # Note that we are assuming it's ordered when fetching keys and values
        where_clause = ' AND '.join([f"{field} = ?" for field in search_dict.keys() if field in item_type.fields()])
        item = tuple(search_dict.values())
        if not where_clause:
            return None
        query = f"SELECT * from {item_type._table} WHERE {where_clause}"
        return self._execute_single(query, item_type, item)
    
    def delete(self, item: RootObject) -> int:
        where_clause = ' AND '.join([f"{field} = ?" for field in item.fields()])
        query = f"DELETE FROM {item._table} WHERE {where_clause}"
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
        query = f"UPDATE {item._table} SET {set_clause} WHERE {where_clause}"
        all_values = tuple(item.get(field) for field in update_fields) + tuple(item.get(field) for field in search_fields)
        return self._execute_modification(query, all_values)

    def insert(self, item: RootObject) -> int:
        columns = ', '.join(item.fields())
        placeholders = ', '.join(['?' for _ in item.fields()])
        query = f"INSERT INTO {item._table} ({columns}) VALUES ({placeholders})"
        retval = self._execute_modification(query, item.astuple())
        if retval != 0:
            item._dirty = []
        return retval
