import logging

# ANSI escape codes for colored terminal output
COLORS = {
    'DEBUG': '\033[94m',  # Blue
    'INFO': '\033[92m',  # Green
    'WARNING': '\033[93m',  # Yellow
    'ERROR': '\033[91m',  # Red
    'CRITICAL': '\033[95m',  # Magenta
    'RESET': '\033[0m',  # Reset to default color
}


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_color = COLORS.get(record.levelname, COLORS[
            'RESET'])  # Get the color for the log level
        reset_color = COLORS['RESET']  # Reset color after the message

        # Add color codes to the log message
        record.msg = f"{log_color}{record.msg}{reset_color}"

        # Call the base class's format method to output the rest of the
        # formatted message
        return super().format(record)


# Define a function to configure logging
def configure_logging():
    # Create a console handler
    console_handler = logging.StreamHandler()

    # Create and set the colored formatter
    formatter = ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Get the root logger and configure it
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Set the logging level globally
    logger.addHandler(console_handler)

    # Optional: if you want to prevent duplicate logs, remove default handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(console_handler)


configure_logging()
