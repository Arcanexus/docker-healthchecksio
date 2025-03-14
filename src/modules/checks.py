import requests
import socket
import re
from .logger import logger


# Function to check if a service URL returns a 200 HTTP status code
def check_serviceHTTP(service_endpoint, check_ssl=True):
    try:
        response = requests.get(service_endpoint, allow_redirects=True, verify=check_ssl)
        logger.debug(f"HTTP Code {response.status_code} - {response.reason}")
        rc_pattern = re.compile(r'^(2\d{2}|401|403)$')
        if rc_pattern.match(str(response.status_code)):
            return True
        else:
            return False

    except requests.exceptions.SSLError as e:
        logger.error(f"SSL Error checking service {service_endpoint}: {e}")
        return False

    except requests.exceptions.RequestException as e:
        if "[Errno 8]" in str(e) or "[Errno 11001]" in str(e) or "[Errno -2]" in str(e):
            logger.debug(f"Fail to resolve {service_endpoint}: {e}")
        else:
            logger.debug(f"Error checking service {service_endpoint}: {e}")
        return False


def check_serviceTCP(service_endpoint, port, timeout=5):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((service_endpoint, port))
        sock.close()
        return True
    except socket.timeout:
        logger.error(f"Connection timeout to {service_endpoint}:{port} after {timeout} seconds.")
        return False
    except socket.error as e:
        logger.error(f"Connection failed to {service_endpoint}:{port} after {timeout} seconds.")
        return False
