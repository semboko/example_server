from fastapi.testclient import TestClient

from db import database
from main import app
from tests.utils import create_user

client = TestClient(app)


def test_signup_success():
    login = "abcde"
    password = "123456"
    database.delete("user:" + login)

    res = client.post("/auth/signup", json={"login": login, "password": password})

    assert res.status_code == 200
    assert res.text == "true"

    database.delete("user:" + login)


def test_signup_fail():
    login = "abcde"
    password = "123456"
    database.delete("user:" + login)

    client.post("/auth/signup", json={"login": login, "password": password})

    res = client.post("/auth/signup", json={"login": login, "password": password})

    assert res.status_code == 400
    assert res.text != "true"

    database.delete("user:" + login)


def test_signin_success():
    login, password = "login", "password"
    create_user(client, login, password)
    res = client.post("/auth/signin", json={"login": login, "password": password})
    assert res.status_code == 200
    database.delete("user:" + login)


def test_signin_fail():
    login, password = "login", "password"
    database.delete("user:" + login)
    res = client.post("/auth/signin", json={"login": login, "password": password})
    assert res.status_code == 400
    database.delete("user:" + login)
