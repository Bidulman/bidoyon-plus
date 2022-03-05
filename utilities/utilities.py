from .config import Config
from .database import Database

from fastapi.templating import Jinja2Templates

import logging
import datetime


class Utilities:

    def __init__(self, config_path, permissions_path, messages_path):
        self.create_config(config_path)
        self.create_permissions(permissions_path)
        self.create_messages(messages_path)
        self.create_logger()
        self.create_database()
        self.create_templates()

    def create_config(self, config_path):
        self.config = Config(config_path)

    def create_permissions(self, permissions_path):
        self.permissions = Config(permissions_path)

    def create_messages(self, messages_path):
        self.messages = Config(messages_path)

    def create_logger(self):
        logging.basicConfig(
            level=logging.INFO,
            format=self.config.get("logger.format"),
            handlers=[
                logging.FileHandler(self.config.get("logger.file")),
                logging.StreamHandler()
            ]
        )
        logging.info(f"{10*'-'} STARTING AT {datetime.datetime.now()} {10*'-'}")

    def create_database(self):
        self.database = Database(self)

    def create_templates(self):
        self.templates = Jinja2Templates(directory="templates")
