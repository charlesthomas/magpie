from os import path

class ConfigPath(object):
    def __getattr__(self, key):
        return_path = path.join(path.dirname(__file__), key + '.cfg')
        if not path.exists(return_path): return None
        return return_path

config_path = ConfigPath()
