from os import path

class ConfigPath(object):
    def __init__(self):
        self.config_paths = [path.join(path.expanduser('~'), '.magpie'), path.dirname(__file__)]
    def __getattr__(self, key):
        for pathc in self.config_paths:
            return_path = path.join(pathc, key + '.cfg')
            if path.exists(return_path): return return_path
        return None

config_path = ConfigPath()
