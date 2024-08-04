import sqlite3


def create_schema(db_path):
    with sqlite3.connect(db_path) as conn:
        with open('db_setup.sql', 'r') as sql_file:
            sql_script = sql_file.read()
        conn.executescript(sql_script)


if __name__ == "__main__":
    db_path = 'test.db'
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        print(cursor.fetchall())
    # create_schema('test.db')