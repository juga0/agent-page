""""""
import logging
from datetime import datetime

from couchdb.mapping import Document, TextField, IntegerField, DateTimeField, \
    ListField, DictField, Mapping, ViewField
from couchdb import Server

logger = logging.getLogger(__name__)


class ConfigRule(Mapping):
    url = TextField()
    xpath = TextField()
    organization = TextField()
    policy = TextField()
    tool = TextField()


class ConfigPagesDoc(Document):
    config = ListField(DictField(ConfigRule))


class PagesConfig(object):
    """
    """

    def __init__(self, config_db, config_doc_name):
        self.config = ConfigPagesDoc.load(config_db, config_doc_name)
        self.rules = self.config.config

    def destroy():
        pass


class Header(Mapping):
    etag = TextField(default='')
    # last_modified = DateTimeField(default=None)
    last_modified = TextField(default='')


class PageValue(Mapping):
    header = DictField(Header)
    content = TextField(default='')
    sha256_html = TextField(default='')
    sha256_md = TextField(default='')


class PageContext(Mapping):
    timestamp_measurement = DateTimeField(default=datetime.utcnow())
    agent_type = TextField(default='')
    agent_ip = TextField(default='')
    page_type = TextField(default='')
    xpath = TextField(default='')


class PageDoc(Document):
    entity = TextField(default='')
    attribute = TextField(default='')
    value = DictField(PageValue)
    context = DictField(PageContext)
