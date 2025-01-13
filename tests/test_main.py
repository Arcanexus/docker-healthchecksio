import src.modules.checks as checks
import src.modules.common as common
# import src.modules.config as config
# import yaml


def test_get_formatted_datetime():
  assert common.get_formatted_datetime()


# def test_get_config_value():
#   value = config.current_config.config.get("some_key")
#   assert value is not None

# def test_read_config():
#   # services_config = config.current_config.config["services"]
#   current_config = config.read_config("src/config/")
#   assert yaml.dump(current_config)


def test_checkHTTPSuccess():
  assert checks.check_serviceHTTP("https://www.google.com")


def test_checkHTTPFail():
  res = checks.check_serviceHTTP("https://www.unknownurlfqdn.com")
  assert res == False


def test_checkTCPSuccess():
  assert checks.check_serviceTCP("www.google.com", 443)


def test_checkTCPFail():
  res = checks.check_serviceTCP("www.unknownurlfqdn.com", 10)
  assert res == False