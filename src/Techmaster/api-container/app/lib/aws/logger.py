import logging, os
from datetime import datetime


class logger:
    def __init__(self) -> None:
        self.log = logging.getLogger()
        self.log.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        self.log.addHandler(ch)
        self.log.info("Log Initialied...")

    def write_log(self, log_message: str):
        self.log.info(str(datetime.now()) + " : " + str(log_message))

    def write_debug_loc(self, log_message: str):
        if os.getenv("DEBUG") == "TRUE":
            self.log.info(str(datetime.now()) + " : " + str(log_message))
