class TokenManager:

    def __init__(self, path):
        self.path = path
        self.file = None

    def get(self):
        self.open('r')
        return self.file.read()

    def set(self, token):
        self.open('w')
        self.file.write(token)

    def open(self, mode):
        self.close()
        try:
            self.file = open(self.path, mode, encoding='utf-8')
        except IOError:
            self.open('w')
            self.open(mode)

    def close(self):
        if self.file and not self.file.close():
            self.file.close()
