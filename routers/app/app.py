from fastapi import Request
from routers.router import Router

from routers.app.login import AppLoginRouter
from routers.app.admin import AppAdminRouter


class AppRouter(Router):

    def __init__(self, utils):
        super().__init__(utils, '')
        self.router.include_router(AppLoginRouter(utils).router)
        self.router.include_router(AppAdminRouter(utils).router)

    def methods(self):

        @self.router.get('/')
        async def app_index(request: Request):
            token = request.query_params.get('token')
            if token:
                return self.template_response('index.html', request, {'token': token})
            else:
                return self.template_response('index.html', request, {})

        @self.router.get('/contact')
        async def app_contact(request: Request):
            token = request.query_params.get('token')
            if token:
                return self.template_response('contact.html', request, {'token': token})
            else:
                return self.template_response('contact.html', request, {})

        @self.router.get('/view')
        async def app_contact(request: Request):
            token = request.query_params.get('token')
            if token:
                return self.template_response('view.html', request, {'token': token})
            else:
                return self.template_response('view.html', request, {})
