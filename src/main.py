import os, sys
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
        # return response.status_code == 200
        return response
    except requests.RequestException as e:
        current_datetime = get_formatted_datetime()
        print(f"{current_datetime} - [ERROR] - Error checking service {service_url}: {e}")
        return False

# Function to send an HTTP POST request to the monitoring URL
def send_monitoring_request(monitoring_url):
    try:
        response = requests.post(monitoring_url)
        # print(f"Sent POST request to {monitoring_url}, response status: {response.status_code}")
    except requests.RequestException as e:
        current_datetime = get_formatted_datetime()
        print(f"{current_datetime} - [ERROR] - Error sending POST request to {monitoring_url}: {e}")

# Main function to perform the checks every minute
def main(config_path):
    while True:
        current_datetime = get_formatted_datetime()
        try:
            config = read_config(config_path)
        except:
            print(f"{current_datetime} - [ERROR] - Invalid config file or directory : " + config_path)
            parser.print_help()
            exit(1)
        if debug:
            print(f"{current_datetime} - [DEBUG] - Reloading config :")
            print('\n{:#^80s}'.format(" BEGINNING "))
            yaml.dump(config, sys.stdout, default_flow_style=False)
            print('{:#^80s}\n'.format(" END "))
        for item in config['services']:
            name = item['name']
            service_url = item['service_url']
            monitoring_url = item['healthchecks_io_monitoring_url']
            
            if debug:
                print(f"{current_datetime} - [DEBUG] - Checking {name} at {service_url} for {monitoring_url}")
            res = check_service(service_url)
            if debug:
                    print(f"{current_datetime} - [DEBUG] - HTTP Code {res.status_code} - {res.reason}")
            if res.ok:
                print(f"{current_datetime} - [INFO ] - Service {name:<10} UP   at {service_url}")
                send_monitoring_request(monitoring_url)
            else:
                print(f"{current_datetime} - [ERROR] - Service {name:<10} DOWN at {service_url}")
                send_monitoring_request(monitoring_url + "/fail")
        
        if debug:
            print(f"{current_datetime} - [DEBUG] - Sleeping 60 seconds ...")
        time.sleep(60)  # Wait for 1 minute before the next check

# Entry point
if __name__ == "__main__":
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    
    current_datetime = get_formatted_datetime()
    
    parser = argparse.ArgumentParser(description="Service health checker for healthchecks.io.",epilog="Arcanexus - Under Licence GPLv3")
    parser.add_argument('-c', '--config', type=str, default=current_dir + '/config', help='Path to the config file or directory')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()
    
    config_path = args.config
    if args.debug or os.getenv('DEBUG', 'false').lower() == 'true':
        debug = True
        print(f"{current_datetime} - [DEBUG] - Debug Mode ON")
    else:
        debug = False
    
    main(config_path)
