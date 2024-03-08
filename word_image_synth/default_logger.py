import logging


def configure_app_logging():
    """
    Configure default logging for the application
    """
    log_level = logging.INFO

    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Create handlers
    stream_handler = logging.StreamHandler()

    # Create formatters and add it to handlers
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    stream_handler.setFormatter(logging.Formatter(log_format))

    # Add handlers to the logger
    logger.addHandler(stream_handler)
