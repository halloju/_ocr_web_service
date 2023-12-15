import logging
import logging.config as log_config
from datetime import datetime
import yaml
import os
from html import escape

class RequestLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        # If the extra dictionary is not passed in kwargs, it's added.
        if 'extra' not in kwargs:
            kwargs['extra'] = {}
        # Include request_id in the 'extra' dictionary
        kwargs['extra']['request_id'] = self.extra.get('request_id', 'unknown')
        kwargs['extra']['user_id'] = self.extra.get('user_id', 'unknown')
        return msg, kwargs


class CustomLogger(logging.Logger):
    def find_caller(self, stack_info=False, stacklevel=1):
        """
        Find the stack frame of the caller, considering a custom stack level.
        This method overrides the default behavior to adjust the depth.
        """
        f = logging.currentframe()
        # Move up the stack to find the actual logging call
        while (stacklevel and f):
            f = f.f_back
            stacklevel -= 1
        rv = "(unknown file)", 0, "(unknown function)"
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == logging._srcfile:
                f = f.f_back
                continue
            rv = (co.co_filename, f.f_lineno, co.co_name)
            break
        return rv


def config_logging(filename='utils/log_config.yml'):
    log_filename = f"./log/{datetime.now().strftime('%Y-%m-%d')}.log"
    with open(filename) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        config['handlers']['file']['filename'] = log_filename
        log_config.dictConfig(config)


class Logger(object):
    def __init__(self, section_name, uid=None, rid=None) -> None:
        config_logging()
        logging.setLoggerClass(CustomLogger)
        self.raw_logger = logging.getLogger(section_name)
        self.section_name = section_name
        self.manual_log = {'uid': uid} if uid else {}
        # We create the adapter here
        self.logger = RequestLoggerAdapter(self.raw_logger, self.manual_log)

    def check_msg(self, log_msg):
        # Validate and sanitize the log message
        if isinstance(log_msg, dict):
            sanitized_msg = {key: self.check_msg(value) for key, value in log_msg.items()}
            return sanitized_msg
        elif isinstance(log_msg, str):
            return escape(log_msg[:1000])
        elif isinstance(log_msg, (int, float)):
            return log_msg
        else:
            return {f'msg_{type(log_msg).__name__}': escape(str(log_msg)[:1000])}

    def log(self, level, log_msg):
        log_entry = {
            **self.manual_log,
            self.section_name: self.check_msg(log_msg)
        }
        log_methods = {
            'debug': self.logger.debug,
            'info': self.logger.info,
            'warning': self.logger.warning,
            'error': self.logger.error,
            'critical': self.logger.critical
        }

        if level in log_methods:
            log_methods[level](log_entry)
        else:
            # Handle the case where the level is not recognized
            # For example, you might want to log this as an error or raise an exception
            self.logger.error(f"Unknown log level: {level}")


    def info(self, log_msg):
        self.log('info', log_msg)

    def warning(self, log_msg):
        self.log('warning', log_msg)

    def error(self, log_msg):
        self.log('error', log_msg)

    def debug(self, log_msg):
        self.log('debug', log_msg)
