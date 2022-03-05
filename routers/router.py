from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
import logging


class Router:

    def __init__(self, utils, prefix):
        self.utils = utils
        self.config = utils.config
        self.permissions = utils.permissions
        self.messages = utils.messages
        self.database = utils.database
        self.router = APIRouter(prefix=prefix)
        self.methods()

    def check_token(self, token, needed_permission, action):
        token = self.utils.database.get_token_by_token(token)
        if not token:
            logging.warning(f"A person tried to use a bad token in the API to : {action}.")
            raise HTTPException(status_code=403, detail="You must to have a valid token")

        try:
            token_permission_code = self.utils.config.get(f"permissions.{token['permission']}")
        except KeyError:
            logging.error(f"Permission {token['permission']} does not exist.")
            raise HTTPException(status_code=500, detail="An error has occurred with permissions")
        try:
            needed_permission_code = self.utils.config.get(f"permissions.{needed_permission}")
        except KeyError:
            logging.error(f"Permission {needed_permission} does not exist.")
            raise HTTPException(status_code=500, detail="An error has occurred with permissions")

        if token_permission_code > needed_permission_code:
            logging.warning(f"User {token['user']} tried to : {action} (require permission {needed_permission}), but he has permission {token['permission']}.")
            raise HTTPException(status_code=403, detail="You must to have a valid token")

        logging.info(f"User {token['user']} successfully executed the action {action} (require {needed_permission}, he has {token['permission']}).")

    def template_response(self, template, request, data):
        data['request'] = request
        data['app_name'] = self.utils.config.get('application.name')
        data['address'] = self.utils.config.get('application.external_address')
        data['messages'] = self.get_messages(request)
        # Contact
        data['contact_name'] = self.utils.config.get('contact.name')
        data['contact_github'] = self.utils.config.get('contact.github')
        data['contact_address'] = self.utils.config.get('contact.mail.address')
        data['contact_subject'] = self.utils.config.get('contact.mail.subject')
        data['contact_body'] = self.utils.config.get('contact.mail.body')

        return self.utils.templates.TemplateResponse(template, data)

    def redirect_response(self, url="", messages=None, params=None):
        url = self.utils.config.get('application.external_address') + url
        if not messages:
            messages = []
        url += "?messages="
        for message in messages:
            url += f"{message[0]}_{message[1]};"
        if not params:
            params = {}
        for param in params.keys():
            url += f"&{param}={params[param]}"
        return RedirectResponse(url, status_code=302)

    def get_messages(self, request):
        request_messages = request.query_params.get('messages')
        messages = [(message, 'info-message') for message in self.utils.config.get('messages')]

        if not request_messages:
            return messages

        for message in request_messages.split(';'):
            if '_' in message:
                messages.append(message.split('_'))

        return messages

    def methods(self):
        pass
