from os import path
import tomllib

def read_conf(filename: str = 'conf.toml') -> dict:
    """
    Function take filename to config toml file in project's root directory as a single argument,
    returns config data as a dictionary.
    """
    conf_path = path.join(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))), filename)
    with open(conf_path, 'rb') as f:
        conf = tomllib.load(f)
        return conf