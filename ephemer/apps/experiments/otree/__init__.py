import logging


def _initialize_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s][%(name)s] - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


_initialize_logger()
