import os
import yaml

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'system_rules.yaml')


def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)
