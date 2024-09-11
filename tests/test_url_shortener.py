import mongomock
import pytest
from flask import json

from url_shortener import app, CompactUrl, connect


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def setup_db():
    connect("mongoengine_test", mongo_client_class=mongomock.MongoClient)
    yield
    CompactUrl.drop_collection()


def test_create_url(client):
    response = client.post("/shorten", json={"url": "https://www.example.com"})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert "short_code" in data
    assert data["url"] == "https://www.example.com"


def test_create_invalid_url(client):
    response = client.post("/shorten", json={"url": "invalid_url"})
    assert response.status_code == 400


def test_get_original_url(client):
    # First, create a shortened URL
    create_response = client.post("/shorten", json={"url": "https://www.example.com"})
    short_code = json.loads(create_response.data)["short_code"]

    # Now, try to retrieve it
    response = client.get(f"/shorten/{short_code}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["url"] == "https://www.example.com"


def test_get_nonexistent_url(client):
    response = client.get("/shorten/nonexistent")
    assert response.status_code == 404


def test_update_url(client):
    # First, create a shortened URL
    create_response = client.post("/shorten", json={"url": "https://www.example.com"})
    short_code = json.loads(create_response.data)["short_code"]

    # Now, update it
    update_response = client.put(
        f"/shorten/{short_code}", json={"url": "https://www.newexample.com"}
    )
    assert update_response.status_code == 200
    data = json.loads(update_response.data)
    assert data["url"] == "https://www.newexample.com"


def test_update_nonexistent_url(client):
    response = client.put(
        "/shorten/nonexistent", json={"url": "https://www.example.com"}
    )
    assert response.status_code == 404


def test_delete_url(client):
    # First, create a shortened URL
    create_response = client.post("/shorten", json={"url": "https://www.example.com"})
    short_code = json.loads(create_response.data)["short_code"]

    # Now, delete it
    delete_response = client.delete(f"/shorten/{short_code}")
    assert delete_response.status_code == 204

    # Try to retrieve the deleted URL
    get_response = client.get(f"/shorten/{short_code}")
    assert get_response.status_code == 404


def test_delete_nonexistent_url(client):
    response = client.delete("/shorten/nonexistent")
    assert response.status_code == 404


def test_get_stats(client):
    # First, create a shortened URL
    create_response = client.post("/shorten", json={"url": "https://www.example.com"})
    short_code = json.loads(create_response.data)["short_code"]

    # Access the URL to increment the counter
    client.get(f"/{short_code}")

    # Now, get the stats
    stats_response = client.get(f"/shorten/{short_code}/stats")
    assert stats_response.status_code == 200
    data = json.loads(stats_response.data)
    assert data["access_count"] == 1


def test_redirect(client):
    # First, create a shortened URL
    create_response = client.post("/shorten", json={"url": "https://www.example.com"})
    short_code = json.loads(create_response.data)["short_code"]

    # Now, try to access it
    response = client.get(f"/{short_code}")
    assert response.status_code == 302  # Redirect status code
    assert response.location == "https://www.example.com"


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"URL Shortener" in response.data
