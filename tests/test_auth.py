import pytest


@pytest.fixture
def user_data():
    return {
        "email": "testuser@example.com",
        "password": "StrongPass123"
    }


def test_register_success(client, user_data):
    res = client.post("/register", json=user_data)
    assert res.status_code in [200, 201]


def test_register_duplicate(client, user_data):
    client.post("/register", json=user_data)
    res = client.post("/register", json=user_data)
    assert res.status_code in [400, 409]


def test_login_success(client, user_data):
    client.post("/register", json=user_data)

    res = client.post(
        "/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"]
        }
    )

    assert res.status_code == 200
    assert "access_token" in res.json()


def test_login_invalid_password(client, user_data):
    client.post("/register", json=user_data)

    res = client.post(
        "/login",
        data={
            "username": user_data["email"],
            "password": "wrongpass"
        }
    )

    assert res.status_code == 401


def test_login_nonexistent_user(client):
    res = client.post(
        "/login",
        data={
            "username": "nouser@example.com",
            "password": "123"
        }
    )

    assert res.status_code == 401