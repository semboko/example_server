from fastapi.testclient import TestClient

from db import database


def create_user(client: TestClient, login: str = "login", password: str = "123456") -> None:
    database.delete("user:" + login)
    client.post("/auth/signup", json={"login": login, "password": password})
