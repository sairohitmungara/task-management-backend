import pytest


@pytest.fixture
def auth_headers(client):
    user = {
        "email": "taskuser@example.com",
        "password": "StrongPass123"
    }

    client.post("/register", json=user)

    res = client.post(
        "/login",
        data={"username": user["email"], "password": user["password"]}
    )

    token = res.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


def test_create_task(client, auth_headers):
    res = client.post(
        "/tasks",
        json={"title": "Test Task"},
        headers=auth_headers
    )
    assert res.status_code == 200


def test_get_tasks(client, auth_headers):
    res = client.get("/tasks", headers=auth_headers)
    assert res.status_code == 200


def test_update_task(client, auth_headers):
    create = client.post("/tasks", json={"title": "Task"}, headers=auth_headers)
    task_id = create.json()["id"]

    res = client.put(f"/tasks/{task_id}", json={"title": "Updated"}, headers=auth_headers)
    assert res.status_code == 200


def test_delete_task(client, auth_headers):
    create = client.post("/tasks", json={"title": "Task"}, headers=auth_headers)
    task_id = create.json()["id"]

    res = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert res.status_code == 200


def test_unauthorized_access(client):
    res = client.get("/tasks")
    assert res.status_code == 401