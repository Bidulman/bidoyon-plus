from routers.router import Router

from models import (
    Token,
    Config
)


class ConfigsAPIRouter(Router):

    def __init__(self, utils):
        super().__init__(utils, '/configs')

    def methods(self):

        @self.router.post('/')
        async def reload_config(token: Token, config: Config):
            self.check_api_token(token.token, self.permissions.get('api.reload_config'), 'Reload Config')

            if config.name == "config":
                self.config.load()
            elif config.name == "permissions":
                self.permissions.load()
            elif config.name == "messages":
                self.messages.load()
