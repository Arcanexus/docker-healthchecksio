import requests
from .common import bcolors
from .common import get_formatted_datetime

# Function to send an HTTP POST request to the monitoring URL
def post_healthchecksio_status(monitoring_url):
    try:
        response = requests.post(monitoring_url)
    except requests.RequestException as e:
        current_datetime = get_formatted_datetime()
        print(f"{current_datetime} - [{bcolors.FAIL}ERROR{bcolors.ENDC}] - Error sending POST request to {monitoring_url}: {e}")
