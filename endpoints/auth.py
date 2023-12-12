from hashlib import sha256
from secrets import token_hex

from fastapi import APIRouter, HTTPException, status

from db import database
from schema import Credentials

router = APIRouter(prefix="/auth")


@router.post("/signup")
def signup(body: Credentials) -> bool:
    login, password = body.login, body.password
    res = database.get("user:" + login)
    if res is not None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    hashed_password = sha256(password.encode("UTF-8")).hexdigest()
    key = "user:" + login
    value = hashed_password
    database.set(key, value)
    return True


@router.post("/signin")
def signin(body: Credentials) -> str:
    res = database.get("user:" + body.login)
    if res is None:
        raise HTTPException(400, "Login was not found")
    hash_password = sha256(body.password.encode("UTF-8")).hexdigest()
    if res != hash_password:
        raise HTTPException(400, "Wrong password")

    token = token_hex(16)

    database.set("session:" + token, body.login)

    return token
