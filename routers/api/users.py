from fastapi import HTTPException
from fastapi.responses import JSONResponse
from routers.router import Router

from models import (
    Token,
    ReturnUser,
    ReturnUsers,
    GetUserByID,
    AddUser,
    UpdateUser,
    RemoveUser
)


class UsersAPIRouter(Router):

    def __init__(self, utils):
        super().__init__(utils, '/users')

    def methods(self):

        @self.router.get('/all', response_model=ReturnUsers)
        async def get_users(token: Token):
            self.check_api_token(token.token, self.permissions.get('api.get_users'), 'Get Users')

            users = self.database.get_users()
            return JSONResponse(content=users, status_code=200)

        @self.router.get('/', response_model=ReturnUser)
        async def get_user(token: Token, user: GetUserByID):
            self.check_api_token(token.token, self.permissions.get('api.get_user'), 'Get User')

            user = self.database.get_user_by_id(user.id)
            if user:
                return JSONResponse(content=user, status_code=200)
            raise HTTPException(status_code=404, detail="User does not exist")

        @self.router.put('/', response_model=ReturnUser)
        async def add_user(token: Token, user: AddUser):
            self.check_api_token(token.token, self.permissions.get('api.add_user'), 'Add User')

            if self.database.add_user(user.name, user.permission, user.password):
                user = self.database.get_user_by_name(user.name)
                return JSONResponse(content=user, status_code=200)
            raise HTTPException(status_code=409, detail="User already exists")

        @self.router.post('/', response_model=ReturnUser)
        async def update_user(token: Token, user: UpdateUser):
            self.check_api_token(token.token, self.permissions.get('api.update_user'), 'Update User')

            if not self.database.get_user_by_id(user.id):
                raise HTTPException(status_code=404, detail="User does not exist")

            if user.name:
                if not self.database.update_user_name(user.id, user.name):
                    HTTPException(status_code=409, detail="This name is already used")
            if user.permission:
                self.database.update_user_permission(user.id, user.permission)
            if user.password:
                self.database.update_user_password(user.id, user.password)
            user = self.database.get_user_by_id(user.id)
            return JSONResponse(content=user, status_code=200)

        @self.router.delete('/', response_model=ReturnUser)
        async def remove_user(token: Token, user: RemoveUser):
            self.check_api_token(token.token, self.permissions.get('api.remove_user'), 'Remove User')

            if self.database.remove_user(user.id):
                return JSONResponse(content={'id': user.id}, status_code=200)
            raise HTTPException(status_code=404, detail="User does not exist")
