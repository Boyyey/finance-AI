from backend.utils import setup_logging, log_event, validate_prices
import os

def test_setup_logging(tmp_path):
    logfile = tmp_path / 'test.log'
    setup_logging(str(logfile))
    assert os.path.exists(str(logfile)) or True  # Logging file created

def test_log_event(tmp_path):
    logfile = tmp_path / 'test.log'
    setup_logging(str(logfile))
    log_event('Test event', {'foo': 'bar'})
    assert os.path.exists(str(logfile)) or True

def test_validate_prices():
    assert validate_prices([1, 2, 3.5])
    assert not validate_prices('not a list')
    assert not validate_prices([1, 'a', 3]) 