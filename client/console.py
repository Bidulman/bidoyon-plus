from .client import Client
from requests import Response


class Console:

    def __init__(self):
        self.load()
        self.start()

    def load(self):
        address = input("Address : ")
        token = input("Token : ")
        self.client = Client(address, token)
        self.commands = [
            # Users
            Command('getusers', ['gus'], 0, lambda: self.client.get_users()),
            Command('getuser', ['gu'], 1, lambda a: self.client.get_user(a)),
            Command('adduser', ['au'], 3, lambda a, b, c: self.client.add_user(a, b, c)),
            Command('removeuser', ['ru'], 1, lambda a: self.client.remove_user(a)),
            Command('updateusername', ['uun'], 2, lambda a, b: self.client.update_user_name(a, b)),
            Command('updateuserpermission', ['uupe'], 2, lambda a, b: self.client.update_user_permission(a, b)),
            Command('updateuserpassword', ['uupa'], 2, lambda a, b: self.client.update_user_password(a, b)),
            # Squeezes
            Command('getsqueezes', ['gss'], 0, lambda: self.client.get_squeezes()),
            Command('getsqueeze', ['gs'], 1, lambda a: self.client.get_squeeze(a)),
            Command('addsqueeze', ['as'], 2, lambda a, b: self.client.add_squeeze(a, b)),
            Command('removesqueeze', ['rs'], 1, lambda a: self.client.remove_squeeze(a)),
            Command('updatesqueezejuice', ['usj'], 2, lambda a, b: self.client.update_squeeze_juice(a, b)),
            Command('updatesqueezeusedapples', ['usua'], 2, lambda a, b: self.client.update_squeeze_used_apples(a, b)),
            # Investments
            Command('getinvestments', ['gis'], 0, lambda: self.client.get_investments()),
            Command('getinvestment', ['gi'], 1, lambda a: self.client.get_investment(a)),
            Command('updateinvestment', ['ui'], 2, lambda a, b: self.client.update_investment(a, b)),
            # Tokens
            Command('gettokens', ['gtoks'], 0, lambda: self.client.get_tokens()),
            Command('gettoken', ['gtok'], 1, lambda a: self.client.get_token(a)),
            Command('generatetoken', ['gentok'], 2, lambda a, b: self.client.generate_token(a, b)),
            # Totals
            Command('gettotal', ['gtot'], 1, lambda a: self.client.get_total(a)),
            Command('updatetotal', ['utot'], 3, lambda a, b, c: self.client.update_total(a, b, c)),
            # Configs
            Command('reloadconfig', ['rlcfg'], 1, lambda a: self.client.reload_config(a)),
            # Console
            Command('!changeaddress', ['!cha'], 1, lambda a: self.client.set_address(a)),
            Command('!changetoken', ['!cht'], 1, lambda a: self.client.set_token(a))
        ]

    def start(self):
        self.running = True
        while self.running is True:
            command = input("> ").split(' ')
            if len(command) == 0:
                continue
            if command[0] == 'exit':
                self.stop()
                return
            valid_command = False
            for registered_command in self.commands:
                if registered_command.name == command[0] or command[0] in registered_command.aliases:
                    print(registered_command.execute(command))
                    valid_command = True
                    break
            if not valid_command:
                print("Unregistered command. Are you sure you typed it correctly ?")

    def stop(self):
        self.running = False
        print("Thank you and goodbye !")


class Command:

    def __init__(self, name: str, aliases: list, args_number: int, execution):
        self.name = name
        self.aliases = aliases
        self.args_number = args_number
        self.execution = execution

    def execute(self, command: list):
        args_number = len(command) - 1
        if args_number != self.args_number:
            return f"This command needs {self.args_number} arguments, {args_number} given..."
        command.pop(0)
        result = self.execution(*command)
        if isinstance(result, Response):
            return result.json()
        else:
            return result
