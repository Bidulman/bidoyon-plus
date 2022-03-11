from fastapi import Request, Form
from fastapi.responses import RedirectResponse
from routers.router import Router


class AppManagerRouter(Router):

    def __init__(self, utils):
        super().__init__(utils, '/manager')

    def methods(self):

        @self.router.get('/')
        async def manager(request: Request):
            token = request.query_params.get('token')
            check = self.check_app_token(token, self.permissions.get('app.manager_page'), 'Access Manager Page')
            if isinstance(check, RedirectResponse):
                return check

            return self.template_response('manager.html', request, {}, token)
