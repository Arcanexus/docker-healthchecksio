import requests
import socket
import re
from modules.common import bcolors, get_formatted_datetime, printdebug

# Function to check if a service URL returns a 200 HTTP status code
def check_serviceHTTP(service_endpoint, check_ssl=True, debug=False):
    current_datetime = get_formatted_datetime()
    try:
        response = requests.get(service_endpoint, allow_redirects=True, verify=check_ssl)
        printdebug(f"HTTP Code {response.status_code} - {response.reason}", debug)
        rc_pattern = re.compile(r'^(2\d{2}|401|403)$')
        if rc_pattern.match(str(response.status_code)):
            return True
        else:
            return False
        
    except requests.exceptions.SSLError as e:
        print(f"{current_datetime} - [{bcolors.FAIL}ERROR{bcolors.ENDC}] - SSL Error checking service {service_endpoint}: {e}")
        return False

    except requests.exceptions.RequestException as e:
        if "[Errno 8]" in str(e) or "[Errno 11001]" in str(e) or "[Errno -2]" in str(e):
            printdebug(f"Fail to resolve {service_endpoint}: {e}", debug)
        else:
            printdebug(f"Error checking service {service_endpoint}: {e}", debug)
        return False

def check_serviceTCP(service_endpoint, port, timeout=5, debug=False):
    current_datetime = get_formatted_datetime()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((service_endpoint, port))
        sock.close()
        return True
    except socket.timeout:
        print(f"{current_datetime} - [{bcolors.FAIL}ERROR{bcolors.ENDC}] - Connection timeout to {service_endpoint}:{port} after {timeout} seconds.")
        return False
    except socket.error as e:
        print(f"{current_datetime} - [{bcolors.FAIL}ERROR{bcolors.ENDC}] - Connection failed to {service_endpoint}:{port} after {timeout} seconds.")
        return False
