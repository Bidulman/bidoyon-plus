from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    permission: str
    password: str


class ReturnUser(BaseModel):
    id: int
    name: str
    permission: str


class ReturnUsers(BaseModel):
    users: list[dict]


class GetUserByID(BaseModel):
    id: int


class GetUserByName(BaseModel):
    name: str


class AddUser(BaseModel):
    name: str
    permission: str
    password: str


class UpdateUser(BaseModel):
    id: int
    name: str = None
    permission: str = None
    password: str = None


class RemoveUser(BaseModel):
    id: int
