import click
import json
import logging
import sys
import traceback
from copy import copy
from uvicorn.logging import AccessFormatter


class DefaultColorFormatter(logging.Formatter):
    """MLaaS default format with color in level.

    Change log level to custom color in stdout.

    color mapping list:
      - DEBUG: cyan
      - INFO: green
      - WARNING: yellow
      - ERROR: red
      - CRITICAL: bright_red

    """
    level_name_colors = {
        logging.DEBUG:
            lambda level_name: click.style(str(level_name),
                                           fg="cyan"),
        logging.INFO:
            lambda level_name: click.style(str(level_name),
                                           fg="green"),
        logging.WARNING:
            lambda level_name: click.style(str(level_name),
                                           fg="yellow"),
        logging.ERROR:
            lambda level_name: click.style(str(level_name),
                                           fg="red"),
        logging.CRITICAL:
            lambda level_name: click.style(str(level_name),
                                           fg="bright_red"),
    }

    def color_level_name(self, level_name, level_no):
        """Change level color in log record.

        Args:
          - level_name: str
          - level_no: int

        """
        default = lambda level_name: str(level_name)  # noqa
        func = self.level_name_colors.get(level_no, default)
        return func(level_name)


class AicloudFormatter(DefaultColorFormatter):
    """Aicloud log format.

    Args:
      - fmt: log format
      - datefmt: datetime format
      - style: format style
      - use_colors: change log object color

    """
    def __init__(self, fmt=None, datefmt=None, style="%", use_colors=None):
        if use_colors in (True, False):
            self.use_colors = use_colors
        else:
            self.use_colors = sys.stdout.isatty()
        super(AicloudFormatter, self).__init__(fmt=fmt,
                                               datefmt=datefmt,
                                               style=style)

    def formatMessage(self, record):
        """Custom record object value color.

        change levelanme, logger, function, file color to bright_blue.

        Args:
          - record: log object

        """
        levelname = record.levelname
        logger_name = record.name
        function_name = record.funcName
        file_name = record.filename
        if self.use_colors:
            record.levelname = self.color_level_name(levelname, record.levelno)
            if logger_name == 'fastapi':
                record.name = click.style(str(logger_name), fg="bright_blue")
            else:
                record.name = click.style(str(logger_name), fg="bright_cyan")
            record.funcName = click.style(str(function_name), fg="bright_blue")
            record.filename = click.style(str(file_name), fg="bright_blue")
        return super(AicloudFormatter, self).formatMessage(record)

    def format(self, record):
        "MLaaS custom record format"
        recordcopy = copy(record)
        s = super(AicloudFormatter, self).format(recordcopy)
        return s


class CustomAccessFormator(AccessFormatter):
    def formatMessage(self, record: logging.LogRecord) -> str:
        recordcopy = copy(record)
        (
            client_addr,
            method,
            full_path,
            http_version,
            status_code,
        ) = recordcopy.args  # type: ignore[misc]
        status_code = self.get_status_code(int(status_code))  # type: ignore[arg-type]
        request_line = "%s %s HTTP/%s" % (method, full_path, http_version)
        if self.use_colors:
            request_line = click.style(request_line, bold=True)
        recordcopy.__dict__.update(
            {
                "method": method,
                "full_path": full_path,
                "client_addr": client_addr,
                "request_line": request_line,
                "status_code": status_code,
                "http_version": http_version,
            }
        )
        return super().formatMessage(recordcopy)


class OneLineExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        """Exception custom format.

        Custom mlaas log format with exception.

        Args:
          - exc_info: traceback info

        """
        e_type, e_value, e_traceback = exc_info
        first_call_stack = traceback.extract_tb(e_traceback)[0]
        last_call_stack = traceback.extract_tb(e_traceback)[-1]
        e_value = str(e_value).replace('"', '')
        e_value = ' '.join(e_value.split())
        if first_call_stack == last_call_stack:
            traceback_msg = '"err_type":"%s", "err_info":"%s", "final_err_filename":"%s", "final_err_lineno":"%d", "final_err_function":"%s"}' % (  # noqa
                e_type.__name__, e_value, last_call_stack[0],
                last_call_stack[1], last_call_stack[2])
        else:
            traceback_msg = '"err_type":"%s", "err_info":"%s", "first_err_filename":"%s", "first_err_lineno":"%d", "first_err_function":"%s", "final_err_filename":"%s", "final_err_lineno":"%d", "final_err_function":"%s"}' % (  # noqa
                e_type.__name__, e_value,
                first_call_stack[0], first_call_stack[1],
                first_call_stack[2], last_call_stack[0],
                last_call_stack[1], last_call_stack[2])
        return traceback_msg

    def format(self, record):
        """MLaaS custom log record format.

        change record.msg type from str to json.

        Args:
          - record: log object
        """
        recordcopy = copy(record)
        if isinstance(recordcopy.msg, dict):
            for key in recordcopy.msg.keys():
                if isinstance(recordcopy.msg[key], str):
                    recordcopy.msg[key] = recordcopy.msg[key].replace(
                        '"', "'").replace('\r', ' ').replace('\n', ' ')
            recordcopy.msg = json.dumps(recordcopy.msg, ensure_ascii=False)
        else:
            recordcopy.msg = recordcopy.msg.replace('"', "'").replace(
                '\r', ' ').replace('\n', ' ')
            recordcopy.msg = json.dumps(dict(msg_body=recordcopy.msg),
                                        ensure_ascii=False)
        s = super(OneLineExceptionFormatter, self).format(recordcopy)
        if recordcopy.exc_text:
            s = s.replace('}\n', ', ')
            s = s.replace('\r', ' ').replace('\n', ' ')
            s = s.replace('^', '')
        else:
            s = s.replace('\r', ' ').replace('\n', ' ')
            s = s.replace('\n', ' ')
        return s
