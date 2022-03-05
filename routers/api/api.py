from fastapi.responses import PlainTextResponse
from routers.router import Router

from routers.api.users import UsersAPIRouter
from routers.api.squeezes import SqueezesAPIRouter
from routers.api.investments import InvestmentsAPIRouter
from routers.api.tokens import TokensAPIRouter
from routers.api.totals import TotalsAPIRouter
from routers.api.configs import ConfigsAPIRouter


class APIRouter(Router):

    def __init__(self, utils):
        super().__init__(utils, '/api')
        self.router.include_router(UsersAPIRouter(utils).router)
        self.router.include_router(SqueezesAPIRouter(utils).router)
        self.router.include_router(InvestmentsAPIRouter(utils).router)
        self.router.include_router(TokensAPIRouter(utils).router)
        self.router.include_router(TotalsAPIRouter(utils).router)
        self.router.include_router(ConfigsAPIRouter(utils).router)

    def methods(self):

        @self.router.get('/')
        async def api_index():
            return PlainTextResponse("Welcome on the API !", 200)
