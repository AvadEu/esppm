from os import path
import tomllib

def read_conf(conf_title: str, filename: str = 'conf.toml') -> dict:
    """
    Function takes filename to config toml file in project's root directory as a first argument,
    name of the settings heading from toml file, 
    returns config data as a dictionary.
    """
    conf_path = path.join(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))), filename)
    with open(conf_path, 'rb') as f:
        data = tomllib.load(f)
        conf = data.get(conf_title)
        return conf