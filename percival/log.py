#import logging.config
import os
from datetime import datetime

percival_log_config = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(name)48s [%(filename)22s:%(lineno)4d]  %(levelname)7s -  %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(name)48s %(levelname)6s - %(message)s'
        },
    },
    'handlers': {
        'console':{
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'log_file': {
            'class': 'percival.mkdir_handler.MkDirRotatingFileHandler',
            'formatter': 'simple',
            'filename': './logs/percival.log',  #.format(datetime.now()
                                                #        .isoformat()
                                                #        .replace(':', '_')
                                                #        .replace('-', '_')),
            'maxBytes': 5242880,
            'backupCount': 20
        },
        'trace_file': {
            'class': 'percival.mkdir_handler.MkDirRotatingFileHandler',
            'formatter': 'simple',
            'filename': './logs/percival_trace.log',  #.format(datetime.now()
                                                      #        .isoformat()
                                                      #        .replace(':', '_')
                                                      #        .replace('-', '_')),
            'maxBytes': 5242880,
            'backupCount': 20
        }
    },
    'loggers': {
        '': {
            'handlers': ['log_file', "console"],
            'propagate': False,
            'level': 'INFO',
        },
        'percival_sandbox': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'INFO',
        },
        'percival_trace': {
            'handlers': ['trace_file'],
            'propagate': False,
            'level': 'INFO',
        },
        'percival': {
            'handlers': ['log_file'],
            'propagate': False,
            'level': 'INFO',
        },
        'percival.spreadsheet_parser': {
            'handlers': ['log_file'],
            'propagate': False,
            'level': 'INFO',
        },
        'percival.carrier': {
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'percival.carrier.simulator': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'percival.carrier.system.SystemSettings': {
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'percival.carrier.sensor.Sensor': {
            'handlers': ['log_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'percival.carrier.buffer': {
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'percival.carrier.buffer.BufferCommand': {
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'percival.carrier.channels': {
            'handlers': ['log_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'percival.carrier.channels.ControlChannel': {
            'handlers': ['log_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'percival.carrier.channels.MonitoringChannel': {
            'handlers': ['log_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'percival.carrier.configuration.SetpointGroupParameters': {
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'percival.carrier.configuration.ControlParameters': {
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'percival.carrier.devices': {
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'percival.carrier.encoding': {
            'handlers': ['log_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'percival.carrier.txrx': {
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'percival.carrier.txrx.TxRx': {
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'percival.control': {
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'percival.detector': {
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'percival.detector.ipc_reactor.IpcReactor': {
            'handlers': ['log_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'percival.detector.standalone.PercivalStandalone': {
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'percival.detector.set_point.SetPointControl': {
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'percival.detector.detector.PercivalParameters': {
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'percival.detector.detector.PercivalDetector': {
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'percival.detector.adapter.PercivalAdapter': {
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'BoardSettings': {
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'percival.configuration.ChannelParameters': {
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}


# logging.config.dictConfig(percival_log_config)

import logging
import logging.config
logging.config.dictConfig(percival_log_config)
log = logging.getLogger("percival")


def logger(name):
    return logging.getLogger(name)


def get_exclusive_file_logger(filename):
    """Return a percival logger with a file handler

    Creates a file handler and removes the existing console handler from the standard percival logger instance. This can
    be used in console-gui applications where writing log messages to stdout/stderr would corrupt the display.

        :param filename: Name of file to write log messages to
        :type filename:  str
        :returns: A logger object with an attached file handler
        :rtype logging.logger:
    """
    check_create_path(filename)
    ch = logging.FileHandler(str(filename), )
    ch.setLevel(log.getEffectiveLevel())
    fmt = logging.Formatter(percival_log_config['formatters']['simple']['format'])
    ch.setFormatter(fmt)
    log.addHandler(ch)

    # Remove console handlers
    console_handlers = [hndlr for hndlr in log.handlers if hndlr.name == 'console']
    for hndlr in console_handlers:
        log.removeHandler(hndlr)
    return log


def check_create_path(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
