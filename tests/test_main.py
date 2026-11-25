from unittest.mock import Mock

import pytest
import requests
import src.main as main
import yaml
from modules import checks

def test_get_formatted_datetime():
  assert main.get_formatted_datetime()

def test_read_config():
  config = main.read_config("src/config")
  assert yaml.dump(config)

@pytest.mark.parametrize("status_code, expected", [
  (200, True), (204, True), (299, True), (401, True), (403, True),
  (300, False), (404, False), (500, False),
])
def test_checkHTTPStatus(monkeypatch, status_code, expected):
  get = Mock(return_value=Mock(status_code=status_code, reason="test"))
  monkeypatch.setattr(checks.requests, "get", get)

  assert main.check_serviceHTTP("https://example.test", check_ssl=False) is expected
  get.assert_called_once_with("https://example.test", allow_redirects=True, verify=False)

@pytest.mark.parametrize("error", [
  requests.exceptions.SSLError("SSL failure"),
  requests.exceptions.ConnectionError("connection failure"),
])
def test_checkHTTPFail(monkeypatch, error):
  get = Mock(side_effect=error)
  monkeypatch.setattr(checks.requests, "get", get)

  assert main.check_serviceHTTP("https://example.test") is False
  get.assert_called_once_with("https://example.test", allow_redirects=True, verify=True)

def test_checkTCPSuccess(monkeypatch):
  sock = Mock()
  create_socket = Mock(return_value=sock)
  monkeypatch.setattr(checks.socket, "socket", create_socket)

  assert main.check_serviceTCP("example.test", 443)
  create_socket.assert_called_once_with(checks.socket.AF_INET, checks.socket.SOCK_STREAM)
  sock.settimeout.assert_called_once_with(5)
  sock.connect.assert_called_once_with(("example.test", 443))
  sock.close.assert_called_once_with()

@pytest.mark.parametrize("error", [checks.socket.timeout("timeout"), OSError("connection failure")])
def test_checkTCPFail(monkeypatch, error):
  sock = Mock()
  sock.connect.side_effect = error
  monkeypatch.setattr(checks.socket, "socket", Mock(return_value=sock))

  assert main.check_serviceTCP("example.test", 10) is False
  sock.connect.assert_called_once_with(("example.test", 10))
