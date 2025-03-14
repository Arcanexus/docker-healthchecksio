# import src.main as main
import src.modules.checks as checks
from src.modules.config import Config
import pytest


@pytest.fixture(scope="module")
def current_config():
  current_config = Config("src/config/config.yml.sample")
  return current_config


@pytest.mark.usefixtures("current_config")
def test_checkHTTPSuccess():
  assert checks.check_serviceHTTP("https://www.google.com")


@pytest.mark.usefixtures("current_config")
def test_checkHTTPFail():
  res = checks.check_serviceHTTP("https://www.unknownurlfqdn123.com")
  assert res is False


@pytest.mark.usefixtures("current_config")
def test_checkTCPSuccess():
  assert checks.check_serviceTCP("www.google.com", 443)


@pytest.mark.usefixtures("current_config")
def test_checkTCPFail():
  res = checks.check_serviceTCP("www.unknownurlfqdn123.com", 10)
  assert res is False
