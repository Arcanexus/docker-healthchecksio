import src.main as main
import yaml

def test_get_formatted_datetime():
  assert main.get_formatted_datetime()

def test_read_config():
  config = main.read_config("src/config")
  assert yaml.dump(config)

def test_checkHTTPSuccess():
  assert main.check_serviceHTTP("https://www.google.com")

def test_checkHTTPFail():
  res = main.check_serviceHTTP("https://www.unknownurlfqdn.com")
  assert res == False