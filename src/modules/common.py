from datetime import datetime
import re


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    GREEN = '\033[32m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DEBUG = OKGREEN
    INFO = OKBLUE
    WARNING = YELLOW
    FAIL = RED
    ERROR = RED
    CRITICAL = RED


# Function to get the current date and time formatted as "31-Dec-2023 19:34"
def get_formatted_datetime():
    now = datetime.now()
    return now.strftime("%d-%b-%Y %H:%M")


# Helper function to convert a string to camelCase
def to_camel_case(s):
    s = re.sub(r'[^a-zA-Z0-9]', ' ', s)
    s = ''.join(word.capitalize() for word in s.split())
    s = s[0].lower() + s[1:]
    return s
