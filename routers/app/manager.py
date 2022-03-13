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

            current_squeeze = self.database.get_current_squeeze_id()

            return self.template_response('manager.html', request, {'current_squeeze': current_squeeze}, token)

        @self.router.post('/addsqueeze')
        async def process_add_squeeze(request: Request):
            token = request.query_params.get('token')
            check = self.check_app_token(token, self.permissions.get('app.manager_page'), 'Add Squeeze (from Manager Page)')
            if isinstance(check, RedirectResponse):
                return check

            self.database.add_squeeze(0, 0)
            return self.redirect_response('/manager', [(self.messages.get('app.manager.squeeze_created'), 'success-message')], {'token': token})

        @self.router.post('/removesqueeze')
        async def process_remove_squeeze(request: Request, id: int = Form(...)):
            token = request.query_params.get('token')
            check = self.check_app_token(token, self.permissions.get('app.manager_page'), 'Remove Squeeze (from Manager Page)')
            if isinstance(check, RedirectResponse):
                return check

            if self.database.remove_squeeze(id):
                return self.redirect_response('/manager', [(self.messages.get('app.manager.squeeze_removed').format(id=id), 'success-message')], {'token': token})
            else:
                return self.redirect_response('/manager', [(self.messages.get('app.manager.squeeze_not_found').format(id=id), 'error-message')], {'token': token})

        @self.router.post('/updatesqueeze')
        async def process_update_squeeze(request: Request, id: int = Form(...), used_apples: int = Form(...), produced_juice: int = Form(...)):
            token = request.query_params.get('token')
            check = self.check_app_token(token, self.permissions.get('app.manager_page'), 'Update Squeeze (from Manager Page)')
            if isinstance(check, RedirectResponse):
                return check

            squeeze = self.database.get_squeeze(id)
            if not squeeze:
                return self.redirect_response('/manager', [(self.messages.get('app.manager.squeeze_not_found').format(id=id), 'error-message')], {'token': token})

            messages = []

            if used_apples != 0:
                given_apples = self.database.get_total_value('given_apples')
                if self.database.get_total_value('used_apples') + used_apples <= given_apples:
                    old_used_apples = squeeze['used_apples']
                    self.database.update_squeeze_used_apples(id, old_used_apples + used_apples)
                    messages.append((self.messages.get('app.manager.squeeze_used_apples_updated').format(id=id, used_apples=used_apples), 'success-message'))
                else:
                    messages.append((self.messages.get('app.manager.too_many_used_apples').format(given_apples=given_apples), 'error-message'))

            if produced_juice != 0:
                old_produced_juice = squeeze['juice']
                self.database.update_squeeze_juice(id, old_produced_juice + produced_juice)
                messages.append((self.messages.get('app.manager.squeeze_produced_juice_updated').format(id=id, produced_juice=produced_juice), 'success-message'))

            return self.redirect_response('/manager', messages, {'token': token})
