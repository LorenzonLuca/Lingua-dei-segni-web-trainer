import logging
from logging.handlers import RotatingFileHandler
import models.Utils as utils

class Logger:
    def __init__(self, app):
        self.app = app

        log_formatter = logging.Formatter("[%(levelname)s] - %(message)s")
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        logger.addHandler(console_handler)

        max_length_handler = RotatingFileHandler(filename="record.log", mode='a', maxBytes=10*1024*1024, backupCount=2, encoding=None, delay=0)
        max_length_handler.setFormatter(log_formatter)
        logger.addHandler(max_length_handler)

    # info log function
    def info(self, msg, source = ' SERVER  '):
        self.app.logger.info(f'{source} - - [{utils.get_formatted_date()}] {msg}')

    def warning(self, msg, source = ' SERVER  '):
        self.app.logger.warning(f'{source} - - [{utils.get_formatted_date()}] {msg}')
    
    def error(self, msg, source = ' SERVER  '):
        self.app.logger.error(f'{source} - - [{utils.get_formatted_date()}] {msg}')
    
    def performance(self, msg, func, *args):
        bf = utils.current_time_ms()
        res = func(*args)
        af = utils.current_time_ms()
        self.app.logger.info(f'PERFORMANCE - [{utils.get_formatted_date()}] {msg}: {af-bf} ms')
        return res