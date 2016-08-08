""""""
from os import environ
from urllib import urlencode, unquote

AGENT_PROJECT_DIR = 'watch-page'
AGENT_PACKAGE_DIR = 'watch_page'

AGENT_TYPE = 'watch'
PAGE_TYPE = 'tos'
AGENT_ATTRIBUTE = 'page/content'

# STORE_CONFIG_DOC = 'pages'
STORE_CONFIG_DOC_DEFAULT = 'pages-juga'
# DB_NAME = 'pages-juga'
DB_NAME_DEFAULT = 'pages-juga-v3'

# STORE_LATEST_VIEW_NAME = 'page/latest'
# # STORE_LATEST_VIEW_DOC = '_design/%s/_view/%s?' % STORE_LATEST_VIEW.split('/')
# STORE_LATEST_VIEW_PARAMS = {'group': True, 'startkey': ["page", "%s"]}
STORE_LATEST_VIEW_NAME = 'page/latest_page'
STORE_LATEST_VIEW_PARAMS = {
        'group_level': 2,
        'startkey': ["page","%s",""],
        'endkey': ["page","%s",{}]
    }
STORE_LATEST_VIEW_OPTIONS  = unquote(urlencode(STORE_LATEST_VIEW_PARAMS))

STORE_UPDATE_DOC_NAME = "page/timestamped"
STORE_UPDATE_DOC_PART = "_design/page/_update/timestamped/%s"

SERVICE_NAME = 'watch_page_tos'

# configuration specific for watch
###################################
FETCH_PAGE_HOST = environ.get('FETCH_PAGE_HOST')
FETCH_PAGE_PORT = environ.get('FETCH_PAGE_PORT')
if FETCH_PAGE_HOST and FETCH_PAGE_PORT:
    FETCH_PAGE_DOMAIN = 'http://' + ":".join([FETCH_PAGE_HOST, FETCH_PAGE_PORT])
else:
    FETCH_PAGE_DOMAIN = 'http://127.0.0.1:8001'
FETCH_PAGE_NAME = 'fetch_page_tos'
FETCH_PAGE_URL = '/'.join([FETCH_PAGE_DOMAIN, FETCH_PAGE_NAME])
