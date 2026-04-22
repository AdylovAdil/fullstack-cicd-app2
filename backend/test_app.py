import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True, "DATABASE_URL": "sqlite:///:memory:"})
    return app.test_client()


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_get_empty_data(client):
    response = client.get("/api/data")
    assert response.status_code == 200
    assert response.get_json() == []


def test_post_data(client):
    response = client.post("/api/data", json={"title": "Первая задача"})
    body = response.get_json()

    assert response.status_code == 201
    assert body["id"] == 1
    assert body["title"] == "Первая задача"

    get_response = client.get("/api/data")
    items = get_response.get_json()
    assert len(items) == 1
    assert items[0]["title"] == "Первая задача"


def test_delete_data(client):
    create = client.post("/api/data", json={"title": "Удалить меня"})
    item_id = create.get_json()["id"]

    response = client.delete(f"/api/data/{item_id}")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Запись удалена"

    get_response = client.get("/api/data")
    assert get_response.get_json() == []


def test_delete_missing_item(client):
    response = client.delete("/api/data/999")
    assert response.status_code == 404
