import logging
import logging.config as log_config
from datetime import datetime
import yaml
import os


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
    def __init__(self, section_name, uid=None, rid=None, project_name='gp_web') -> None:
        config_logging()
        logging.setLoggerClass(CustomLogger)
        self.logger = logging.getLogger(project_name)
        self.section_name = section_name
        self.manual_log = {}
        if uid:
            self.manual_log['uid'] = uid
        if rid:
            self.manual_log['rid'] = rid


    def check_msg(self, log_msg):
        if isinstance(log_msg, dict):
            return log_msg
        else:
            return {f'msg_{type(log_msg).__name__}': log_msg}

    def log(self, level, log_msg):
        caller_info = self.logger.find_caller()
        log_entry = {
            "file": caller_info[0],
            "line": caller_info[1],
            "function": caller_info[2],
            **self.manual_log,
            self.section_name: self.check_msg(log_msg)
        }
        getattr(self.logger, level)(log_entry)

    def info(self, log_msg):
        self.log('info', log_msg)

    def warning(self, log_msg):
        self.log('warning', log_msg)

    def error(self, log_msg):
        self.log('error', log_msg)

    def debug(self, log_msg):
        self.log('debug', log_msg)
