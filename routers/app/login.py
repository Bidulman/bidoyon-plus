from fastapi import Request, Form
from routers.router import Router


class AppLoginRouter(Router):

    def __init__(self, utils):
        super().__init__(utils, '')

    def methods(self):

        @self.router.get('/login')
        async def get_login(request: Request):
            return self.template_response('login.html', request, {})

        @self.router.post('/login')
        async def post_login(username: str = Form(...), password: str = Form(...)):
            user = self.database.get_user_by_name(username)
            if not user or user['password'] != password:
                return self.redirect_response('/login', [("Vous n'avez pas pu vous connecter car les identifiants sont inconnus.", 'error-message')])

            token = self.database.generate_token(user['id'], user['permission'])
            return self.redirect_response(messages=[("Vous avez été connecté à l'application !", 'success-message')], params={'token': token})
