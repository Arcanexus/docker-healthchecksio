# import src.main as main
import src.modules.checks as checks
from src.modules.config import Config

current_config = Config("src/config/config.yml.sample")


def test_checkHTTPSuccess():
  assert checks.check_serviceHTTP("https://www.google.com")


def test_checkHTTPFail():
  res = checks.check_serviceHTTP("https://www.unknownurlfqdn123.com")
  assert res is False


def test_checkTCPSuccess():
  assert checks.check_serviceTCP("www.google.com", 443)


def test_checkTCPFail():
  res = checks.check_serviceTCP("www.unknownurlfqdn123.com", 10)
  assert res is False
