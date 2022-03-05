import requests
import json


class RawClient:

    def __init__(self, address: str, token: str):
        self.set_address(address)
        self.set_token(token)

    def set_address(self, address: str):
        address = address.strip(' ').strip('/')
        if not address:
            address = "http://localhost:8080"
        self.address = address

    def set_token(self, token: str):
        self.token = token

    def set_base_router(self, base_router: str):
        self.base_router = base_router

    def request(self, method: str, path: str, data: dict = None, params: dict = None):
        if not data:
            data = {}
        if not params:
            params = {}

        if data:
            data['token'] = {'token': self.token}
        else:
            data['token'] = self.token

        if self.base_router:
            return requests.request(method, self.address+self.base_router+path, data=json.dumps(data), params=params)
        else:
            return requests.request(method, self.address+path, data=json.dumps(data), params=params)
