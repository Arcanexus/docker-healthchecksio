""" Main entry point for the service health checker. """
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import yaml
import urllib3

from modules.common import to_camel_case
from modules.config import current_config, config_path
from modules.checks import check_serviceHTTP, check_serviceTCP
from modules.healthchecksio import post_healthchecksio_status
from modules.logger import logging

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Function to monitor a service
def monitor_service(item, debug):
    name = item['name']
    thread_name = f"{to_camel_case(name)}Thread"
    threading.current_thread().name = thread_name
    service_endpoint = item['service_endpoint']
    monitoring_url = item['healthchecks_io_monitoring_url']
    check_type = item.get('check', {}).get('type', 'http')
    itemdebug = item.get('check', {}).get('debug', debug)
    # logging.critical(f"Debug: {debug}")
    # logging.critical(f"itemdebug: {itemdebug}")
    if debug or itemdebug:
        logging.setLevel('DEBUG')
    polling_timer = item.get('check', {}).get('polling_timer', 60)


    while True:
        if check_type == 'http':
            check_ssl = item.get('check', {}).get('ssl_check', True)
            logging.debug(f"Checking [{name}] ({check_type.upper()}/SSL Check={str(check_ssl)}) at {service_endpoint} for {monitoring_url}")
            res = check_serviceHTTP(service_endpoint, check_ssl)
            tested_endpoint = service_endpoint

        elif check_type == 'tcp':
            tcp_port = int(item.get('check', {}).get('tcp_port', 80))
            tcp_timeout = int(item.get('check', {}).get('tcp_timeout', 5))
            logging.debug(f"Checking [{name}] ({check_type.upper()}) at {service_endpoint}:{str(tcp_port)} for {monitoring_url}")
            res = check_serviceTCP(service_endpoint, tcp_port, tcp_timeout)
            tested_endpoint = 'tcp://' + service_endpoint + ':' + str(tcp_port)

        if res:
            logging.info(f"Service [{name}] UP at {tested_endpoint}")
            post_healthchecksio_status(monitoring_url)
        else:
            logging.error(f"Service [{name}] DOWN at {tested_endpoint}")
            post_healthchecksio_status(monitoring_url + "/fail")

        logging.debug(f"Sleeping {polling_timer} seconds before next check for [{name}]...")
        logging.setLevel(current_config.get('config.logs.log_level').upper())
        time.sleep(polling_timer)


# Main function to read the config and start monitoring services in parallel
def main():
    if current_config.get('config.logs.log_level').upper() == "DEBUG":
        logging.debug(f"Loaded config from {config_path} :")
        logging.debug('{:#^80s}'.format(' BEGINNING '))
        logging.debug('\n\n' + yaml.dump(current_config.config, default_flow_style=False))
        logging.debug('{:#^80s}'.format(' END '))

    logging.info("Initialisation complete.")
    logging.info("Starting service health checker...")
    with ThreadPoolExecutor() as executor:
        services = current_config.config["services"]
        if current_config.get('config.logs.log_level').upper() == "DEBUG":
            debug = True
        else:
            debug = False
        futures = [executor.submit(monitor_service, item, debug=(debug or item.get('check', {}).get('debug', False))) for item in services]
        for future in futures:
            future.result()


# Entry point
if __name__ == "__main__":
    main()
