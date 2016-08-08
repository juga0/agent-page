""""""
import logging
import logging.config
from datetime import datetime
from couchdb import Server

from models import PagesConfig, PageDoc, PageContext, Header, PageValue

from settings import LOGGING
from settings_agent import STORE_LATEST_VIEW_NAME, STORE_LATEST_VIEW_PARAMS
from settings_agent import STORE_LATEST_VIEW_OPTIONS, STORE_UPDATE_DOC_PART
from settings_agent import STORE_UPDATE_DOC_NAME

from agents_common import obtain_public_ip, get_etag
from agents_common import gen_doc_id_etag_part, gen_doc_id, get_request
from agents_common import dtzutcstr2dtz

logger = logging.getLogger(__name__)


class WatchAgent(object):
    """
    """
    def __init__(self, store_url, db_name, config_db_name, config_doc_name,
                 agent_type, page_type, attribute, next_agent):
        logger.debug('Starting watch agent.')
        self.server = Server(store_url)
        self.db = self.server[db_name]
        self.next_agent_url = next_agent
        self.init_config(config_db_name, config_doc_name)
        self.init_page_all_rules(agent_type, page_type, attribute)

    def init_config(self, config_db_name, config_doc_name):
        logger.debug('Initializing config for pages.')
        self.config_db = self.server[config_db_name]
        self.config = PagesConfig(self.config_db, config_doc_name)
        self.rules = self.config.rules
        # logger.debug('Obtained rules %s.', self.rules)

    def init_page_all_rules(self, agent_type, page_type, attribute):
        logger.debug('Initializing page values for all rules.')
        self.agent_type = agent_type
        self.page_type = page_type
        self.attribute = attribute
        # self.sha256_html = ''
        # self.sha256_md = ''

    def init_page_per_rule(self, rule):
        logger.debug('Initializing rule.')
        # FIXME: when runing with tor, the Website request IP could be
        # different
        self.agent_ip = obtain_public_ip()
        # FIXME: timestamp should be calcualted in the very moment the request
        # is done
        self.timestamp_measurement = datetime.utcnow()
        logger.debug(self.timestamp_measurement)
        self.rule = rule
        self.xpath = rule.xpath
        self.entity = rule.url
        self.etag_store = ''
        # self.etag = ''
        self.last_modified_store = None
        # self.last_modified = None
        self.doc_id = None
        self.latest_page_doc = None
        self.value = None
        self.content = ''
        self.context = None
        self.page = None

    def process_rules(self):
        for rule in self.rules:
            logger.debug('Processing rule %s.', rule.url)
            self.process_rule(rule)

    def process_rule(self, rule):
        # FIXME
        self.init_page_per_rule(rule)
        self.get_etag_website()
        self.get_latest_page_doc()
        self.get_etag_store()
        if self.is_etag_different():
            self.gen_doc_id()
            self.gen_page()
            self.store_page()
            self.fetch_page()

    def get_etag_website(self):
        logger.info('Getting etag from Website with url %s.', self.entity)
        self.etag, self.last_modified = get_etag(self.entity)
        logger.debug('Latest etag Website %s.', self.etag)
        logger.debug('Latest last_modified Website %s.', self.last_modified)

    def get_etag_store(self):
        # FIXME
        # page = PageDoc()
        # page.load(self.db, doc_id)
        try:
            self.etag_store = self.latest_page_doc.value.header.etag
        except (AttributeError, KeyError) as e:
            logger.error('No etag in store.')
        logger.debug('Latest etag store %s.', self.etag_store)
        try:
            self.last_modified_store = \
                self.latest_page_doc.value.header.last_modified
        except (AttributeError, KeyError) as e:
            logger.error('No last_modified in store.')
        logger.debug('Latest last_modified store %s.',
                     self.last_modified_store)

    def get_latest_page_doc(self):
        logger.info('Getting last document with url %s.', self.entity)
        # print STORE_LATEST_VIEW_PARAMS
        # options = STORE_LATEST_VIEW_PARAMS.copy()
        # options['startkey'][1] = options['startkey'][1] % self.entity
        # options['endkey'][1] = options['endkey'][1] % self.entity
        params = {
            'group_level': 2,
            'startkey': ["page","%s" % self.entity,""],
            'endkey': ["page","%s" % self.entity,{}]
        }
        latest_view = self.db.view(STORE_LATEST_VIEW_NAME,
                                   **params)
                                #    **options)
                                #    options=STORE_LATEST_VIEW_OPTIONS %
                                #    (self.entity, self.entity))
            # options="""startkey=['page','%s','']&endkey=['page','%s',{}]&group_level=2""" % (self.entity, self.entity)
        # logger.debug('!!!!!!!!!!!!!!!!Latest docs %s.', latest_view)
        latest_docs = [r for r in latest_view]
        # FIXME
        # logger.debug('Latest docs %s.', latest_docs)
        if latest_docs:
            latest_doc = latest_docs[0]['value']
            logger.debug('Latest doc value %s', latest_doc)
            # FIXME: move outside
            latest_doc['context']['timestamp_measurement'] = \
                dtzutcstr2dtz(latest_doc['context']['timestamp_measurement'])
            # latest_doc['value']['header']['last_modified'] = \
            #     dtzutcstr2dtz(latest_doc['value']['header']['last_modified'])
            self.latest_page_doc = PageDoc(**latest_doc)
            logger.debug('page after PageDoc(**latest_doc) %s',
                         self.latest_page_doc)
        else:
            logger.error('Latest view not found.')

    def is_etag_different(self):
        logger.debug('Comparing etags.')
        if (self.etag_store == self.etag == '' and
            self.last_modified_store == self.last_modified == '') or \
           (self.etag_store != self.etag) or \
           (self.last_modified_store != self.last_modified):
            logger.info('Etag or/and last_modified headers are different.')
            return True
        logger.info('Etag and last_modified headers are equal.')
        return False

    def gen_doc_id(self):
        logger.debug('Generating document id.')
        doc_id_etag_part = gen_doc_id_etag_part(self.etag, self.last_modified)
        logger.debug('Document id etag part %s', doc_id_etag_part)
        doc_id = gen_doc_id(self.entity, self.agent_type, self.agent_ip,
                            doc_id_etag_part)
        self.doc_id = doc_id
        logger.debug('Document id is %s', self.doc_id)

    def gen_page(self,):
        logger.info('Generating new document.')
        self.context = PageContext(
            agent_ip=self.agent_ip,
            # timestamp_measurement=self.timestamp_measurement,
            agent_type=self.agent_type,
            page_type=self.page_type,
            xpath=self.xpath
        )
        # logger.debug('context %s', self.context.__dict__)
        self.header = Header(
            etag=self.etag,
            last_modified=self.last_modified
        )
        # logger.debug('header %s', self.header.__dict__)
        self.value = PageValue(
            header=self.header,
            # content=self.content,
            # sha256_html=self.sha256_html,
            # sha256_md=self.sha256_md,
        )
        # logger.debug('value %s', self.value.__dict__)
        self.page = PageDoc(
            # id=self.doc_id,
            entity=self.entity,
            attribute=self.attribute,
            value=self.value,
            context=self.context
        )
        logger.debug('Document content %s', self.page)

    def store_page(self):
        logger.info('Storing new document.')
        # self.page.store(self.db)
        body = self.page._data
        # body = self.page.unwrap()
        # body = self.page._to_json('value')
        self.db.update_doc(STORE_UPDATE_DOC_NAME, self.doc_id, **{'body': body})

    def fetch_page(self):
        logger.info('Requesting next agent.')
        get_request(self.next_agent_url)
