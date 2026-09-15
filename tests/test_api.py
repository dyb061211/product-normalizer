from urllib import response

from fastapi.testclient import TestClient
from api.app import app
import api.routes as routes
from ai.schemas import GeneratedListing
from unittest.mock import Mock
import api.routes
from ai.exceptions import LLMOutputError,LLMConnectionError,LLMAuthenticationError

client=TestClient(app)

def test_health():
    response=client.get("/health")
    assert response.status_code==200
    assert response.json()=={"status":"ok"}

def test_normalize_success():
    with open("data/input/upc.xlsx","rb") as upc_file,\
        open("data/input/products.xlsx", "rb") as products_file:
        response=client.post(
            "/normalize",
            files={
                "upc_file":(
                    "upc.xlsx",
                    upc_file,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                ),
                "products_file":(
                    "products.xlsx",
                    products_file,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            }
        )
    assert response.status_code == 200
    assert "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" \
           in response.headers["content-type"]
    assert "attachment" in response.headers["content-disposition"]
    assert "standardized_products.xlsx" \
           in response.headers["content-disposition"]
    assert len(response.content) > 0

def test_normalize_invalid_extension():
    with open("data/input/test.txt", "rb") as upc_file, \
         open("data/input/products.xlsx", "rb") as products_file:

        response = client.post(
            "/normalize",
            files={
                "upc_file": (
                    "test.txt",
                    upc_file,
                    "text/plain"
                ),
                "products_file": (
                    "products.xlsx",
                    products_file,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                ),
            }
        )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "文件必须是xlsx"
    }

def test_normalize_missing_sku():
    with open("data/input/upc.xlsx", "rb") as upc_file, \
         open("data/input/products_no_sku.xlsx", "rb") as products_file:

        response = client.post(
            "/normalize",
            files={
                "upc_file": (
                    "upc.xlsx",
                    upc_file,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                ),
                "products_file": (
                    "products_no_sku.xlsx",
                    products_file,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                ),
            }
        )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Products文件缺少sku"
    }

