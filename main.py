from fastapi import FastAPI
from utilities import utilities

from routers.api.api import APIRouter
from routers.cdn import CDNRouter

import logging
from uvicorn import run

app = FastAPI()

utils = utilities.Utilities('config.yml')

app.include_router(APIRouter(utils).router)
app.include_router(CDNRouter(utils).router)

if __name__ == "__main__":
    host = utils.config.get("application.host")
    port = utils.config.get("application.port")
    logging.info(f"Enabling application with host '{host}' and port {port}.")
    run(app=app, host=host, port=port)
