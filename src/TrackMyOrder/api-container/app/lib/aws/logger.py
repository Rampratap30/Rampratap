import logging, os
from datetime import datetime


class logger:
    def __init__(self) -> None:
        self.log = logging.getLogger()
        self.log.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        self.log.addHandler(ch)
        self.pid = os.getpid()
        self.log.info("Log Initialied for Pid: " + str(self.pid))

    def write_log(self, log_message: str):
        self.log.info(
            "PID : "
            + str(self.pid)
            + " : "
            + str(datetime.now())
            + " : "
            + str(log_message)
        )
