import os
import yaml

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