from pydantic import BaseModel


class Credentials(BaseModel):
    login: str
    password: str


class FriendRequest(BaseModel):
    friend_id: str
