# import src.main as main
import src.modules.checks as checks
import src.modules.common as common


def test_get_formatted_datetime():
  assert common.get_formatted_datetime()


def test_checkHTTPSuccess():
  assert checks.check_serviceHTTP("https://www.google.com")


def test_checkHTTPFail():
  res = checks.check_serviceHTTP("https://www.unknownurlfqdn.com")
  assert res is False


def test_checkTCPSuccess():
  assert checks.check_serviceTCP("www.google.com", 443)


def test_checkTCPFail():
  res = checks.check_serviceTCP("www.unknownurlfqdn.com", 10)
  assert res is False
