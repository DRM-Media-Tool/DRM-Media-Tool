import os
import logging
import sys


def setup_logging():
    # Get the directory of the script or the executable
    if getattr(sys, 'frozen', False):  # if the application is frozen
        current_dir = os.path.dirname(sys.executable)
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))

    log_dir = os.path.join(current_dir, 'logs')
    os.makedirs(log_dir, exist_ok=True)

    info_log_file = os.path.join(log_dir, 'info.log')
    debug_log_file = os.path.join(log_dir, 'debug.log')

    # Configuration for info_logger
    info_logger = logging.getLogger('info_logger')
    info_handler = logging.FileHandler(info_log_file)
    info_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    info_handler.setFormatter(info_formatter)
    info_logger.addHandler(info_handler)
    info_logger.setLevel(logging.INFO)

    # Configuration for debug_logger
    debug_logger = logging.getLogger('debug_logger')
    debug_handler = logging.FileHandler(debug_log_file)
    debug_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    debug_handler.setFormatter(debug_formatter)
    debug_logger.addHandler(debug_handler)
    debug_logger.setLevel(logging.DEBUG)

    return info_logger, debug_logger


if __name__ == "__main__":
    setup_logging()
