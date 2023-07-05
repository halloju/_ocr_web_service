import logging
import logging.config as log_config
from datetime import datetime

import yaml


def config_logging(filename='log_config.yml'):
    log_filename = f"./app/logger/{datetime.now().strftime('%Y-%m-%d')}.log"  # log
    with open(filename) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        # print(config)
        config['handlers']['file']['filename'] = log_filename
        log_config.dictConfig(config)


class Logger(object):
    def __init__(self, section_name, uid, rid, project_name='gp_ocr') -> None:
        config_logging()
        self.logger = logging.getLogger(project_name)
        self.section_name = section_name
        self.uid = uid
        self.rid = rid
        self.log_dict = dict()

    def check_msg(self, log_msg):
        if isinstance(log_msg, dict):
            return log_msg
        else:
            return {f'msg_{type(log_msg).__name__}': log_msg}

    def log(self, level, log_msg):
        log_entry = {
            "uid": self.uid,
            "rid": self.rid,
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
