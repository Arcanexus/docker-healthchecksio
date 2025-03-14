import logging
import sys
import threading
import pytest
from unittest.mock import patch, MagicMock
from src.modules.logger import CustomFormatter, get_logger


@pytest.fixture
def mock_config():
    with patch('src.modules.logger.current_config', {
        'config.logs.log_level': 'DEBUG',
        'config.logs.format': 'console'
    }):
        yield


def test_custom_formatter_debug(mock_config):
    formatter = CustomFormatter()
    record = logging.LogRecord(
        name='test', level=logging.DEBUG, pathname='', lineno=0, msg='Test UP message', args=(), exc_info=None
    )
    formatted_message = formatter.format(record)
    assert 'UP' in formatted_message
    assert 'DEBUG' in formatted_message


def test_custom_formatter_info(mock_config):
    formatter = CustomFormatter()
    record = logging.LogRecord(
        name='test', level=logging.INFO, pathname='', lineno=0, msg='Test DOWN message', args=(), exc_info=None
    )
    formatted_message = formatter.format(record)
    assert 'DOWN' in formatted_message
    assert 'INFO' in formatted_message


def test_custom_formatter_warning(mock_config):
    formatter = CustomFormatter()
    record = logging.LogRecord(
        name='test', level=logging.WARNING, pathname='', lineno=0, msg='Test DOWN message', args=(), exc_info=None
    )
    formatted_message = formatter.format(record)
    assert 'DOWN' in formatted_message
    assert 'WARNING' in formatted_message


def test_custom_formatter_error(mock_config):
    formatter = CustomFormatter()
    record = logging.LogRecord(
        name='test', level=logging.ERROR, pathname='', lineno=0, msg='Test DOWN message', args=(), exc_info=None
    )
    formatted_message = formatter.format(record)
    assert 'DOWN' in formatted_message
    assert 'ERROR' in formatted_message


def test_custom_formatter_critical(mock_config):
    formatter = CustomFormatter()
    record = logging.LogRecord(
        name='test', level=logging.CRITICAL, pathname='', lineno=0, msg='Test DOWN message', args=(), exc_info=None
    )
    formatted_message = formatter.format(record)
    assert 'DOWN' in formatted_message
    assert 'CRITICAL' in formatted_message


# def test_get_logger_console_format(mock_config):
#     logger = get_logger(loglevel='DEBUG', logformat='console')
#     assert logger.level == logging.DEBUG
#     assert isinstance(logger.handlers[0].formatter, CustomFormatter)


# def test_get_logger_logfmt_format(mock_config):
#     logger = get_logger(loglevel='DEBUG', logformat='logfmt')
#     assert logger.level == logging.DEBUG
#     assert logger.handlers[0].formatter.__class__.__name__ == 'Logfmter'


# def test_get_logger_json_format(mock_config):
#     logger = get_logger(loglevel='DEBUG', logformat='json')
#     assert logger.level == logging.DEBUG
#     assert logger.handlers[0].formatter.__class__.__name__ == 'JsonFormatter'
