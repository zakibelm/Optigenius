from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_post_appointment_success():
    payload = {
        "name": "Alice",
        "phone": "0612345678",
        "datetime": "2025-08-11T15:00:00Z",
        "notes": "Urgent",
    }
    resp = client.post("/appointments", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["received"]["name"] == "Alice"


def test_post_appointment_missing_name():
    payload = {"phone": "0612345678", "datetime": "2025-08-11T15:00:00Z"}
    resp = client.post("/appointments", json=payload)
    assert resp.status_code == 422


def test_post_appointment_bad_datetime():
    payload = {"name": "Bob", "phone": "0612345678", "datetime": "not-a-date"}
    resp = client.post("/appointments", json=payload)
    assert resp.status_code == 422
