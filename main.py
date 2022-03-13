from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from os.path import exists
import requests

from utilities import utilities

from routers.app.app import AppRouter
from routers.api.api import APIRouter
from routers.cdn import CDNRouter

import logging
from uvicorn import run

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

utils = utilities.Utilities('config.yml', 'permissions.yml', 'messages.yml', 'token.txt')

app.include_router(AppRouter(utils).router)
app.include_router(APIRouter(utils).router)
app.include_router(CDNRouter(utils).router)

host = utils.config.get("application.host")
port = utils.config.get("application.port")


def check_updates():
    file = utils.config.get('version.file')
    url = utils.config.get('version.url')
    if not exists(file):
        logging.error(f"{file} does not exist. Update checker can't continue...")
        return
    try:
        response = requests.get(url)
        if response.status_code == 404:
            logging.error(f"{url} is reachable but unreadable.")
            return
        with open(file, 'r') as file:
            version = file.read()
            available_version = response.text
            if version == available_version:
                logging.info(f"Application is up to date ! (Version {version})")
            else:
                logging.warning(f"New version {available_version} is available ! (You have {version})")
    except ConnectionError:
        logging.error(f"{url} is not reachable.")
        return


if __name__ == "__main__":
    check_updates()
    logging.info(f"Enabling application with host '{host}' and port {port}.")
    run(app=app, host=host, port=port)
