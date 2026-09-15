# import sqlite3
#
# conn=sqlite3.connect("/Users/dyb/Desktop/product-normalizer/week4_schema_test.db")
# cursor=conn.cursor()
# # cursor.execute("SELECT * FROM processing_runs")
# # rows=cursor.fetchall()
# # print(rows)
# # cursor.execute("SELECT * FROM processing_runs WHERE id=1")
# # rows1=cursor.fetchone()
# # print(rows1)
# # cursor.execute("INSERT INTO processing_runs (source,upc_filename,products_filename,started_at) "
# #                "VALUES('cli','rollback_upc','rollback_products','2026-08-30 12:20:00')")
# # conn.rollback()
#
# # try:
# #     cursor.execute("""
# #                    INSERT INTO processing_runs(source,upc_filename,products_filename,started_at)
# #                    VALUES('cli','transaction_upc','transaction_products','2026-08-30 12:30:00')
# #                    """
# #                    )
# #     cursor.execute("""
# #                    INSERT INTO processing_runs(source,upc_filename,products_filename,started_at)
# #                    VALUES('web','transaction_upc','transaction_products','2026-08-30 12:30:00')
# #                    """
# #                    )
# #     conn.commit()
# # except Exception as e:
# #     print(e)
# #     conn.rollback()
# source='api'
# cursor.execute(
#     """
#     SELECT * FROM processing_runs WHERE source=?
#     """,
#     (source,)
# )
# source='cli'
# upc_filename='parameter_upc'
# products_filename='parameter_products'
# started_at='2026-08-30 12:40:00'
# cursor.execute(
#     """
#     INSERT INTO processing_runs (source,upc_filename,products_filename,started_at)
#     VALUES(?,?,?,?)
#     """,
#     (source,upc_filename,products_filename,started_at)
# )
# conn.commit()
# rows=cursor.fetchall()
# print(rows)
# cursor.close()
# conn.close()
#
from product_normalizer.repository import *
import pandas as pd

test_issues = pd.DataFrame([
    {
        "source": "UPC",
        "row_number": 5,
        "field": "sku",
        "value": "ABC123",
        "error_type": "DUPLICATE",
        "message": "sku重复"
    },
    {
        "source": "UPC",
        "row_number": 8,
        "field": "upc",
        "value": "",
        "error_type": "EMPTY_VALUE",
        "message": "upc不能为空"
    }
])
save_validation_issues(1, test_issues)

print(get_run_issues(1))

