from .client import Client


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
            Command('getusers', 0, lambda: self.client.get_users()),
            Command('getuser', 1, lambda a: self.client.get_user(a)),
            Command('adduser', 3, lambda a, b, c: self.client.add_user(a, b, c)),
            Command('removeuser', 1, lambda a: self.client.remove_user(a)),
            Command('updateusername', 2, lambda a, b: self.client.update_user_name(a, b)),
            Command('updateuserpermission', 2, lambda a, b: self.client.update_user_permission(a, b)),
            Command('updateuserpassword', 2, lambda a, b: self.client.update_user_password(a, b)),
            # Squeezes
            Command('getsqueezes', 0, lambda: self.client.get_squeezes()),
            Command('getsqueeze', 1, lambda a: self.client.get_squeeze(a)),
            Command('addsqueeze', 2, lambda a, b: self.client.add_squeeze(a, b)),
            Command('removesqueeze', 1, lambda a: self.client.remove_squeeze(a)),
            Command('updatesqueezejuice', 2, lambda a, b: self.client.update_squeeze_juice(a, b)),
            Command('updatesqueezeusedapples', 2, lambda a, b: self.client.update_squeeze_used_apples(a, b)),
            # Investments
            Command('getinvestments', 0, lambda: self.client.get_investments()),
            Command('getinvestment', 1, lambda a: self.client.get_investment(a)),
            Command('updateinvestment', 2, lambda a, b: self.client.update_investment(a, b)),
            # Tokens
            Command('gettokens', 0, lambda: self.client.get_tokens()),
            Command('gettoken', 1, lambda a: self.client.get_token(a)),
            Command('generatetoken', 2, lambda a, b: self.client.generate_token(a, b)),
            # Totals
            Command('gettotal', 1, lambda a: self.client.get_total(a)),
            Command('updatetotal', 3, lambda a, b, c: self.client.update_total(a, b, c))
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
                if registered_command.name == command[0]:
                    print(registered_command.execute(command))
                    valid_command = True
                    break
            if not valid_command:
                print("Unregistered command. Are you sure you typed it correctly ?")

    def stop(self):
        self.running = False
        print("Thank you and goodbye !")


class Command:

    def __init__(self, name, args_number, execution):
        self.name = name
        self.args_number = args_number
        self.execution = execution

    def execute(self, command):
        args_number = len(command) - 1
        if args_number != self.args_number:
            return f"This command needs {self.args_number} arguments, {args_number} given..."
        command.pop(0)
        return self.execution(*command).json()
