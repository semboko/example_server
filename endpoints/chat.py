from typing import List

from fastapi import APIRouter, Depends

from db import database
from endpoints.deps import auth
from schema import FriendRequest


router = APIRouter(prefix="/chat")


@router.get("/contacts")
def get_contacts(_: str = Depends(auth)) -> List[str]:
    keys = database.keys("user:*")
    result = []

    for key in keys:
        result.append(key[5:])

    return result


@router.get("/friends")
def get_friends(username: str = Depends(auth)):
    result = database.smembers("friends:" + username)
    return list(result)


@router.post("/friends")
def add_friend(
    data: FriendRequest,
    username: str = Depends(auth),
):
    database.sadd("friends:" + username, data.friend_id)


@router.post("/friends/delete")
def delete_friend(data: FriendRequest, username: str = Depends(auth)):
    database.srem("friends:" + username, data.friend_id)
