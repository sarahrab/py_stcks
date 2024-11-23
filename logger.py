import logging
from datetime import datetime

from Utils.singleton import Singleton


class StocksAppLogger:
    log: logging.Logger = None

    @classmethod
    def initialize(cls):
        cls.log = logging.getLogger(__name__)
        logging.basicConfig(filename='stocks.log', level=logging.DEBUG)

    @classmethod
    def get_logger(cls) -> logging.Logger:
        return cls.log

    @classmethod
    def build_message(cls, text: str) -> str:
        return  f"    {datetime.now()}    {text}"

    @classmethod
    def debug(cls, text: str):
        cls.log.debug(cls.build_message(text))

    @classmethod
    def info(cls, text: str):
        cls.log.info(cls.build_message(text))

    @classmethod
    def warning(cls, text: str):
        cls.log.warning(cls.build_message(text))

    @classmethod
    def error(cls, text: str):
        cls.log.error(cls.build_message(text))

    @classmethod
    def critical(cls, text: str):
        cls.log.critical(cls.build_message(text))
