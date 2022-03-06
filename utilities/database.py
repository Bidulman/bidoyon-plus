from sqlite3 import connect
from os import listdir, path

from secrets import token_hex

import logging


class Database:

    # Useful methods for Database

    def __init__(self, utils, load=True):
        self.utils = utils
        self.path = utils.config.get('database.file_path')
        self.scripts_path = utils.config.get('database.scripts_folder')
        self.connexion = None

        self.scripts = {}
        self.load_scripts()

        logging.info(f"Initialized database with path '{self.path}'.")

        if load:
            self.load()

    def load(self):
        if path.exists(self.path):
            logging.info(f"Database '{self.path}' already exists. Using it !")
            self.connect()
            self.build()
            token = self.get_token_by_user(0)
            self.utils.token.set(token['token'])
        else:
            logging.info(f"Database '{self.path}' does not exist. Creating it...")
            self.connect()
            self.build()
            token = self.create_root()
            self.utils.token.set(token)
            logging.info(f"Superuser token is '{token}'. Please save it !")

    def connect(self):
        self.connexion = connect(self.path)

    def create_root(self):
        return self.generate_token(0, 'SUPER')

    def close(self):
        self.connexion.close()
        logging.info(f"Closed database '{self.path}'.")

    def build(self):
        cursor = self.connexion.cursor()
        cursor.executescript(self.scripts['BUILD'])
        logging.info(f"Built database '{self.path}'.")

    def load_scripts(self):
        self.scripts = {}
        scripts_number = 0
        for file in listdir(self.scripts_path):
            file_name = file.replace('.sql', '')
            file_path = self.scripts_path + file
            with open(file_path, 'r', encoding='utf-8') as red_file:
                self.scripts[file_name] = red_file.read()
            scripts_number += 1
        logging.info(f"Loaded {scripts_number} scripts from '{self.scripts_path}'.")

    def __enter__(self):
        return self.connexion.cursor()

    def __exit__(self, _1, _2, _3):
        self.connexion.commit()

    # Useful methods for Tokens

    def get_tokens(self):
        tokens = []
        with self as cursor:
            cursor.execute(self.scripts['GET_TOKENS'])
        for token in cursor.fetchall():
            tokens.append(dict(zip(['user', 'permission', 'token'], token)))
        return tokens

    def get_token_by_token(self, token):
        with self as cursor:
            cursor.execute(self.scripts['GET_TOKEN_BY_TOKEN'], (token,))
            token = cursor.fetchone()
            if token:
                return dict(zip(['user', 'permission', 'token'], token))
        return None

    def get_token_by_user(self, user):
        with self as cursor:
            cursor.execute(self.scripts['GET_TOKEN_BY_USER'], (user,))
            token = cursor.fetchone()
            if token:
                return self.get_token_by_token(token[0])
        return None

    def generate_token(self, user, permission):
        if user == 0: token = token_hex(64)
        else: token = token_hex(32)
        with self as cursor:
            if not self.get_token_by_user(user):
                cursor.execute(self.scripts['ADD_TOKEN'], (user, permission, token))
            else:
                cursor.execute(self.scripts['UPDATE_TOKEN'], (permission, token, user))
        return token

    # Useful methods for Totals

    def get_total(self, of):
        with self as cursor:
            cursor.execute(self.scripts['GET_TOTAL'], (of,))
            total = cursor.fetchone()
            if total:
                return dict(zip(['of', 'value'], total))
        return None

    def update_total(self, of, value, addition=False):
        with self as cursor:
            total = self.get_total(of)
            if total:
                if addition:
                    value = total['value']+value
                cursor.execute(self.scripts['UPDATE_TOTAL'], (value, of))
            else:
                cursor.execute(self.scripts['ADD_TOTAL'], (of, value))
        return self.get_total(of)

    # Useful methods for Users

    def get_users(self):
        users = []
        with self as cursor:
            cursor.execute(self.scripts['GET_USERS'])
        for user in cursor.fetchall():
            users.append(dict(zip(['id', 'name', 'permission'], user)))
        return users

    def get_user_by_id(self, id):
        with self as cursor:
            cursor.execute(self.scripts['GET_USER_BY_ID'], (id,))
            user = cursor.fetchone()
            if user:
                return dict(zip(['id', 'name', 'permission', 'password'], user))
        return None

    def get_user_by_name(self, name):
        with self as cursor:
            cursor.execute(self.scripts['GET_USER_BY_NAME'], (name,))
            user = cursor.fetchone()
            if user:
                return self.get_user_by_id(user[0])
        return None

    def add_user(self, name, permission, password):
        if not self.get_user_by_name(name):
            with self as cursor:
                cursor.execute(self.scripts['ADD_USER'], (name, permission, password))
                self.update_total('users', 1, True)
            return True
        return False

    def remove_user(self, id):
        if self.get_user_by_id(id):
            with self as cursor:
                cursor.execute(self.scripts['DELETE_USER'], (id,))
                self.update_total('users', -1, True)
            return True
        return False

    def update_user_name(self, id, new_name):
        if self.get_user_by_id(id) and not self.get_user_by_name(new_name):
            with self as cursor:
                cursor.execute(self.scripts['UPDATE_USER_NAME'], (new_name, id))
            return True
        return False

    def update_user_permission(self, id, new_permission):
        if self.get_user_by_id(id):
            with self as cursor:
                cursor.execute(self.scripts['UPDATE_USER_PERMISSION'], (new_permission, id))
            return True
        return False

    def update_user_password(self, id, new_password):
        if self.get_user_by_id(id):
            with self as cursor:
                cursor.execute(self.scripts['UPDATE_USER_PASSWORD'], (new_password, id))
            return True
        return False

    # Useful methods for Squeezes

    def get_squeezes(self):
        squeezes = []
        with self as cursor:
            cursor.execute(self.scripts['GET_SQUEEZES'])
        for squeeze in cursor.fetchall():
            squeezes.append(dict(zip(['id', 'juice', 'used_apples'], squeeze)))
        return squeezes

    def get_squeeze(self, id):
        with self as cursor:
            cursor.execute(self.scripts['GET_SQUEEZE'], (id,))
            squeeze = cursor.fetchone()
            if squeeze:
                return dict(zip(['id', 'juice', 'used_apples'], squeeze))
        return None

    def add_squeeze(self, juice, used_apples):
        with self as cursor:
            cursor.execute(self.scripts['ADD_SQUEEZE'], (juice, used_apples))
            self.update_total('produced_juice', juice, True)
            self.update_total('used_apples', used_apples, True)
        return True

    def remove_squeeze(self, id):
        squeeze = self.get_squeeze(id)
        if squeeze:
            with self as cursor:
                cursor.execute(self.scripts['DELETE_SQUEEZE'], (id,))
                self.update_total('produced_juice', -squeeze['juice'], True)
                self.update_total('used_apples', -squeeze['used_apples'], True)
            return True
        return False

    def update_squeeze_juice(self, id, new_juice):
        squeeze = self.get_squeeze(id)
        if squeeze:
            with self as cursor:
                cursor.execute(self.scripts['UPDATE_SQUEEZE_JUICE'], (new_juice, id))
                self.update_total('produced_juice', new_juice-squeeze['juice'], True)
            return True
        return False

    def update_squeeze_used_apples(self, id, new_used_apples):
        squeeze = self.get_squeeze(id)
        if squeeze:
            with self as cursor:
                cursor.execute(self.scripts['UPDATE_SQUEEZE_USED_APPLES'], (new_used_apples, id))
                self.update_total('used_apples', new_used_apples-squeeze['used_apples'], True)
            return True
        return False

    # Useful methods for Investments

    def get_investments(self):
        investments = []
        with self as cursor:
            cursor.execute(self.scripts['GET_INVESTMENTS'])
        for investment in cursor.fetchall():
            investments.append(dict(zip(['user', 'given_apples'], investment)))
        return investments

    def get_investment(self, user):
        with self as cursor:
            cursor.execute(self.scripts['GET_INVESTMENT'], (user,))
            investment = cursor.fetchone()
            if investment:
                return dict(zip(['user', 'given_apples'], investment))
        return None

    def update_investment(self, user, new_given_apples):
        with self as cursor:
            investment = self.get_investment(user)
            if investment:
                cursor.execute(self.scripts['UPDATE_INVESTMENT'], (new_given_apples, user))
                self.update_total('given_apples', new_given_apples-investment['given_apples'], True)
            else:
                cursor.execute(self.scripts['ADD_INVESTMENT'], (user, new_given_apples))
                self.update_total('given_apples', new_given_apples, True)
        return self.get_investment(user)
