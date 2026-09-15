import sqlite3
from pathlib import Path

root_path=Path(__file__).resolve().parent.parent

def get_connection():
    connection =sqlite3.connect(str(root_path/"data"/"database"/'product_normalizer.db'))
    connection.execute('PRAGMA foreign_keys=ON')
    connection.row_factory=sqlite3.Row
    return connection

def initialize_database():
    conn=get_connection()
    schema_path=root_path/"database"/"schema.sql"
    schema_sql=schema_path.read_text(encoding="utf-8")
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()

