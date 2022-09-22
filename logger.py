import logging.config
import os
from colored_logger import ColorFormatter

#ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(__file__)
LOGFILE = os.path.join(ROOT_DIR, os.path.basename(__file__).split('.')[0] + '.log')
if not os.path.exists(LOGFILE): 
    print(LOGFILE)
    with open(LOGFILE, 'w'): pass

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'minimal': {
            'format': '%(asctime)s:%(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'verbose': {
            'format': '%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d:%(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'color_format': {
            'class': 'logging.ColorFormatter',
            'format': '$TIME_COLOR%(asctime)s$RESET:$COLOR%(levelname)s$RESET:%(filename)s:%(lineno)d:%(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'color_format',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'filename': LOGFILE,
            'mode': 'w',
            'class': 'logging.FileHandler',
        },
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
        },
        'another.module': {
            'level': 'DEBUG',
        },
    },
}


logging.config.dictConfig(DEFAULT_LOGGING)