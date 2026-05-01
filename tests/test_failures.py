import pytest


@pytest.fixture
def auth_headers(client):
    user = {
        "email": "failuser@example.com",
        "password": "StrongPass123"
    }

    client.post("/register", json=user)

    res = client.post(
        "/login",
        data={"username": user["email"], "password": user["password"]}
    )

    token = res.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


def test_invalid_token(client):
    res = client.get(
        "/tasks",
        headers={"Authorization": "Bearer invalid"}
    )
    assert res.status_code == 401


def test_invalid_payload(client, auth_headers):
    res = client.post(
        "/tasks",
        json={},
        headers=auth_headers
    )
    assert res.status_code in [400, 422]


def test_update_nonexistent(client, auth_headers):
    res = client.put(
        "/tasks/999",
        json={"title": "No Task"},
        headers=auth_headers
    )
    assert res.status_code in [404, 400]


def test_delete_nonexistent(client, auth_headers):
    res = client.delete(
        "/tasks/999",
        headers=auth_headers
    )
    assert res.status_code in [404, 400]


def test_cross_user_access(client):
    user1 = {"email": "u1@example.com", "password": "123456"}
    user2 = {"email": "u2@example.com", "password": "123456"}

    client.post("/register", json=user1)
    client.post("/register", json=user2)

    res1 = client.post("/login", data={"username": user1["email"], "password": user1["password"]})
    token1 = res1.json()["access_token"]

    res2 = client.post("/login", data={"username": user2["email"], "password": user2["password"]})
    token2 = res2.json()["access_token"]

    headers1 = {"Authorization": f"Bearer {token1}"}
    headers2 = {"Authorization": f"Bearer {token2}"}

    create = client.post("/tasks", json={"title": "User1 Task"}, headers=headers1)
    task_id = create.json()["id"]

    res = client.get(f"/tasks/{task_id}", headers=headers2)
    assert res.status_code in [403, 404]