import sqlite3
from pathlib import Path

def test_database_table_exist(tmp_path):
    root_path=Path(__file__).resolve().parent.parent
    dp_path=tmp_path/'test.db'
    schema_path=root_path/'database'/'schema.sql'
    schema_sql=schema_path.read_text(encoding='utf-8')
    con=sqlite3.connect(dp_path)
    cursor=con.cursor()
    con.executescript(schema_sql)
    cursor.execute(
        """
        SELECT name FROM sqlite_master WHERE type='table'
        """
    )
    rows=cursor.fetchall()
    cursor.close()
    con.close()
    assert len(rows)>0
    rows=[row[0] for row in rows]
    assert "processing_runs" in rows
    assert "validation_issues" in rows