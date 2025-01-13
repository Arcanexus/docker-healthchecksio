import requests
from .logger import logging


# Function to send an HTTP POST request to the monitoring URL
def post_healthchecksio_status(monitoring_url):
    try:
        response = requests.post(monitoring_url)
    except requests.RequestException as e:
        logging.error(f"Error sending POST request to {monitoring_url}: {e}")
