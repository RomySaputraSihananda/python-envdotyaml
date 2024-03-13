import os

from yaml import safe_load
from dotenv import find_dotenv

from envdotyaml.__version__ import __title__, __author_email__, __autor__, __description__, __license__, __url__, __version__

def load_envdotyaml(envdotyaml_path: str = 'env.yaml') -> bool:
    """
    Parse a env.yaml file and then load all the variables found as environment variables.

    Parameters:
        envdotyaml_path: Absolute or relative path to env.yam; file.
    Returns:
        Bool: True if at least one environment variable is set else False

    If both `envdotyaml_path` are `None`, `find_dotenv()` is used to find the env.yaml file.
    """
    if not find_dotenv(envdotyaml_path): raise FileNotFoundError(f'File {envdotyaml_path} not found')
    
    with open(envdotyaml_path, 'r') as file:
        env_data: dict = safe_load(file.read())
        for key, value in flatten_dict(env_data).items():
            os.environ[key] = value
    
    return True

def flatten_dict(env_data: dict, parent_key: str = '', sep: str = '_') -> dict:
    items: list = []
    for key, value in env_data.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_dict(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))

    return dict(items)


if(__name__ == '__main__'):
    load_envdotyaml()

    print(os.getenv('AUTH_USERNAME'))
    print(__author_email__)
