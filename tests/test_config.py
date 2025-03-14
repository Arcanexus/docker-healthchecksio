import src.modules.config as config
import yaml
import os

current_config = config.Config("src/config/config.yml.sample")

def test_read_config():
  current_config = config.read_config("src/config/config.yml.sample")
  assert yaml.dump(current_config)


def test_get_config_value():
  value = config.current_config.get('config.logs.log_level')
  assert value is not None


def test_config_path_exists():
  assert os.path.exists(config.config_path)


def test_config_has_services():
  services = config.current_config.config.get("services")
  assert services is not None
  assert isinstance(services, list)
  assert len(services) > 0


def test_config_log_level():
  log_level = config.current_config.get('config.logs.log_level')
  assert log_level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
