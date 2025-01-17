import logging
import os
from logging.handlers import RotatingFileHandler

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[92m',  # Green
        'INFO': '\033[94m',   # Blue
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',  # Red
        'CRITICAL': '\033[95m',  # Magenta
        'RESET': '\033[0m'    # Reset
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        message = super().format(record)
        return f"{color}{message}{self.COLORS['RESET']}"

class PlainFormatter(logging.Formatter):
    def format(self, record):
        return super().format(record)

def setup_logger():
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)

    # Ensure the logs directory exists
    log_dir = os.path.join(os.path.dirname(__file__), '../logs')
    os.makedirs(log_dir, exist_ok=True)

    # Create rotating file handler
    log_file = os.path.join(log_dir, 'logs.log')
    fh = RotatingFileHandler(log_file, maxBytes=0, backupCount=5)
    fh.setLevel(logging.DEBUG)

    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create formatters and add them to the handlers
    plain_formatter = PlainFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    colored_formatter = ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(plain_formatter)
    ch.setFormatter(colored_formatter)

    # Add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.debug('Logger setup complete')
    return logger
