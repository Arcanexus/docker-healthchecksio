import os, sys
import re
import time
import yaml
import requests
import argparse
from datetime import datetime
import socket
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

debug = False
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Function to get the current date and time formatted as "31-Dec-2023 19:34"
def get_formatted_datetime():
    now = datetime.now()
    return now.strftime("%d-%b-%Y %H:%M")

def printdebug(msg):
    if debug:
        current_datetime = get_formatted_datetime()
        print(f"{bcolors.OKBLUE}{current_datetime} - [DEBUG] - {msg}{bcolors.ENDC}")

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
def check_serviceHTTP(service_endpoint, check_ssl=True):
    current_datetime = get_formatted_datetime()
    try:
        response = requests.get(service_endpoint, allow_redirects=True, verify=check_ssl)
        printdebug(f"HTTP Code {response.status_code} - {response.reason}")
        rc_pattern = re.compile(r'^(2\d{2}|401|403)$')
        if rc_pattern.match(str(response.status_code)):
            return True
        else:
            return False
        
    except requests.exceptions.SSLError as e:
        print(f"{current_datetime} - [{bcolors.FAIL}ERROR{bcolors.ENDC}] - SSL Error checking service {service_endpoint}: {e}")
        return False

    except requests.exceptions.RequestException as e:
        # if 'MaxRetryError' not in str(e.args) or 'NewConnectionError' not in str(e.args):
        #     print(f"{current_datetime} - [ERROR] - What {service_endpoint}: {e}")
        if "[Errno 8]" in str(e) or "[Errno 11001]" in str(e) or "[Errno -2]" in str(e):
            printdebug(f"Fail to resolve {service_endpoint}: {e}")
        else:
            printdebug(f"Error checking service {service_endpoint}: {e}")
        return False

def check_serviceTCP(service_endpoint, port, timeout=5):
    current_datetime = get_formatted_datetime()
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)  # Set a timeout for the connection attempt
        
        # Connect to the service endpoint
        sock.connect((service_endpoint, port))
        
        # If the connection is successful, close the socket and return True
        sock.close()
        return True
    except socket.timeout:
        print(f"{current_datetime} - [{bcolors.FAIL}ERROR{bcolors.ENDC}] - Connection timeout to {service_endpoint}:{port} after {timeout} seconds.")
        return False
    except socket.error as e:
        print(f"{current_datetime} - [{bcolors.FAIL}ERROR{bcolors.ENDC}] - Connection failed to {service_endpoint}:{port} after {timeout} seconds.")
        return False
    
# Function to send an HTTP POST request to the monitoring URL
def send_monitoring_request(monitoring_url):
    try:
        response = requests.post(monitoring_url)
        # print(f"Sent POST request to {monitoring_url}, response status: {response.status_code}")
    except requests.RequestException as e:
        current_datetime = get_formatted_datetime()
        print(f"{current_datetime} - [{bcolors.FAIL}ERROR{bcolors.ENDC}] - Error sending POST request to {monitoring_url}: {e}")

# Main function to perform the checks every minute
def main(config_path):
    while True:
        current_datetime = get_formatted_datetime()
        try:
            config = read_config(config_path)
        except:
            print(f"{current_datetime} - [{bcolors.FAIL}ERROR{bcolors.ENDC}] - Invalid config file or directory : " + config_path)
            parser.print_help()
            exit(1)
        if debug:
            print(f"{bcolors.OKBLUE}{current_datetime} - [DEBUG] - Reloading config :")
            print('\n{:#^80s}'.format(" BEGINNING "))
            yaml.dump(config, sys.stdout, default_flow_style=False)
            print('{:#^80s}\n'.format(" END ")+f"{bcolors.ENDC}")
        for item in config['services']:
            name = item['name']
            service_endpoint = item['service_endpoint']
            monitoring_url = item['healthchecks_io_monitoring_url']
            check_type = item.get('check', {}).get('type', 'http')

            if check_type == 'http':
                check_ssl = item.get('check', {}).get('ssl_check', True)
                printdebug(f"Checking {name} ({check_type.upper()}/SSL Check={str(check_ssl)}) at {service_endpoint} for {monitoring_url}")
                res = check_serviceHTTP(service_endpoint, check_ssl)
                tested_endpoint = service_endpoint
            
            if check_type == 'tcp':
                tcp_port = int(item.get('check', {}).get('tcp_port', 80))
                tcp_timeout = int(item.get('check', {}).get('tcp_timeout', 5))
                printdebug(f"Checking {name} ({check_type.upper()}) at {service_endpoint}:{str(tcp_port)} for {monitoring_url}")
                res = check_serviceTCP(service_endpoint, tcp_port, tcp_timeout)
                tested_endpoint = 'tcp://' + service_endpoint + ':' + str(tcp_port)

            if res:
                print(f"{current_datetime} - [{bcolors.OKGREEN}INFO {bcolors.ENDC}] - Service {name:<20} {bcolors.OKGREEN}UP{bcolors.ENDC}   at {tested_endpoint}")
                send_monitoring_request(monitoring_url)
            else:
                print(f"{current_datetime} - [{bcolors.FAIL}ERROR{bcolors.ENDC}] - Service {name:<20} {bcolors.FAIL}DOWN{bcolors.ENDC} at {tested_endpoint}")
                send_monitoring_request(monitoring_url + "/fail")
    
        printdebug(f"Sleeping 60 seconds ...")
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
        printdebug(f"Debug Mode ON")
    else:
        debug = False
    
    main(config_path)
