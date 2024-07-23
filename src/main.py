import os
import time
import argparse
import threading
import urllib3
from concurrent.futures import ThreadPoolExecutor

from modules.common import bcolors, get_formatted_datetime, printdebug, to_camel_case
from modules.config import read_config
from modules.checks import check_serviceHTTP, check_serviceTCP
from modules.healthchecksio import post_healthchecksio_status

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

debug = False

# Function to monitor a service
def monitor_service(item):
    name = item['name']
    service_endpoint = item['service_endpoint']
    monitoring_url = item['healthchecks_io_monitoring_url']
    check_type = item.get('check', {}).get('type', 'http')
    polling_timer = item.get('check', {}).get('polling_timer', 60)
    thread_name = f"c_{to_camel_case(name)}"
    threading.current_thread().name = thread_name

    while True:
        current_datetime = get_formatted_datetime()
        if check_type == 'http':
            check_ssl = item.get('check', {}).get('ssl_check', True)
            printdebug(f"Checking {name} ({check_type.upper()}/SSL Check={str(check_ssl)}) at {service_endpoint} for {monitoring_url}", debug)
            res = check_serviceHTTP(service_endpoint, check_ssl, debug)
            tested_endpoint = service_endpoint

        elif check_type == 'tcp':
            tcp_port = int(item.get('check', {}).get('tcp_port', 80))
            tcp_timeout = int(item.get('check', {}).get('tcp_timeout', 5))
            printdebug(f"Checking {name} ({check_type.upper()}) at {service_endpoint}:{str(tcp_port)} for {monitoring_url}", debug)
            res = check_serviceTCP(service_endpoint, tcp_port, tcp_timeout, debug)
            tested_endpoint = 'tcp://' + service_endpoint + ':' + str(tcp_port)

        if res:
            print(f"{current_datetime} - [{bcolors.OKGREEN}INFO {bcolors.ENDC}] - Service {name:<20} {bcolors.OKGREEN}UP{bcolors.ENDC}   at {tested_endpoint}")
            post_healthchecksio_status(monitoring_url)
        else:
            print(f"{current_datetime} - [{bcolors.FAIL}ERROR{bcolors.ENDC}] - Service {name:<20} {bcolors.FAIL}DOWN{bcolors.ENDC} at {tested_endpoint}")
            post_healthchecksio_status(monitoring_url + "/fail")

        printdebug(f"Sleeping {polling_timer} seconds before next check for {name}...", debug)
        time.sleep(polling_timer)

# Main function to read the config and start monitoring services in parallel
def main(config_path):
    try:
        config = read_config(config_path)
    except ValueError as e:
        current_datetime = get_formatted_datetime()
        print(f"{current_datetime} - [{bcolors.FAIL}ERROR{bcolors.ENDC}] - {e}")
        parser.print_help()
        exit(1)
    
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(monitor_service, item) for item in config['services']]
        for future in futures:
            future.result()

# Entry point
if __name__ == "__main__":
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    current_datetime = get_formatted_datetime()
    
    parser = argparse.ArgumentParser(description="Service health checker for healthchecks.io.", epilog="Arcanexus - Under Licence GPLv3")
    parser.add_argument('-c', '--config', type=str, default=current_dir + '/config', help='Path to the config file or directory')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()
    
    config_path = args.config
    if args.debug or os.getenv('DEBUG', 'false').lower() == 'true':
        debug = True
        printdebug(f"Debug Mode ON", debug)
    else:
        debug = False
    
    main(config_path)
