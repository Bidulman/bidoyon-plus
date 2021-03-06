from fastapi import Request
from routers.router import Router

from routers.app.login import AppLoginRouter
from routers.app.admin import AppAdminRouter
from routers.app.manager import AppManagerRouter


class AppRouter(Router):

    def __init__(self, utils):
        super().__init__(utils, '')
        self.router.include_router(AppLoginRouter(utils).router)
        self.router.include_router(AppAdminRouter(utils).router)
        self.router.include_router(AppManagerRouter(utils).router)

    def methods(self):

        @self.router.get('/')
        async def app_index(request: Request):
            token = request.query_params.get('token') or ""
            return self.template_response('index.html', request, {}, token)

        @self.router.get('/contact')
        async def app_contact(request: Request):
            token = request.query_params.get('token') or ""
            return self.template_response('contact.html', request, {}, token)

        @self.router.get('/view')
        async def app_contact(request: Request):
            token = request.query_params.get('token') or ""
            return self.template_response('view.html', request, {}, token)
