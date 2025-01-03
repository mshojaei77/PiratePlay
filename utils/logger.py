import logging
import coloredlogs
import inspect
import os

class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self, name='PiratePlay', log_level=logging.DEBUG, exc_info=True):
        if not hasattr(self, 'initialized'):
            self.logger = logging.getLogger(name)
            self.setup_logging(log_level)
            self.initialized = True

    def setup_logging(self, log_level):
        coloredlogs.install(
            level=log_level,
            logger=self.logger,
            fmt='%(name)s - %(levelname)s - %(message)s',
            level_styles={
                'debug': {'color': 'cyan', 'bold': True},
                'info': {'color': 'green', 'bold': True}, 
                'warning': {'color': 'yellow', 'bold': True},
                'error': {'color': 'red', 'bold': True},
                'critical': {'color': 'magenta', 'bold': True, 'background': 'red'},
            }
        )

    def _get_caller_info(self):
        # Get the caller's frame info, skipping this function and the logging function
        frame = inspect.currentframe()
        # Skip this function and the logging function
        caller_frame = frame.f_back.f_back
        filename = os.path.basename(caller_frame.f_code.co_filename)
        func_name = caller_frame.f_code.co_name
        return filename, func_name

    def debug(self, message, exc_info=True):
        filename, func_name = self._get_caller_info()
        self.logger.debug(f"\033[36m[{filename}:{func_name}]\033[0m - {message}")

    def info(self, message, exc_info=True):
        filename, func_name = self._get_caller_info()
        self.logger.info(f"\033[32m[{filename}:{func_name}]\033[0m - {message}")

    def warning(self, message, exc_info=True):
        filename, func_name = self._get_caller_info()
        self.logger.warning(f"\033[33m[{filename}:{func_name}]\033[0m - {message}")

    def error(self, message, exc_info=True):
        filename, func_name = self._get_caller_info()
        self.logger.error(f"\033[31m[{filename}:{func_name}]\033[0m - {message}")

    def critical(self, message, exc_info=True):
        filename, func_name = self._get_caller_info()
        self.logger.critical(f"\033[35m[{filename}:{func_name}]\033[0m - {message}")

# Create a global logger instance
app_logger = Logger()

# Usage example:
# from utils.logger import app_logger
# app_logger.info("This is an info message")
