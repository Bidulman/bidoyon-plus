from fastapi import Request, Form
from fastapi.responses import RedirectResponse
from routers.router import Router


class AppAdminRouter(Router):

    def __init__(self, utils):
        super().__init__(utils, '/admin')

    def methods(self):

        @self.router.get('/')
        async def admin(request: Request):
            token = request.query_params.get('token')
            check = self.check_app_token(token, self.permissions.get('app.admin_page'), 'Access Admin Page')
            if isinstance(check, RedirectResponse):
                return check

            return self.template_response('admin.html', request, {}, token)

        @self.router.post('/adduser')
        async def process_add_user(request: Request, username: str = Form(...), password: str = Form(...), permission: str = Form(...)):
            token = request.query_params.get('token')
            check = self.check_app_token(token, self.permissions.get('app.admin_page'), 'Add User (from Admin Page)')
            if isinstance(check, RedirectResponse):
                return check

            if self.database.add_user(username, permission, password):
                user = self.database.get_user_by_name(username)
                return self.redirect_response('/admin', [(self.messages.get('app.admin.user_created').format(id=user['id'], name=user['name'], password=user['password'], permission=user['permission']), 'success-message')], {'token': token})
            else:
                return self.redirect_response('/admin', [(self.messages.get('app.admin.user_already_exists').format(name=username), 'error-message')], {'token': token})

        @self.router.post('/removeuser')
        async def process_remove_user(request: Request, id: str = Form(...)):
            token = request.query_params.get('token')
            check = self.check_app_token(token, self.permissions.get('app.admin_page'), 'Remove User (from Admin Page)')
            if isinstance(check, RedirectResponse):
                return check

            try:
                user_id = int(id)
                removed = self.database.remove_user(user_id)
            except ValueError:
                user = self.database.get_user_by_name(id)
                if user:
                    removed = self.database.remove_user(user['id'])
                else:
                    removed = False

            if removed:
                return self.redirect_response('/admin', [(self.messages.get('app.admin.user_removed').format(id=id), 'success-message')], {'token': token})
            else:
                return self.redirect_response('/admin', [(self.messages.get('app.admin.user_not_found').format(id=id), 'error-message')], {'token': token})

        @self.router.post('/updateuser')
        async def process_update_user(request: Request, id: str = Form(...), username: str = Form(...), password: str = Form(...), permission: str = Form(...)):
            token = request.query_params.get('token')
            check = self.check_app_token(token, self.permissions.get('app.admin_page'), 'Update User (from Admin Page)')
            if isinstance(check, RedirectResponse):
                return check

            username = None if username == "None" else username
            password = None if password == "None" else password
            permission = None if permission == "None" else permission

            try:
                user_id = int(id)
            except ValueError:
                user = self.database.get_user_by_name(id)
                if user:
                    user_id = user['id']
                else:
                    user_id = None

            if not user_id or not self.database.get_user_by_id(user_id):
                return self.redirect_response('/admin', [(self.messages.get('app.admin.user_not_found').format(id=id), 'error-message')], {'token': token})

            messages = []

            if username:
                boole = self.database.update_user_name(user_id, username)
                if boole:
                    messages.append((self.messages.get('app.admin.user_updated_name').format(id=id, name=username), 'success-message'))
                else:
                    messages.append((self.messages.get('app.admin.user_already_exists').format(name=username), 'error-message'))

            if password:
                self.database.update_user_password(user_id, password)
                messages.append((self.messages.get('app.admin.user_updated_password').format(id=id, password=password), 'success-message'))

            if permission:
                self.database.update_user_permission(user_id, permission)
                messages.append((self.messages.get('app.admin.user_updated_permission').format(id=id, permission=permission), 'success-message'))

            return self.redirect_response('/admin', messages, {'token': token})

        @self.router.post('/reloadconfig')
        async def process_reload_config(request: Request, name: str = Form(...)):
            token = request.query_params.get('token')
            check = self.check_app_token(token, self.permissions.get('app.admin_page'), 'Reload Config (from Admin Page)')
            if isinstance(check, RedirectResponse):
                return check

            if name == "config":
                self.config.load()
            elif name == "permissions":
                self.permissions.load()
            elif name == "messages":
                self.messages.load()

            return self.redirect_response('/admin', [(self.messages.get('app.admin.config_reloaded').format(name=name), 'success-message')], {'token': token})
