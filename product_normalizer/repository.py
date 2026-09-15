from product_normalizer.database import get_connection
from datetime import datetime

def create_run(source,upc_filename,products_filename):
    conn=get_connection()
    source=source
    upc_filename=upc_filename
    products_filename=products_filename
    started_at=datetime.now().isoformat(timespec='seconds')
    cursor=conn.cursor()
    cursor.execute(
        """
        INSERT INTO processing_runs(source,upc_filename,products_filename,started_at)
        VALUES (?,?,?,?)
        """,
        (source,upc_filename,products_filename,started_at)
    )
    last_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return last_id

def update_run_success(run_id,upc_rows,products_rows,output_rows,validation_issue_count):
    conn=get_connection()
    cursor=conn.cursor()
    finished_at=datetime.now().isoformat(timespec='seconds')
    cursor.execute(
        """
        UPDATE processing_runs SET upc_rows=?,products_rows=?,output_rows=?,validation_issue_count=?,finished_at=?,status='success'
        WHERE id=?
        """,
        (upc_rows,products_rows,output_rows,validation_issue_count,finished_at,run_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

def update_run_failed(run_id,error_message):
    conn=get_connection()
    cursor=conn.cursor()
    finished_at=datetime.now().isoformat(timespec='seconds')
    cursor.execute(
        """
        UPDATE processing_runs SET status=?,error_message=?,finished_at=? WHERE id=?
        """,
        ('failed',error_message,finished_at,run_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_run(run_id):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
        """
        SELECT * FROM processing_runs WHERE id=?
        """,
        (run_id,)
    )
    row=cursor.fetchone()
    cursor.close()
    conn.close()
    if row is None:
        return None
    return dict(row)

def get_runs(limit):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
        """
        SELECT * FROM processing_runs ORDER BY id DESC LIMIT ?
        """,
        (limit,)
    )
    rows=cursor.fetchall()
    result=[dict(row) for row in rows]
    cursor.close()
    conn.close()
    return result

def get_run_issues(run_id):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
        """
        SELECT * FROM validation_issues WHERE run_id=? ORDER BY id ASC
        """,
        (run_id,)
    )
    rows=cursor.fetchall()
    cursor.close()
    conn.close()
    result=[dict(row) for row in rows]
    return result

def save_validation_issues(run_id,issues):
    conn=get_connection()
    cursor=conn.cursor()
    params = []
    for _,row in issues.iterrows():
        params.append(
            (
                run_id,
                row["source"],
                row["row_number"],
                row["field"],
                row["value"],
                row["error_type"],
                row["message"]
            )
        )
    cursor.executemany(
        """
        INSERT INTO validation_issues (run_id,source,row_number,field,value,error_type,message) VALUES (?,?,?,?,?,?,?)
        """,
        params
    )
    conn.commit()
    cursor.close()
    conn.close()