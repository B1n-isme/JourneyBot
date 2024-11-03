import logging

def setup_logger():
    logging.basicConfig(level=logging.ERROR)
    logger = logging.getLogger(__name__)
    logging.getLogger("langchain").setLevel(logging.ERROR)
