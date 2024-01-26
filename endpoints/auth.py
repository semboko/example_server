from hashlib import sha256
from secrets import token_hex

from fastapi import APIRouter, HTTPException, status
from managers.auth import AuthManager, AuthError

from db import database
from schema import Credentials

router = APIRouter(prefix="/auth")


@router.post("/signup")
def signup(body: Credentials) -> bool:
    login, password = body.login, body.password

    am = AuthManager()
    try:
        am.signup(login, password)
    except AuthError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
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

    res = database.set("session:" + token, body.login, ex=24 * 60 * 60)
    return token
