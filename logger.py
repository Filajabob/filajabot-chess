import logging


def setup_logger(name, log_file):
    # Create a filajabot_logger
    logger = logging.getLogger(name)

    # Set the logging level (you can change this to control verbosity)
    logger.setLevel(logging.DEBUG)

    # Create a file handler to log to a file
    file_handler = logging.FileHandler(log_file)

    # Create a console handler to log to the console (optional)
    console_handler = logging.StreamHandler()

    # Define the log format
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the filajabot_logger
    logger.addHandler(file_handler)

    return logger


filajabot_logger = setup_logger("filajabot", "logs/filajabot_logs.log")
