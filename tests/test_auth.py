def test_register(client):
    response = client.post("/auth/register", json={
        "username": "user_test1",   # 🔥 change
        "password": "1234"
    })

    assert response.status_code == 200


def test_login(client):
    client.post("/auth/register", json={
        "username": "user_test2",   # 🔥 change
        "password": "1234"
    })

    response = client.post("/auth/login", json={
        "username": "user_test2",
        "password": "1234"
    })

    assert response.status_code == 200