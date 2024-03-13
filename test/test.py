import os

from envdotyaml import load_envdotyaml

if(__name__ == '__main__'):
    load_envdotyaml('/home/romy/Destop/miniPjoject/yamlenv/env.yaml')

    print(os.environ.keys())