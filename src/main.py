""" Main entry point for the service health checker. """
import os
import sys
import time
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor
import yaml
import urllib3

from modules.common import bcolors, to_camel_case
from modules.config import Config
from modules.checks import check_serviceHTTP, check_serviceTCP
from modules.healthchecksio import post_healthchecksio_status
from modules.logger import get_logger

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Function to monitor a service
def monitor_service(item, debug=False):
    name = item['name']
    service_endpoint = item['service_endpoint']
    monitoring_url = item['healthchecks_io_monitoring_url']
    check_type = item.get('check', {}).get('type', 'http')
    debug = item.get('check', {}).get('debug', debug)
    polling_timer = item.get('check', {}).get('polling_timer', 60)
    thread_name = f"{to_camel_case(name)}Thread"
    threading.current_thread().name = thread_name

    while True:
        if check_type == 'http':
            check_ssl = item.get('check', {}).get('ssl_check', True)
            logging.debug(f"Checking [{name}] ({check_type.upper()}/SSL Check={str(check_ssl)}) at {service_endpoint} for {monitoring_url}")
            res = check_serviceHTTP(service_endpoint, check_ssl, debug)
            tested_endpoint = service_endpoint

        elif check_type == 'tcp':
            tcp_port = int(item.get('check', {}).get('tcp_port', 80))
            tcp_timeout = int(item.get('check', {}).get('tcp_timeout', 5))
            logging.debug(f"Checking [{name}] ({check_type.upper()}) at {service_endpoint}:{str(tcp_port)} for {monitoring_url}")
            res = check_serviceTCP(service_endpoint, tcp_port, tcp_timeout, debug)
            tested_endpoint = 'tcp://' + service_endpoint + ':' + str(tcp_port)

        if res:
            logging.info(f"Service [{name}] UP at {tested_endpoint}")
            post_healthchecksio_status(monitoring_url)
        else:
            logging.error(f"Service [{name}] DOWN at {tested_endpoint}")
            post_healthchecksio_status(monitoring_url + "/fail")

        logging.debug(f"Sleeping {polling_timer} seconds before next check for [{name}]...")
        time.sleep(polling_timer)


# Main function to read the config and start monitoring services in parallel
def main():
    logging.debug(f"Loaded config from {config_path} :")
    if current_config.get('config.logs.log_level').upper() == "DEBUG":
        print(f"{bcolors.GREEN}" + '{:#^80s}'.format(" BEGINNING "))
        yaml.dump(current_config.config, sys.stdout, default_flow_style=False)
        print('{:#^80s}'.format(" END ") + f"{bcolors.ENDC}")

    with ThreadPoolExecutor() as executor:
        services = current_config.config["services"]
        if current_config.get('config.logs.log_level').upper() == "DEBUG":
            debug = True
        else:
            debug = False
        futures = [executor.submit(monitor_service, item, debug) for item in services]
        for future in futures:
            future.result()


# Entry point
if __name__ == "__main__":
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)

    parser = argparse.ArgumentParser(description="Service health checker for healthchecks.io.", epilog="Arcanexus - Under Licence GPLv3")
    parser.add_argument('-c', '--config', type=str, default=current_dir + '/config', help='Path to the config file or directory')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()

    config_path = args.config
    current_config = Config(config_path)

    # current_config.set('config.logs.log_level', "DEBUG")

    if args.debug or os.getenv('DEBUG', 'false').lower() == 'true':
        current_config.set('config.logs.log_level', 'DEBUG')

    logging = get_logger(logformat=current_config.get('config.logs.format'))
    logging.setLevel(current_config.get('config.logs.log_level').upper())

    main()
