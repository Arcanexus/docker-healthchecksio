import os
import yaml

# Function to read a single YAML file
def read_yaml_file(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to read all YAML files from a directory
def read_yaml_directory(dir_path):
    config = {'services': []}
    for file_name in os.listdir(dir_path):
        if file_name.endswith('.yml') or file_name.endswith('.yaml'):
            file_path = os.path.join(dir_path, file_name)
            file_config = read_yaml_file(file_path)
            config['services'].extend(file_config.get('services', []))
    return config

# Function to determine if a path is a file or directory and read config
def read_config(path):
    if os.path.isfile(path):
        return read_yaml_file(path)
    elif os.path.isdir(path):
        return read_yaml_directory(path)
    else:
        raise ValueError(f"Invalid path: {path}")