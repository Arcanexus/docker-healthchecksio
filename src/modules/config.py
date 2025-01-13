"""Config management"""

import os
import yaml
import argparse


# Function to read a single YAML file
def read_yaml_file(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


# Function to read all YAML files from a directory
def read_yaml_directory(dir_path):
    merged_data = {}

    # Loop through all files in the directory
    for file_name in os.listdir(dir_path):
        # Check if the file is a YAML file
        if file_name.endswith(('.yml', '.yaml')):
            file_path = os.path.join(dir_path, file_name)
            with open(file_path, 'r') as file:
                try:
                    yaml_data = yaml.safe_load(file)  # Load the YAML file
                    if isinstance(yaml_data, dict):
                        merged_data.update(yaml_data)  # Merge dictionaries
                    else:
                        print(f"Skipping {file_name}: not a dictionary")
                except yaml.YAMLError as e:
                    print(f"Error parsing {file_name}: {e}")

    return merged_data


# Function to determine if a path is a file or directory and read config
def read_config(path):
    if os.path.isfile(path):
        return read_yaml_file(path)
    elif os.path.isdir(path):
        return read_yaml_directory(path)
    else:
        raise ValueError(f"Invalid path: {path}")


class Config:
    def __init__(self, path):
        self.config_path = path
        self.config_override = {}
        self.reload()

    def reload(self):
        self.config = read_config(self.config_path)
        self.current_config = self._merge_dicts(self.config, self.config_override)

    def _merge_dicts(self, base, override):
        for key, value in override.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._merge_dicts(base[key], value)
            else:
                base[key] = value

    def get(self, yaml_path):
        keys = yaml_path.split('.')
        value = self.config
        for key in keys:
            value = value.get(key)
            if value is None:
                return None
        return value

    def set(self, yaml_path, value):
        keys = yaml_path.split('.')
        d = self.config_override
        for key in keys[:-1]:
            if key not in d:
                d[key] = {}
                d = d[key]
        d[keys[-1]] = value
        self.reload()

    def delete(self, yaml_path):
        keys = yaml_path.split('.')
        d = self.config_override
        for key in keys[:-1]:
            if key in d:
                d = d[key]
            else:
                return  # Key path does not exist
        if keys[-1] in d:
            del d[keys[-1]]

        # Function to recursively delete empty keys
        def delete_empty_keys(d):
            keys_to_delete = [key for key, value in d.items() if isinstance(value, dict)]
            for key in keys_to_delete:
                delete_empty_keys(d[key])
                if not d[key]:
                    del d[key]

        delete_empty_keys(self.config_override)
        self.reload()


current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(os.path.dirname(current_file_path))

parser = argparse.ArgumentParser(description="Service health checker for healthchecks.io.", epilog="Arcanexus - Under Licence GPLv3")
parser.add_argument('-c', '--config', type=str, default=current_dir + '/config', help='Path to the config file or directory')
parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
args = parser.parse_args()

config_path = args.config
current_config = Config(config_path)

# current_config.set('config.logs.log_level', "DEBUG")

if args.debug or os.getenv('DEBUG', 'false').lower() == 'true':
    current_config.set('config.logs.log_level', 'DEBUG')
