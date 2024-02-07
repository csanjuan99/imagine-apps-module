from pydantic import BaseModel
from .Task import Task


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    repeat_password: str


class User(UserBase):
    id: int
    password: str
    tasks: list[Task] = []

    class Config:
        from_attributes = True
