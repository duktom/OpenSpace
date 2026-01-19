import sys
import logging

from colorlog import ColoredFormatter

formetter = ColoredFormatter(
    "%(log_color)s%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formetter)

logging.basicConfig(
    level=logging.INFO,
    handlers=[stream_handler]
)


def get_logger(name: str):
    return logging.getLogger(name)
