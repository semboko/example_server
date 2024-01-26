from managers.base import BaseManager
from db import database
from hashlib import sha256
from model.user import User


class AuthError(Exception):
    pass


class AuthManager(BaseManager):
    def signup(self, username: str, password: str) -> None:
        hashed_password = sha256(password.encode("UTF-8")).hexdigest()
        new_user = User(username=username, hashed_password=hashed_password)

        if new_user.exists():
            raise AuthError()

        new_user.save()
