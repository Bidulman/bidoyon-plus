from pydantic import BaseModel


class Squeeze(BaseModel):
    id: int
    juice: int
    used_apples: int


ReturnSqueeze = Squeeze


class ReturnSqueezes(BaseModel):
    squeezes: list[dict]


class GetSqueeze(BaseModel):
    id: int


class AddSqueeze(BaseModel):
    juice: int
    used_apples: int


class UpdateSqueeze(BaseModel):
    id: int
    juice: int = None
    used_apples: int = None


class RemoveSqueeze(BaseModel):
    id: int
