from fastapi import HTTPException
from fastapi.responses import JSONResponse
from routers.router import Router

from models import (
    Token,
    ReturnTotal,
    GetTotal,
    UpdateTotal
)


class TotalsAPIRouter(Router):

    def __init__(self, utils):
        super().__init__(utils, '/totals')

    def methods(self):

        @self.router.get('/', response_model=ReturnTotal)
        async def get_total(token: Token, total: GetTotal):
            self.check_token(token.token, 'MANAGER', 'Get Total')

            total = self.utils.database.get_total(total.of)
            if total:
                return JSONResponse(content=total, status_code=200)
            raise HTTPException(status_code=404, detail="Total does not exist")

        @self.router.post('/', response_model=None)
        async def update_total(token: Token, total: UpdateTotal):
            self.check_token(token.token, 'MANAGER', 'Update Total')

            total = self.utils.database.update_total(total.of, total.value, total.addition)
            return JSONResponse(content=total, status_code=200)
