from os import environ
from os.path import join

from settings_ro import PROJECT_PATH, ROOT_PATH
from settings_common import DEBUG, CONSOLE_LOG_DEFAULT, DATA_DIR_DEFAULT, \
    LOG_DIR_DEFAULT, LOG_FILE_DEFAULT, LOG_ERROR_FILE_DEFAULT, \
    AGENTS_MODULE_DIR, STORE_URL_DEFAULT, NAME_SEPARATOR, INTERVAL, \
    CONFIG_DOC_KEY, STORE_CONFIG_DB_DEFAULT
from settings_agent import STORE_CONFIG_DOC_DEFAULT, DB_NAME_DEFAULT
from settings_agent import PAGE_TYPE, FETCH_PAGE_URL



AGENTS_COMMON_PATH = join(PROJECT_PATH, AGENTS_MODULE_DIR)

# fs store
FS_PATH = environ.get('FS_PATH') or join(PROJECT_PATH, DATA_DIR_DEFAULT)

# URLs
############################
# couchdb configuration and urls
STORE_URL = environ.get('STORE_URL') or STORE_URL_DEFAULT
STORE_CONFIG_DB = environ.get('STORE_CONFIG_DB') or STORE_CONFIG_DB_DEFAULT
STORE_CONFIG_DOC = environ.get('STORE_CONFIG_DOC') or STORE_CONFIG_DOC_DEFAULT
STORE_CONFIG_URL = '/'.join([STORE_URL, STORE_CONFIG_DB, STORE_CONFIG_DOC])

# configuration that depends on common constants
STORE_DB = environ.get('DB_NAME') or DB_NAME_DEFAULT
STORE_DB_URL = '/'.join([STORE_URL, STORE_DB])
# STORE_LATEST_VIEW = '_design/page/_view/latest?reduce=true&group_level=2&' \
#     'startkey=["page","' + PAGE_TYPE + '","%s"]' \
#     '&endkey=["page","' + PAGE_TYPE + '","%s",{}]'
# STORE_LATEST_VIEW_URL = '/'.join([STORE_DB_URL, STORE_LATEST_VIEW])

# STORE_UPDATE_DOC_URL = '/'.join([STORE_DB_URL, STORE_UPDATE_DOC])

NEXT_AGENT_URL = FETCH_PAGE_URL

# logging
LOG_PATH = environ.get('LOG_PATH') or \
                            join(PROJECT_PATH, LOG_FILE_DEFAULT)
LOG_ERROR_PATH = environ.get('LOG_ERROR_PATH') or \
                            join(PROJECT_PATH, LOG_ERROR_FILE_DEFAULT)
LOG_LEVEL = environ.get('LOG_LEVEL') or \
            ('DEBUG' if DEBUG else CONSOLE_LOG_DEFAULT)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            # ERROR:watch_url_util - ...
            'format': "%(levelname)s: %(module)s - %(message)s"
        },
        'detailed': {
            'format': "%(levelname)s: %(filename)s:%(lineno)s - "
                      "%(funcName)s - %(message)s"
        },
        'syslog_like': {
            # Aug  1 11:22:43 host anacron[5063]: ...
            'format': "%(asctime)s %(name)s[%(process)d]: " \
                      "%(levelname)s - %(message)s",
                      # % {'host': environ.get('HOSTNAME'),
            'datefmt': '%B %d %H:%M:%S',
        }
    },
    'handlers': {
        'console_stderr': {
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
            'level': 'ERROR'
        },
        'console_stdout': {
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
            'level': LOG_LEVEL,
            'stream': 'ext://sys.stdout'
        },
        "debug_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "syslog_like",
            "filename": LOG_PATH,
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8"
        },
        "error_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "syslog_like",
            "filename": LOG_ERROR_PATH,
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8"
        }
    },
    'loggers': {
        'nameko': {
            'level': 'DEBUG',
            'handlers': ['console_stderr', 'debug_file_handler']
        },
        # uncomment this to get logs only from these modules and comment root
        'watch_service': {
            # DEBUG must be here to catch all possible logs
            # that will get filtered by the handler
            'level': 'DEBUG',
            'handlers': ['console_stderr', 'console_stdout',
                         'debug_file_handler']
        },
        'model_watch_page': {
            # DEBUG must be here to catch all possible logs
            # that will get filtered by the handler
            'level': 'DEBUG',
            'handlers': ['console_stderr', 'console_stdout',
                         'debug_file_handler']
        },
        'models': {
            # DEBUG must be here to catch all possible logs
            # that will get filtered by the handler
            'level': 'DEBUG',
            'handlers': ['console_stderr', 'console_stdout',
                         'debug_file_handler']
        },
        'agents_common': {
            # DEBUG must be here to catch all possible logs
            # that will get filtered by the handler
            'level': 'DEBUG',
            'handlers': ['console_stderr', 'console_stdout',
                         'debug_file_handler']
        }
    },
    # 'root': {
    #     # DEBUG must be here to catch all possible logs
    #     # that will get filtered by the handler
    #     'level': 'DEBUG',
    #     'handlers': ['console_stderr', 'console_stdout', 'debug_file_handler']
    # }
}

# nameko
############################
CONFIG_YAML_PATH = join(ROOT_PATH, 'config.yaml')
WEB_SERVER_ADDRESS = '127.0.0.1:8000'
# rabbitmq configuration
# this doesn't have any effect here
# AMQP_CONFIG = {'AMQP_URI': 'amqp://guest:guest@localhost'}
