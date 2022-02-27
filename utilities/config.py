import yaml


class Config:

    def __init__(self, path, load=True):
        self.path = path
        self.file = None
        self.loader = yaml.Loader
        self.dumper = yaml.Dumper
        self.loaded = {}
        if load:
            self.load()

    def get(self, path):
        path = path.split('.')
        value = self.loaded
        for key in path:
            try: key = int(key)
            except ValueError: pass
            value = value[key]
        return value

    def load(self):
        self.open_file('r')
        self.loaded = yaml.load(self.file, self.loader)

    def save(self):
        self.open_file('w')
        yaml.dump(self.loaded, self.file, self.dumper)
        self.load()

    def close(self):
        self.loaded = {}
        self.close_file()

    def save_and_close(self):
        self.save()
        self.close()

    def open_file(self, mode):
        self.close_file()
        self.file = open(self.path, mode, encoding='utf-8')

    def close_file(self):
        if self.file and not self.file.closed:
            self.file.close()
