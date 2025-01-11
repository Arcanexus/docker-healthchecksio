import src.main as main
import src.modules.common as common
import src.modules.config as config
import yaml


def test_get_formatted_datetime():
  assert common.get_formatted_datetime()


def test_read_config():
  services_config = config.current_config.config["services"]
  assert yaml.dump(services_config)


def test_checkHTTPSuccess():
  assert main.check_serviceHTTP("https://www.google.com")


def test_checkHTTPFail():
  res = main.check_serviceHTTP("https://www.unknownurlfqdn.com")
  assert res == False


def test_checkTCPSuccess():
  assert main.check_serviceTCP("www.google.com", 443)


def test_checkTCPFail():
  res = main.check_serviceTCP("www.unknownurlfqdn.com", 10)
  assert res == False