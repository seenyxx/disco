from yaml import load as load_yaml, Loader
from .logs import *
from .messages import *
from .db import *

def load_config():
    with open('config.yml') as file:
        data = file.read()
        parsed_data = load_yaml(data, Loader=Loader)
    return parsed_data