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
            self.check_api_token(token.token, self.permissions.get('api.get_investments'), 'Get Investments')

            investments = self.database.get_investments()
            return JSONResponse(content=investments, status_code=200)

        @self.router.get('/', response_model=ReturnInvestment)
        async def get_investment(token: Token, investment: GetInvestment):
            self.check_api_token(token.token, self.permissions.get('api.get_investment'), 'Get Investment')

            investment = self.database.get_investment(investment.user)
            if investment:
                return JSONResponse(content=investment, status_code=200)
            raise HTTPException(status_code=404, detail="Investment does not exist")

        @self.router.post('/', response_model=None)
        async def update_investment(token: Token, investment: UpdateInvestment):
            self.check_api_token(token.token, self.permissions.get('api.update_investment'), 'Update Investment')

            investment = self.database.update_investment(investment.user, investment.given_apples)
            return JSONResponse(content=investment, status_code=200)
