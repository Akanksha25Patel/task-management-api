def get_token(client, username):
    # हर बार unique user create होगा
    client.post("/auth/register", json={
        "username": username,
        "password": "1234"
    })

    res = client.post("/auth/login", json={
        "username": username,
        "password": "1234"
    })

    return res.get_json()["token"]


def test_create_task(client):
    token = get_token(client, "user1")

    response = client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "Testing"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_get_tasks(client):
    token = get_token(client, "user2")   # 🔥 अलग user

    client.post(
        "/tasks/",
        json={"title": "Task", "description": "Test"},
        headers={"Authorization": f"Bearer {token}"}
    )

    response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_unauthorized_access(client):
    response = client.get("/tasks/")
    assert response.status_code == 401