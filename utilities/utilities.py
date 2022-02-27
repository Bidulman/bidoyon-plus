from .config import Config
from .database import Database

import logging
import datetime


class Utilities:

    def __init__(self, config_path):
        self.create_config(config_path)
        self.create_logger()
        self.create_database()

    def create_config(self, config_path):
        self.config = Config(config_path)

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
