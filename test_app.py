import pytest
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app, init_db

TEST_DB = "test_contacts.db"


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr("app.DB_PATH", str(tmp_path / "test.db"))
    app.config["TESTING"] = True
    init_db()
    with app.test_client() as client:
        yield client


def test_homepage_loads(client):
    res = client.get("/")
    assert res.status_code == 200


def test_contact_success(client):
    res = client.post(
        "/api/contact",
        data=json.dumps({"name": "Test User", "email": "test@example.com", "message": "Hello!"}),
        content_type="application/json",
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["success"] is True


def test_contact_missing_fields(client):
    res = client.post(
        "/api/contact",
        data=json.dumps({"name": "", "email": "", "message": ""}),
        content_type="application/json",
    )
    assert res.status_code == 400
    assert res.get_json()["success"] is False


def test_contact_invalid_email(client):
    res = client.post(
        "/api/contact",
        data=json.dumps({"name": "Test", "email": "not-an-email", "message": "Hi"}),
        content_type="application/json",
    )
    assert res.status_code == 400


def test_messages_endpoint(client):
    # Insert one message first
    client.post(
        "/api/contact",
        data=json.dumps({"name": "A", "email": "a@b.com", "message": "Test"}),
        content_type="application/json",
    )
    res = client.get("/api/messages")
    assert res.status_code == 200
    messages = res.get_json()
    assert len(messages) == 1
    assert messages[0]["name"] == "A"
