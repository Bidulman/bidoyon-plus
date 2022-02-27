from .rawclient import RawClient


class Client(RawClient):

    def __init__(self, address, token):
        super().__init__(address, token)

    # Users

    def get_users(self):
        self.set_base_router('/api')
        return self.request('get', '/users/all')

    def get_user(self, id):
        self.set_base_router('/api')
        return self.request('get', '/users', data={'user': {'id': id}})

    def add_user(self, name, permission, password):
        self.set_base_router('/api')
        return self.request('put', '/users', data={'user': {'name': name, 'permission': permission, 'password': password}})

    def remove_user(self, id):
        self.set_base_router('/api')
        return self.request('delete', '/users', data={'user': {'id': id}})

    def update_user_name(self, id, name):
        self.set_base_router('/api')
        return self.request('post', '/users',data={'user': {'id': id, 'name': name}})

    def update_user_permission(self, id, permission):
        self.set_base_router('/api')
        return self.request('post', '/users',data={'user': {'id': id, 'permission': permission}})

    def update_user_password(self, id, password):
        self.set_base_router('/api')
        return self.request('post', '/users',data={'user': {'id': id, 'password': password}})

    # Squeezes

    def get_squeezes(self):
        self.set_base_router('/api')
        return self.request('get', '/squeezes/all')

    def get_squeeze(self, id):
        self.set_base_router('/api')
        return self.request('get', '/squeezes', data={'squeeze': {'id': id}})

    def add_squeeze(self, juice, used_apples):
        self.set_base_router('/api')
        return self.request('put', '/squeezes', data={'squeeze': {'juice': juice, 'used_apples': used_apples}})

    def remove_squeeze(self, id):
        self.set_base_router('/api')
        return self.request('delete', '/squeezes', data={'squeeze': {'id': id}})

    def update_squeeze_juice(self, id, juice):
        self.set_base_router('/api')
        return self.request('post', '/squeezes', data={'squeeze': {'id': id, 'juice': juice}})

    def update_squeeze_used_apples(self, id, used_apples):
        self.set_base_router('/api')
        return self.request('post', '/squeezes', data={'squeeze': {'id': id, 'used_apples': used_apples}})

    # Investments

    def get_investments(self):
        self.set_base_router('/api')
        return self.request('get', '/investments/all')

    def get_investment(self, user):
        self.set_base_router('/api')
        return self.request('get', '/investments', data={'investment': {'user': user}})

    def update_investment(self, user, given_apples):
        self.set_base_router('/api')
        return self.request('post', '/investments', data={'investment': {'user': user, 'given_apples': given_apples}})

    # Tokens

    def get_tokens(self):
        self.set_base_router('/api')
        return self.request('get', '/tokens/all')

    def get_token(self, user):
        self.set_base_router('/api')
        return self.request('get', '/tokens', data={'gettoken': {'user': user}})

    def generate_token(self, user, permission):
        self.set_base_router('/api')
        return self.request('post', '/tokens', data={'generatetoken': {'user': user, 'permission': permission}})

    # Totals

    def get_total(self, of):
        self.set_base_router('/api')
        return self.request('get', '/totals', data={'total': {'of': of}})

    def update_total(self, of, value, addition):
        addition = True if str(addition).upper() == "TRUE" else addition
        addition = False if str(addition).upper() == "FALSE" else addition
        self.set_base_router('/api')
        return self.request('post', '/totals', data={'total': {'of': of, 'value': value, 'addition': addition}})
