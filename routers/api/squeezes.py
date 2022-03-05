from fastapi import HTTPException
from fastapi.responses import JSONResponse
from routers.router import Router

from models import (
    Token,
    ReturnSqueeze,
    ReturnSqueezes,
    GetSqueeze,
    AddSqueeze,
    UpdateSqueeze,
    RemoveSqueeze
)


class SqueezesAPIRouter(Router):

    def __init__(self, utils):
        super().__init__(utils, '/squeezes')

    def methods(self):

        @self.router.get('/all', response_model=ReturnSqueezes)
        async def get_squeezes(token: Token):
            self.check_token(token.token, self.permissions.get('api.get_squeezes'), 'Get Squeezes')

            squeezes = self.database.get_squeezes()
            return JSONResponse(content=squeezes, status_code=200)

        @self.router.get('/', response_model=ReturnSqueeze)
        async def get_squeeze(token: Token, squeeze: GetSqueeze):
            self.check_token(token.token, self.permissions.get('api.get_squeeze'), 'Get Squeeze')

            squeeze = self.database.get_squeeze(squeeze.id)
            if squeeze:
                return JSONResponse(content=squeeze, status_code=200)
            raise HTTPException(status_code=404, detail="Squeeze does not exist")

        @self.router.put('/', response_model=None)
        async def add_squeeze(token: Token, squeeze: AddSqueeze):
            self.check_token(token.token, self.permissions.get('api.add_squeeze'), 'Add Squeeze')

            if self.database.add_squeeze(squeeze.juice, squeeze.used_apples):
                return JSONResponse(content={}, status_code=200)
            raise HTTPException(status_code=409, detail="Squeeze already exists")

        @self.router.post('/', response_model=ReturnSqueeze)
        async def update_squeeze(token: Token, squeeze: UpdateSqueeze):
            self.check_token(token.token, self.permissions.get('api.update_squeeze'), 'Update Squeeze')

            if not self.database.get_squeeze(squeeze.id):
                raise HTTPException(status_code=404, detail="Squeeze does not exist")

            if squeeze.juice:
                self.database.update_squeeze_juice(squeeze.id, squeeze.juice)
            if squeeze.used_apples:
                self.database.update_squeeze_used_apples(squeeze.id, squeeze.used_apples)

            squeeze = self.database.get_squeeze(squeeze.id)
            return JSONResponse(content=squeeze, status_code=200)

        @self.router.delete('/', response_model=ReturnSqueeze)
        async def remove_squeeze(token: Token, squeeze: RemoveSqueeze):
            self.check_token(token.token, self.permissions.get('api.remove_squeezes'), 'Remove Squeeze')

            if self.database.remove_squeeze(squeeze.id):
                return JSONResponse(content={'id': squeeze.id}, status_code=200)
            raise HTTPException(status_code=404, detail="Squeeze does not exist")
