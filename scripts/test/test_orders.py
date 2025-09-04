from fastapi.testclient import TestClient
from scripts.main import app

client = TestClient(app)

def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_ingest_orders():
    payload = {
        "orders": [
            {"id": "o1","customer_id": 1,"created_at": "2025-08-20T10:00:00Z","currency": "EUR",
             "items":[{"sku":"A","quantity":2,"unit_price":10.0}]},
            {"id": "o2","customer_id": 2,"created_at": "2025-08-20T11:00:00Z","currency": "USD",
             "items":[{"sku":"B","quantity":1,"unit_price":30.0},{"sku":"C","quantity":3,"unit_price":5.0}]},
            {"id": "o2","customer_id": 2,"created_at": "2025-08-20T12:00:00Z","currency": "USD",
             "items":[{"sku":"B","quantity":1,"unit_price":32.0},{"sku":"C","quantity":3,"unit_price":5.0}]},
            {"id": "o3","customer_id": 3,"created_at": "2025-08-20T09:00:00Z","currency": "GBP",
             "items":[{"sku":"D","quantity":1,"unit_price":100.0}]}
        ]
    }
    response = client.post("/orders/ingest", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["summary"]["orders_received"] == 4
    assert data["summary"]["orders_valid"] == 3
    assert data["summary"]["orders_invalid"] == 0
    assert data["summary"]["duplicates_dropped"] == 1
