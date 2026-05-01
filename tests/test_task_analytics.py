def test_task_analytics_flow(client):
    user = {
        "email": "analytics@example.com",
        "password": "StrongPass123"
    }

    client.post("/register", json=user)

    login = client.post(
        "/login",
        data={"username": user["email"], "password": user["password"]}
    )

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    client.post("/tasks", json={"title": "Task 1"}, headers=headers)
    client.post("/tasks", json={"title": "Task 2"}, headers=headers)

    res = client.get("/analytics", headers=headers)

    assert res.status_code == 200