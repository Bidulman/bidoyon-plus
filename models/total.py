from pydantic import BaseModel


class Total(BaseModel):
    of: str
    value: int


ReturnTotal = Total


class GetTotal(BaseModel):
    of: str


class UpdateTotal(BaseModel):
    of: str
    value: int
    addition: bool
