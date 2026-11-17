import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.core.cache import STUDENT_CACHE

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_cache():
    STUDENT_CACHE["+254712345678"] = {
        "student_id": "STU001",
        "name": "Jane Doe",
        "fees_due": "KES 15,000",
        "attendance": "95%",
        "latest_grade": "Mathematics: A"
    }
    yield
    STUDENT_CACHE.pop("+254712345678", None)
    STUDENT_CACHE.pop("+254722000001", None)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "MzaziRada" in data["service"]


def test_ussd_endpoint_initial_dial():
    response = client.post(
        "/api/v1/ussd",
        data={
            "sessionId": "test-session-123",
            "serviceCode": "*384*73355#",
            "phoneNumber": "+254712345678",
            "text": ""
        }
    )
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert "CON Welcome to MzaziRada!" in response.text


def test_ussd_endpoint_menu_selection():
    response = client.post(
        "/api/v1/ussd",
        data={
            "sessionId": "test-session-123",
            "serviceCode": "*384*73355#",
            "phoneNumber": "+254712345678",
            "text": "1"
        }
    )
    assert response.status_code == 200
    assert "END Fee Balance" in response.text
    assert "KES 15,000" in response.text


def test_webhook_update_success(monkeypatch):
    # Mock SMS alert so tests do not make real network calls
    monkeypatch.setattr(
        "app.api.webhook.send_sms_alert",
        lambda phone_number, message: {"status": "mocked", "recipients": [phone_number]}
    )

    payload = {
        "secret": settings.WEBHOOK_SECRET,
        "phone_number": "+254722000001",
        "student_id": "ADM-1002",
        "name": "Brian Kiprop",
        "fees_due": "KES 0",
        "attendance": "98%",
        "latest_grade": "Mathematics: A",
        "send_sms": True
    }

    response = client.post("/api/v1/webhook/update-student", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

    # Verify cache was updated
    assert "+254722000001" in STUDENT_CACHE
    assert STUDENT_CACHE["+254722000001"]["name"] == "Brian Kiprop"
    assert STUDENT_CACHE["+254722000001"]["fees_due"] == "KES 0"


def test_webhook_unauthorized_secret():
    payload = {
        "secret": "invalid_wrong_secret",
        "phone_number": "+254722000001",
        "student_id": "ADM-1002",
        "name": "Brian Kiprop",
        "fees_due": "KES 0",
        "attendance": "98%",
        "latest_grade": "Mathematics: A",
        "send_sms": False
    }

    response = client.post("/api/v1/webhook/update-student", json=payload)
    assert response.status_code == 401
    assert "Invalid security token" in response.json()["detail"]


def test_webhook_missing_required_fields():
    # Omitting required phone_number and name
    bad_payload = {
        "secret": settings.WEBHOOK_SECRET,
        "student_id": "ADM-1002"
    }

    response = client.post("/api/v1/webhook/update-student", json=bad_payload)
    assert response.status_code == 422
