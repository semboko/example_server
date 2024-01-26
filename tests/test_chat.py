from fastapi.testclient import TestClient

from db import database
from main import app
from tests.utils import create_user

client = TestClient(app)


def test_get_user_list_unauthorized():
    res = client.get("/chat/contacts", headers={"token": "11111111"})
    assert res.status_code == 401


def test_get_user_list():
    login1 = "login1"
    login2 = "login2"
    create_user(client, login1)
    create_user(client, login2)

    res = client.post("/auth/signin", json={"login": login1, "password": "123456"})

    token = res.json()
    res = client.get("/chat/contacts", headers={"token": token})

    assert res.status_code == 200
    assert login1 in res.json()
    assert login2 in res.json()

    database.delete("user:" + login1)
    database.delete("user:" + login2)


def test_change_friends():
    login1 = "login1"
    login2 = "login2"
    create_user(client, login1)
    create_user(client, login2)

    res = client.post("/auth/signin", json={"login": login1, "password": "123456"})

    token = res.json()

    res = client.post("/chat/friends", json={"friend_id": login2}, headers={"token": token})

    assert res.status_code == 200

    res = client.get("/chat/friends", headers={"token": token})

    assert res.status_code == 200
    assert res.json()[0] == login2

    res = client.post("/chat/friends/delete", headers={"token": token}, json={"friend_id": login2})

    assert res.status_code == 200

    res = client.get("/chat/friends", headers={"token": token})

    assert res.status_code == 200
    assert len(res.json()) == 0

    database.delete("user:" + login1)
    database.delete("user:" + login2)
