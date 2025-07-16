import logging
import json

def setup_logging(logfile='backend.log'):
    """
    Set up logging to a file.
    Args:
        logfile (str): Path to log file.
    """
    logging.basicConfig(
        filename=logfile,
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s'
    )

def log_event(event, data=None):
    """
    Log an event with optional data.
    Args:
        event (str): Event description.
        data (dict, optional): Additional data.
    """
    if data:
        logging.info(f"{event}: {json.dumps(data)}")
    else:
        logging.info(event)

def validate_prices(prices):
    """
    Validate that prices is a list of numbers.
    Args:
        prices (list): List to validate.
    Returns:
        bool: True if valid, False otherwise.
    """
    if not isinstance(prices, list):
        return False
    return all(isinstance(x, (int, float)) for x in prices) 