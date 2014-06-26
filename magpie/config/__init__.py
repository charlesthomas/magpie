from os import path

class ConfigPath(object):
    def __init__(self):
        self.config_paths = [path.join(path.expanduser('~'), '.magpie'),
                             path.dirname(__file__)]

    def __getattr__(self, key):
        for p in self.config_paths:
            fname = key + '.cfg'
            return_path = path.join(p, fname)
            if path.exists(return_path): return return_path
        return None

config_path = ConfigPath()
