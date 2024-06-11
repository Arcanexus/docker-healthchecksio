import os
import time
import yaml
import requests
import argparse
from datetime import datetime

# Function to get the current date and time formatted as "31-Dec-2023 19:34"
def get_formatted_datetime():
    now = datetime.now()
    return now.strftime("%d-%b-%Y %H:%M")

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

# Function to check if a service URL returns a 200 HTTP status code
def check_service(service_url):
    try:
        response = requests.get(service_url, allow_redirects=True)
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Error checking service {service_url}: {e}")
        return False

# Function to send an HTTP POST request to the monitoring URL
def send_monitoring_request(monitoring_url):
    try:
        response = requests.post(monitoring_url)
        # print(f"Sent POST request to {monitoring_url}, response status: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error sending POST request to {monitoring_url}: {e}")

# Main function to perform the checks every minute
def main(config_path):
    while True:
        try:
          config = read_config(config_path)
        except:
          print("Invalid config file or directory : " + config_path)
          parser.print_help()
          exit(1)
        current_datetime = get_formatted_datetime()
        for item in config['services']:
            name = item['name']
            service_url = item['service_url']
            monitoring_url = item['healthchecks_io_monitoring_url']
            
            # print(f"Checking service: {name}")
            if check_service(service_url):
                print(f"{current_datetime} - Service {name:<10} UP   at {service_url}")
                send_monitoring_request(monitoring_url)
            else:
                print(f"{current_datetime} - Service {name:<10} DOWN at {service_url}")
                send_monitoring_request(monitoring_url + "/fail")
        
        time.sleep(60)  # Wait for 1 minute before the next check

# Entry point
if __name__ == "__main__":
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)

    parser = argparse.ArgumentParser(description="Service health checker for healthchecks.io.",epilog="Arcanexus - Under Licence GPLv3")
    parser.add_argument('-c', '--config', type=str, default=current_dir + '/config', help='Path to the config file or directory')
    args = parser.parse_args()
    
    config_path = args.config
    main(config_path)
