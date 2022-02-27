from pydantic import BaseModel


class Token(BaseModel):
    token: str


class ReturnTokens(BaseModel):
    tokens: list[dict]


class ReturnToken(BaseModel):
    user: int
    permission: str
    token: str


class GetTokenByToken(BaseModel):
    token: str


class GetTokenByUser(BaseModel):
    user: int


class GenerateToken(BaseModel):
    user: int
    permission: str = None
