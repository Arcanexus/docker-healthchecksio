import pytest
# from test_config import current_config
import src.modules.checks as checks
from unittest.mock import patch


@pytest.fixture
def mock_config():
    with patch('src.modules.logger.current_config', {
        'config.logs.log_level': 'DEBUG',
        'config.logs.format': 'console'
    }):
        yield

def test_checkHTTPSuccess(mock_config):
  assert checks.check_serviceHTTP("https://www.google.com")


def test_checkHTTPFail(mock_config):
  res = checks.check_serviceHTTP("https://www.unknownurlfqdn123.com")
  assert res is False


def test_checkTCPSuccess(mock_config):
  assert checks.check_serviceTCP("www.google.com", 443)


def test_checkTCPFail(mock_config):
  res = checks.check_serviceTCP("www.unknownurlfqdn123.com", 10)
  assert res is False


def test_checkHTTPSSLFail(mock_config):
  res = checks.check_serviceHTTP("https://self-signed.badssl.com/", check_ssl=True)
  assert res is False


def test_checkHTTPSSLSuccess(mock_config):
  res = checks.check_serviceHTTP("https://self-signed.badssl.com/", check_ssl=False)
  assert res is True


def test_checkTCPTimeout(mock_config):
  res = checks.check_serviceTCP("10.255.255.1", 80, timeout=1)
  assert res is False
