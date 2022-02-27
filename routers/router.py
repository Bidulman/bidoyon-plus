from fastapi import APIRouter, HTTPException
import logging


class Router:

    def __init__(self, utils, prefix):
        self.utils = utils
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

    def methods(self):
        pass
