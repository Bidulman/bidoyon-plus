from fastapi import HTTPException
from fastapi.responses import JSONResponse
from routers.router import Router

from models import (
    Token,
    ReturnInvestment,
    ReturnInvestments,
    GetInvestment,
    UpdateInvestment
)


class InvestmentsAPIRouter(Router):

    def __init__(self, utils):
        super().__init__(utils, '/investments')

    def methods(self):

        @self.router.get('/all', response_model=ReturnInvestments)
        async def get_investments(token: Token):
            self.check_token(token.token, 'MANAGER', 'Get Investments')

            investments = self.utils.database.get_investments()
            return JSONResponse(content=investments, status_code=200)

        @self.router.get('/', response_model=ReturnInvestment)
        async def get_investment(token: Token, investment: GetInvestment):
            self.check_token(token.token, 'MANAGER', 'Get Investment')

            investment = self.utils.database.get_investment(investment.user)
            if investment:
                return JSONResponse(content=investment, status_code=200)
            raise HTTPException(status_code=404, detail="Investment does not exist")

        @self.router.post('/', response_model=None)
        async def update_investment(token: Token, investment: UpdateInvestment):
            self.check_token(token.token, 'MANAGER', 'Update Investment')

            investment = self.utils.database.update_investment(investment.user, investment.given_apples)
            return JSONResponse(content=investment, status_code=200)
