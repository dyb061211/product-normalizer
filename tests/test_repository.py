import sqlite3
from pathlib import Path
import product_normalizer.repository as repository
import pytest
import pandas as pd

@pytest.fixture
def temp_repository_db(tmp_path,monkeypatch):
    dp_path = tmp_path / 'test.db'
    root_path = Path(__file__).resolve().parent.parent
    schema_path = root_path / "database" / "schema.sql"
    schema_sql = schema_path.read_text(encoding='utf-8')
    conn = sqlite3.connect(dp_path)
    conn.executescript(schema_sql)
    conn.close()
    def fake_get_connecttion():
        conn = sqlite3.connect(dp_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    monkeypatch.setattr(
        repository,
        "get_connection",
        fake_get_connecttion
    )
    return dp_path

def test_create_run(temp_repository_db):
    run_id=repository.create_run(
        source='api',
        upc_filename='test_upc.xlsx',
        products_filename='test_products.xlsx'
    )
    assert run_id==1
    run=repository.get_run(run_id)
    assert run['id']==1
    assert run['upc_filename']=='test_upc.xlsx'
    assert run['products_filename']=='test_products.xlsx'
    assert run['status']=='running'

def test_update_run_success(temp_repository_db):
    run_id=repository.create_run(
        source='api',
        upc_filename='test_upc.xlsx',
        products_filename='test_products.xlsx'
    )
    repository.update_run_success(
        run_id=run_id,
        upc_rows=8,
        products_rows=6,
        output_rows=6,
        validation_issue_count=3
    )
    run=repository.get_run(run_id)
    assert run["status"] == "success"
    assert run["upc_rows"] == 8
    assert run["products_rows"] == 6
    assert run["output_rows"] == 6
    assert run["validation_issue_count"] == 3
    assert run["finished_at"] is not None

def test_update_run_failed(temp_repository_db):
    run_id=repository.create_run(
        source='api',
        upc_filename='test_upc.xlsx',
        products_filename='test_products.xlsx'
    )
    repository.update_run_failed(
        run_id=run_id,
        error_message="Missing required column:sku"
    )
    row=repository.get_run(run_id)
    assert row["status"] == "failed"
    assert row["error_message"] == "Missing required column:sku"
    assert row["finished_at"] is not None

def test_save_validation_issues(temp_repository_db):
    run_id=repository.create_run(
        source='api',
        upc_filename='test_upc.xlsx',
        products_filename='test_products.xlsx'
    )
    issues=pd.DataFrame([
        {
            "source": "UPC",
            "row_number": 5,
            "field": "sku",
            "value": "A001",
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
    repository.save_validation_issues(
        run_id=run_id,
        issues=issues,
    )
    rows=repository.get_run_issues(run_id)
    assert len(rows)==2
    assert rows[0]["run_id"] == run_id
    assert rows[0]["source"] == "UPC"
    assert rows[0]["row_number"] == 5
    assert rows[0]["field"] == "sku"
    assert rows[0]["value"] == "A001"
    assert rows[0]["error_type"] == "DUPLICATE"
    assert rows[0]["message"] == "sku重复"
    assert rows[1]["run_id"] == run_id
    assert rows[1]["field"] == "upc"
    assert rows[1]["error_type"] == "EMPTY_VALUE"

def test_get_run_not_found(temp_repository_db):
    run=repository.get_run(999)
    assert run is None

def test_get_runs_limit(temp_repository_db):
    repository.create_run(
        source='api',
        upc_filename='test_upc1.xlsx',
        products_filename='test_products1.xlsx'
    )
    repository.create_run(
        source='api',
        upc_filename='test_upc2.xlsx',
        products_filename='test_products2.xlsx'
    )
    repository.create_run(
        source='api',
        upc_filename='test_upc3.xlsx',
        products_filename='test_products3.xlsx'
    )
    rows=repository.get_runs(limit=2)
    assert len(rows)==2
    assert rows[0]['id']==3
    assert rows[1]['id']==2

def test_save_validation_issues_invalid_run_id(temp_repository_db):
     issues = pd.DataFrame([
         {
             "source": "UPC",
             "row_number": 5,
             "field": "sku",
             "value": "A001",
             "error_type": "DUPLICATE",
             "message": "sku重复"
         }
     ])
     with pytest.raises(sqlite3.IntegrityError):
         repository.save_validation_issues(
             run_id=999,
             issues=issues,
         )
