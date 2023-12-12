from pydantic import BaseModel


class Credentials(BaseModel):
    login: str
    password: str
