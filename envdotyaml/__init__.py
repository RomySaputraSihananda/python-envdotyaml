import os
import sys

from yaml import safe_load

from envdotyaml.__version__ import __title__, __author_email__, __autor__, __description__, __license__, __url__, __version__

def find_envdotyaml(filename: str = 'env.yaml', usecwd: bool = False) -> str:
    """
    Search in increasingly higher folders for the given file

    Returns path to the file if found, or an empty string otherwise
    """

    def _is_interactive():
        """ Decide whether this is running in a REPL or IPython notebook """
        try:
            main: object = __import__('__main__', None, None, fromlist=['__file__'])
        except ModuleNotFoundError:
            return False
        return not hasattr(main, '__file__')
    
    def _walk_to_root(path: str):
        """
        Yield directories starting from the given directory up to the root
        """
        if not os.path.exists(path):
            raise IOError('Starting path not found')

        if os.path.isfile(path):
            path: str = os.path.dirname(path)

        last_dir = None
        current_dir = os.path.abspath(path)
        while last_dir != current_dir:
            yield current_dir
            parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
            last_dir, current_dir = current_dir, parent_dir

    if usecwd or _is_interactive() or getattr(sys, 'frozen', False):
        # Should work without __file__, e.g. in REPL or IPython notebook.
        path: str = os.getcwd()
    else:
        # will work for .py files
        frame = sys._getframe()
        current_file = __file__

        while frame.f_code.co_filename == current_file or not os.path.exists(
            frame.f_code.co_filename
        ):
            assert frame.f_back is not None
            frame = frame.f_back
        frame_filename = frame.f_code.co_filename
        path = os.path.dirname(os.path.abspath(frame_filename))

    for dirname in _walk_to_root(path):
        check_path = os.path.join(dirname, filename)
        if os.path.isfile(check_path):
            return check_path

    return ''

def load_envdotyaml(envdotyaml_path: str = 'env.yaml') -> bool:
    """
    Parse a env.yaml file and then load all the variables found as environment variables.

    Parameters:
        envdotyaml_path: Absolute or relative path to env.yam; file.
    Returns:
        Bool: True if at least one environment variable is set else False

    If both `envdotyaml_path` are `None`, `find_envdotyaml()` is used to find the env.yaml file.
    """
    # envdotyaml_path: str = 
    if not (envdotyaml_path := find_envdotyaml()): 
        raise FileNotFoundError(f'File {envdotyaml_path} not found')
    
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