def test_normalize_missing_file():
    with open("data/input/upc.xlsx", "rb") as upc_file:
        response = client.post(
            "/normalize",
            files={
                "upc_file": (
                    "upc.xlsx",
                    upc_file,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            }
        )

    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["type"] == "missing"
    assert data["detail"][0]["loc"] == ["body", "products_file"]

def test_get_runs_api(monkeypatch):
    def fake_get_runs(limit):
        return [
            {
                "id": 2,
                "source": "api",
                "upc_filename": "upc2.xlsx",
                "products_filename": "products2.xlsx",
                "status": "success"
            },
            {
                "id": 1,
                "source": "cli",
                "upc_filename": "upc1.xlsx",
                "products_filename": "products1.xlsx",
                "status": "failed"
            }
        ]
    monkeypatch.setattr(
        routes,
        "get_runs",
        fake_get_runs
    )
    response=client.get("/runs?limit=2")
    data = response.json()
    assert len(data)==2
    assert response.status_code==200
    assert data[0]['id']==2
    assert data[1]['id']==1

def test_get_run_api(monkeypatch):
    def fake_get_run(run_id):
        return {
            "id": run_id,
            "source": "api",
            "upc_filename": "upc.xlsx",
            "products_filename": "products.xlsx",
            "status": "success",
            "upc_rows": 8,
            "products_rows": 6,
            "output_rows": 6,
            "validation_issue_count": 3,
            "started_at": "2026-08-30T10:00:00",
            "finished_at": "2026-08-30T10:00:01",
            "error_message": None
        }

    monkeypatch.setattr(
        routes,
        "get_run",
        fake_get_run
    )
    response = client.get("/run/5")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 5
    assert data["source"] == "api"
    assert data["status"] == "success"
    assert data["upc_rows"] == 8

def test_get_run_api_not_found(monkeypatch):
    def faka_get_run(run_id):
        return None
    monkeypatch.setattr(
        routes,
        "get_run",
        faka_get_run
    )
    response=client.get("/run/999")
    assert response.status_code==404
    assert response.json()["detail"]=="Run not found"

def test_get_run_issues_api(monkeypatch):
    def fake_get_run(run_id):
        return {
            "id": run_id,
            "source": "api",
            "status": "success"
        }

    def fake_get_run_issues(run_id):
        return [
            {
                "id": 1,
                "run_id": run_id,
                "source": "UPC",
                "row_number": 5,
                "field": "sku",
                "value": "A001",
                "error_type": "DUPLICATE",
                "message": "sku重复"
            },
            {
                "id": 2,
                "run_id": run_id,
                "source": "UPC",
                "row_number": 8,
                "field": "upc",
                "value": "",
                "error_type": "EMPTY_VALUE",
                "message": "upc不能为空"
            }
        ]
    monkeypatch.setattr(
        routes,
        "get_run",
        fake_get_run
    )
    monkeypatch.setattr(
        routes,
        "get_run_issues",
        fake_get_run_issues
    )
    response = client.get("/runs/6/issues")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["run_id"] == 6
    assert data[0]["field"] == "sku"
    assert data[0]["error_type"] == "DUPLICATE"
    assert data[1]["run_id"] == 6
    assert data[1]["field"] == "upc"
    assert data[1]["error_type"] == "EMPTY_VALUE"

def test_get_run_issues_api_not_found(monkeypatch):
    def fake_get_run(run_id):
        return None
    monkeypatch.setattr(
        routes,
        "get_run",
        fake_get_run
    )
    response = client.get("/runs/999/issues")
    assert response.status_code == 404
    assert response.json()["detail"] == "Run not found"

def test_generate_listing_api_success(monkeypatch):
    fake_listing = GeneratedListing(
        sku="A001",
        listing_title="Portable Green Camping Chair",
        bullet_points=[
            "Portable design",
            "Green finish",
            "Suitable for outdoor use"
        ],
        description="A portable camping chair."
    )
    generate_listing_mock = Mock(
        return_value=fake_listing
    )
    monkeypatch.setattr(
        api.routes,
        "generate_listing",
        generate_listing_mock
    )
    response = client.post(
        "/generate-listing",
        json={
            "sku": "A001",
            "title": "Portable Camping Chair",
            "color": "Green",
            "category": "Outdoor",
            "price": 29.99
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["sku"] == "A001"
    assert data["listing_title"] == "Portable Green Camping Chair"
    assert len(data["bullet_points"]) == 3
    assert generate_listing_mock.call_count == 1

def test_generate_listing_api_invalid_input_returns_422(monkeypatch):
    generate_listing_mock = Mock()
    monkeypatch.setattr(
        api.routes,
        "generate_listing",
        generate_listing_mock
    )
    response = client.post(
        "/generate-listing",
        json={
            "sku": "A001",
            "title": "Portable Camping Chair",
            "color": "Green",
            "category": "Outdoor",
            "price": "abc"
        }
    )
    assert response.status_code == 422
    generate_listing_mock.assert_not_called()

def test_generate_listing_api_negative_price_returns_422(monkeypatch):
    generate_listing_mock = Mock()
    monkeypatch.setattr(
        api.routes,
        "generate_listing",
        generate_listing_mock
    )
    response = client.post(
        "/generate-listing",
        json={
            "sku": "A001",
            "title": "Portable Camping Chair",
            "color": "Green",
            "category": "Outdoor",
            "price": -1
        }
    )
    assert response.status_code == 422
    generate_listing_mock.assert_not_called()

def test_generate_listing_api_empty_sku_returns_422(monkeypatch):
    generate_listing_mock = Mock()
    monkeypatch.setattr(
        api.routes,
        "generate_listing",
        generate_listing_mock
    )
    response = client.post(
        "/generate-listing",
        json={
            "sku": "",
            "title": "Portable Camping Chair",
            "color": "Green",
            "category": "Outdoor",
            "price": 29.99
        }
    )
    assert response.status_code == 422
    generate_listing_mock.assert_not_called()

def test_generate_listing_api_connection_error_returns_503(monkeypatch):
    generate_listing_mock = Mock(
        side_effect=LLMConnectionError("LLM connection failed")
    )
    monkeypatch.setattr(
        api.routes,
        "generate_listing",
        generate_listing_mock
    )
    response = client.post(
        "/generate-listing",
        json={
            "sku": "A001",
            "title": "Portable Camping Chair",
            "color": "Green",
            "category": "Outdoor",
            "price": 29.99
        }
    )
    assert response.status_code == 503
    assert response.json() == {
        "detail": "AI service unavailable"
    }
    assert generate_listing_mock.call_count == 1

def test_generate_listing_api_output_error_returns_502(monkeypatch):
    generate_listing_mock = Mock(
        side_effect=LLMOutputError("Invalid LLM output")
    )
    monkeypatch.setattr(
        api.routes,
        "generate_listing",
        generate_listing_mock
    )
    response = client.post(
        "/generate-listing",
        json={
            "sku": "A001",
            "title": "Portable Camping Chair",
            "color": "Green",
            "category": "Outdoor",
            "price": 29.99
        }
    )
    assert response.status_code == 502
    assert response.json() == {
        "detail": "AI service returned invalid output"
    }
    assert generate_listing_mock.call_count == 1

def test_generate_listing_api_authentication_error_returns_500(monkeypatch):
    generate_listing_mock = Mock(
        side_effect=LLMAuthenticationError(
            "LLM authentication failed"
        )
    )
    monkeypatch.setattr(
        api.routes,
        "generate_listing",
        generate_listing_mock
    )
    response = client.post(
        "/generate-listing",
        json={
            "sku": "A001",
            "title": "Portable Camping Chair",
            "color": "Green",
            "category": "Outdoor",
            "price": 29.99
        }
    )
    assert response.status_code == 500
    assert response.json() == {
        "detail": "AI service error"
    }
    assert generate_listing_mock.call_count == 1