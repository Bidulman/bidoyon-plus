from fastapi import HTTPException
from fastapi.responses import JSONResponse
from routers.router import Router

from models import (
    Token,
    ReturnTokens,
    ReturnToken,
    GetTokenByUser,
    GenerateToken
)


class TokensAPIRouter(Router):

    def __init__(self, utils):
        super().__init__(utils, '/tokens')

    def methods(self):

        @self.router.get('/all', response_model=ReturnTokens)
        async def get_tokens(token: Token):
            self.check_token(token.token, 'SUPER', 'Get Tokens')

            tokens = self.utils.database.get_tokens()
            return JSONResponse(content=tokens, status_code=200)

        @self.router.get('/', response_model=ReturnToken)
        async def get_token(token: Token, gettoken: GetTokenByUser):
            self.check_token(token.token, 'SUPER', 'Get Token')

            token = self.utils.database.get_token_by_user(gettoken.user)
            if token:
                return JSONResponse(content=token, status_code=200)
            raise HTTPException(status_code=404, detail="Token does not exist")

        @self.router.post('/', response_model=None)
        async def generate_token(token: Token, generatetoken: GenerateToken):
            self.check_token(token.token, 'SUPER', 'Generate Token')

            if generatetoken.permission:
                token = self.utils.database.generate_token(generatetoken.user, generatetoken.permission)
            else:
                try:
                    user = self.utils.database.get_user_by_id(generatetoken.user)
                except KeyError:
                    raise HTTPException(status_code=422, detail="User must be existing if 'permission' is unfilled")
                token = self.utils.database.generate_token(user['id'], user['permission'])

            token = self.utils.database.get_token_by_token(token)
            return JSONResponse(content=token, status_code=200)
