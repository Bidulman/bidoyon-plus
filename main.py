from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from utilities import utilities

from routers.app.app import AppRouter
from routers.api.api import APIRouter
from routers.cdn import CDNRouter

import logging
from uvicorn import run

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

utils = utilities.Utilities('config.yml', 'permissions.yml', 'messages.yml')

app.include_router(AppRouter(utils).router)
app.include_router(APIRouter(utils).router)
app.include_router(CDNRouter(utils).router)

if __name__ == "__main__":
    host = utils.config.get("application.host")
    port = utils.config.get("application.port")
    logging.info(f"Enabling application with host '{host}' and port {port}.")
    run(app=app, host=host, port=port)
