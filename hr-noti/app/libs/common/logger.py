import sys
import os
import logging


class LogLevel:
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class TraceException:
    def __init__(self, *error_message):
        ex_str = ""
        for item in error_message:
            ex_str += str(item) + " "
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        self.message = '{}:{}-{}:{}'.format(fname, exc_tb.tb_lineno, exc_type, ex_str)

    def get_message(self):
        return self.message

    # def write_log(self):
    #     logger.log(LogLevel.ERROR, self.message)

    def __str__(self):
        return self.message
