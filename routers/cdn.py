from fastapi import HTTPException
from fastapi.responses import FileResponse
from routers.router import Router

from os.path import exists


class CDNRouter(Router):

    def __init__(self, utils):
        super().__init__(utils, '/cdn')

    def methods(self):

        @self.router.get('/{resource}')
        async def cdn(resource: str):
            path = f'cdn/{resource}'
            if exists(path):
                return FileResponse(path)
            else:
                raise HTTPException(status_code=404)
