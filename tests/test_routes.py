from fastapi.testclient import TestClient

from converter.app import app

client = TestClient(app)

import converter.routes


def test_success():
    response = client.get("/api/rates", params={"from": "USD", "to": "RUB"})
    assert response.status_code == 200
    assert "result" in response.json()


def test_value():
    response = client.get(
        "/api/rates", params={"from": "USD", "to": "RUB", "value": 100}
    )
    assert response.status_code == 200
    assert "result" in response.json()


def test_failure():
    response = client.get("/api/rates", params={"from": "USD", "to": "RUBasdfa"})
    assert response.status_code == 422
