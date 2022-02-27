import requests
import json


class RawClient:

    def __init__(self, address, token):
        self.set_address(address)
        self.set_token(token)

    def set_address(self, address: str):
        self.address = address.strip(' ').strip('/')

    def set_token(self, token):
        self.token = token

    def set_base_router(self, base_router):
        self.base_router = base_router

    def request(self, method, path, data=None, params=None):
        if not data:
            data = {}
        if not params:
            params = {}

        if self.token:
            if data:
                data['token'] = {'token': self.token}
            else:
                data['token'] = self.token

        if self.base_router:
            return requests.request(method, self.address+self.base_router+path, data=json.dumps(data), params=params)
        else:
            return requests.request(method, self.address+path, data=json.dumps(data), params=params)
