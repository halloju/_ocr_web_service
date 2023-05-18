import logging
import logging.config as log_config
from datetime import datetime

import yaml


def config_logging(filename='log_config.yml'):
    log_filename = f"./app/logger/{datetime.now().strftime('%Y-%m-%d')}.log"
    with open(filename) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        # print(config)
        config['handlers']['file']['filename'] = log_filename
        log_config.dictConfig(config)

class Logger(object):
    def __init__(self, section_name, project_name='if_gp_ocr_system_backend') -> None:
        config_logging()
        self.logger = logging.getLogger(project_name)
        self.section_name = section_name
        self.log_dict = dict()

    def check_msg(self, log_msg):
        if isinstance(log_msg, dict):
            return log_msg
        else:
            return {f'msg_{type(log_msg).__name__}': str(log_msg)}

    def info(self, log_msg):
        self.log_dict[self.section_name] = self.check_msg(log_msg)
        self.logger.info(self.log_dict)

    def warning(self, log_msg):
        self.log_dict[self.section_name] = self.check_msg(log_msg)
        self.logger.warning(self.log_dict)

    def error(self, log_msg):
        self.log_dict[self.section_name] = self.check_msg(log_msg)
        self.logger.error(self.log_dict)

    def debug(self, log_msg):
        self.log_dict[self.section_name] = self.check_msg(log_msg)
        self.logger.debug(self.log_dict)
