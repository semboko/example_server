from typing import Annotated

from fastapi import Header, HTTPException, status

from db import database

TokenHeader = Annotated[str, Header()]


def auth(token: TokenHeader) -> str:
    username = database.get("session:" + token)
    print(username)
    if username is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return username
