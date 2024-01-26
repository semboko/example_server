from pydantic import BaseModel
from db import database


class User(BaseModel):
    username: str
    hashed_password: str

    prefix: str = "user:"

    def exists(self) -> bool:
        res = database.get(self.prefix + self.username)
        return res is not None

    def save(self) -> None:
        key = self.prefix + self.username
        value = self.hashed_password
        database.set(key, value)
