import logging
import sys


def setup_logger():
    logger = logging.getLogger("Bootstrap")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s: %(message)s", datefmt="%H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
