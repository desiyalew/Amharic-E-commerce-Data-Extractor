import logging

def setup_logger(name, level=logging.INFO):
    logging.basicConfig(level=level)
    return logging.getLogger(name)