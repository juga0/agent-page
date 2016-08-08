""""""
import logging
from couchdb import Server

from settings import STORE_URL, STORE_CONFIG_DB, STORE_CONFIG_DOC, STORE_DB, \
    LOGGING, LOG_LEVEL, STORE_LATEST_VIEW_URL
from models import PagesConfig, WatchAgent, PageDoc, map_fun, reduce_fun

# logging.config.dictConfig(LOGGING)
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

pages_config = PagesConfig(STORE_URL, STORE_CONFIG_DB, STORE_CONFIG_DOC)

watch_agent = WatchAgent(STORE_URL, STORE_DB, STORE_CONFIG_DB, STORE_CONFIG_DOC)

server = Server(STORE_URL)
db = server[STORE_DB]
doc_id = 'analyse-197.231.221.211-httpsguardianproject.infohomedata-usage-and-protection-policies-d0f97c1818a390713648278b91d5aaa6a0d7e64f87aa8ad2e764e60b49b8e070'
page = PageDoc.load(db, doc_id)
etag = page.value.header.etag
logging.debug(etag)

page = PageDoc()
page.load(db, doc_id)
etag = page.value.header.etag
logging.debug(etag)

map_fun2 = '''function(doc) {
        if (doc.type == 'Page')
            emit(doc.name, null);
    }'''
rows = db.query(map_fun2, descending=True)
print rows

rows = db.query(map_fun, reduce_fun, descending=True)
print rows

pagedoc = PageDoc()

for row in db.view('_all_docs'):
    print(row.id)

uname_list = db.view('page/latest', reduce=True, group_level=2)

uname_list = db.view('page/latest', group=True, startkey=["page",doc_id])
for r in uname_list:
    print r.value

uname_list = db.view('page/latest', group=True, startkey=["page","%s" % doc_id])


uname_list = db.view('page/latest', reduce=True, group_level=2, descending=True, startkey=["page","%s",{}], endkey=["page","%s"]
uname_list = db.view('page/latest', reduce=True, group_level=2, descending=True, startkey=["page", doc_id, {}], endkey=["page", doc_id])
uname_list = db.view('page/latest', reduce=True, group_level=2, descending=True, startkey=["page","%s" % doc_id, {}], endkey=["page","%s" % doc_id])


[%22page%22,%22http%3A%2F%2Fwww.t-mobile.com%2FTemplates%2FPopup.aspx%3FPAsset%3DFtr_Ftr_TermsAndConditions%26amp%3Bprint%3Dtrue%22,{}]&endkey=[%22page%22,%22http%3A%2F%2Fwww.t-mobile.com%2FTemplates%2FPopup.aspx%3FPAsset%3DFtr_Ftr_TermsAndConditions%26amp%3Bprint%3Dtrue%22]

https://staging-store.openintegrity.org/pages-juga/_design/page/_view/latest?group=true&group_level=2&descending=true&startkey=[%22page%22,%22http%3A%2F%2Fwww.t-mobile.com%2FTemplates%2FPopup.aspx%3FPAsset%3DFtr_Ftr_TermsAndConditions%26amp%3Bprint%3Dtrue%22,{}]&endkey=[%22page%22,%22http%3A%2F%2Fwww.t-mobile.com%2FTemplates%2FPopup.aspx%3FPAsset%3DFtr_Ftr_TermsAndConditions%26amp%3Bprint%3Dtrue%22]

uname_list = db.view('page/latest', reduce=True, group=True, group_level=2, descending=True, startkey=["page","http%3A%2F%2Fwww.t-mobile.com%2FTemplates%2FPopup.aspx%3FPAsset%3DFtr_Ftr_TermsAndConditions%26amp%3Bprint%3Dtrue",{}], endkey=["page","http%3A%2F%2Fwww.t-mobile.com%2FTemplates%2FPopup.aspx%3FPAsset%3DFtr_Ftr_TermsAndConditions%26amp%3Bprint%3Dtrue"])
