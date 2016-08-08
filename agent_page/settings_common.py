from os import environ
from os.path import join

DEBUG = environ.get('DEBUG') or False
CONSOLE_LOG_DEFAULT = 'INFO'
DATA_DIR_DEFAULT = 'data'
LOG_DIR_DEFAULT = 'log'
LOG_FILE_DEFAULT = join(LOG_DIR_DEFAULT, 'info.log')
LOG_ERROR_FILE_DEFAULT = join(LOG_DIR_DEFAULT, 'error.log')
AGENTS_MODULE_DIR = 'agents_common'

STORE_URL_DEFAULT = 'https://staging-store.openintegrity.org'
STORE_CONFIG_DB_DEFAULT = 'config'

NAME_SEPARATOR = '-'
INTERVAL = 60
CONFIG_DOC_KEY = 'config'
