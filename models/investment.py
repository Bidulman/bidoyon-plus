from pydantic import BaseModel


class Investment(BaseModel):
    user: int
    given_apples: int


class ReturnInvestments(BaseModel):
    investments: list[dict]


ReturnInvestment = Investment


class GetInvestment(BaseModel):
    user: int


UpdateInvestment = Investment
