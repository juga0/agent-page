
#######
# watch
#######

import logging

logger = logging.getLogger(__name__)


# datetime
##########
def now_utc_dtz():
    from datetime import datetime
    from pytz import utc
    return utc.localize(datetime.utcnow())


def nowdt2iso8601str():
    """
    # assuming that utcnow returns the correct local time converted to UTC:
    >> datetime.utcnow().isoformat()
    '2016-07-30T13:36:06.305653'
    # for python timezone aware objects:
    >> datetime.now(tz=pytz.utc).isoformat()
    '2016-07-30T13:37:23.748609+00:00'
    Both 'Z' and '+00:00' are compatible with iso format
    """
    # return now_utc_dtz().isoformat() + 'Z'
    import datetime
    return datetime.strftime(now_utc_dtz(), '%Y-%m-%dT%H:%M:%S.%fZ')


def dtzutcstr2dtz(dtzutcstr):
    from datetime import datetime
    from pytz import utc
    try:
        dtutc = datetime.strptime(dtzutcstr, '%Y-%m-%dT%H:%M:%S.%fZ')
        dtzutc = utc.localize(dtutc)
    except ValueError as e:
        logger.debug('The datetime string did not contain a valid datetime')
        dtzutc = None
    logger.debug('Datetime object %s', dtzutc)
    return dtzutc


def dtz2dtzstr(dtz):
    from datetime import datetime
    return datetime.strftime(dtz, '%Y-%m-%dT%H:%M:%S.%fZ')

def dtz_local2dtz_utc(dtz):
    from pytz import utc
    dtzutc = dtz.astimezone(utc)
    logger.debug('Datetime in UTC %s.', dtzutc)
    return dtzutc


def last_modified2dtz(last_modified):
    """
    >>> last_modified = u'Mon, 01 Sep 1997 01:03:33 GMT'
    >>> dt = datetime.strptime(last_modified, '%a, %d %b %Y %H:%M:%S %Z')
    >>> dt.replace(tzinfo=timezone(last_modified.split()[-1:][0]))
    datetime.datetime(1997, 9, 1, 1, 3, 33, tzinfo=<StaticTzInfo 'GMT'>)
    """
    from datetime import datetime
    from pytz import timezone
    dt = datetime.strptime(last_modified, '%a, %d %b %Y %H:%M:%S %Z')
    logger.debug('Datetime without timezone %s.', dt)
    tz = timezone(last_modified.split()[-1:][0])
    logger.debug('Timezone %s.', tz)
    # wrong way?
    # dtz = dt.replace(tzinfo=tz)
    # right way?
    dtz = tz.localize(dt)
    logger.debug('Datetime with timezone %s.', dtz)
    if tz != timezone('UTC'):
        dtz = dtz_local2dtz_utc(dtz)
    return dtz


def dtz_str2dtz_str_docid(dtz_str):
    """
    Returns the current last_modified header of a Web page
    (Mon, 13 Jun 2016 19:01:36 GMT) in ISO 8601 (yyyy-MM-ddTHH:mm:ssZ) date
    time without dashes (yyyyMMddTHHmmssZ).
    >>> last_modified = 'Mon, 13 Jun 2016 19:01:36 GMT'
    >>> dtz_str2dtz_str_docid(last_modified)
    '20160613T190136Z'
    Also:
    iso8601.parse_date(datetime.datetime.now(tz=pytz.utc).isoformat())
    """
    # dt = last_modified2dtz(last_modified)
    # timestamp_str = dt.isoformat().replace(':', '').replace('-', '') + 'Z'
    timestamp_str = dtz_str.replace(':', '').replace('-', '').replace('.', '')
    logger.debug('Last-modified document id part: %s', timestamp_str)
    return timestamp_str

# file system names
####################


def filename_allowed_chars(filename):
    import string
    import unicodedata
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    valid_filename = unicodedata.normalize('NFKD', filename)\
        .encode('ASCII', 'ignore')
    new_filename = "".join(c for c in valid_filename if c in valid_chars)
    logger.debug('File name: %s', new_filename)
    return new_filename


def url2filenamedashes(url):
    """
    Convert a url (https://staging-store.openintegrity.org/url) into a POSIX
    file name ()

    >>> url = 'https://staging-store.openintegrity.org/url'
    >>> url.replace(' ', '_').replace('://', '-').replace('/', '-')
    'https-staging-store.openintegrity.org-url'
    """
    return filename_allowed_chars(unicode(url))


# system
#########


def obtain_public_ip():
    """Return the public IP where the program is running."""
    from urllib2 import urlopen
    my_ip = urlopen('http://ip.42.pl/raw').read()
    logger.debug('The public ip is: %s' % my_ip)
    return str(my_ip)


# data structures
#################


def get_value_from_key_index(dict_or_list, keys_indexes):
    """"""
    if not isinstance(keys_indexes, list):
        keys_indexes = [keys_indexes]
    for k in keys_indexes:
        logger.debug('key or index is %s', k)
        try:
            dict_or_list = dict_or_list[k]
        except (KeyError, IndexError) as e:
            logger.error(e)
            return None
    return dict_or_list


# docment id
############


def gen_doc_id_etag_part(etag=None, last_modified=None):
    if etag:
        tag = etag
    elif last_modified:
        tag = dtz_str2dtz_str_docid(last_modified)
    else:
        tag = ''
    logger.debug('Document id etag part: %s', tag)
    return tag


def gen_doc_id(url, agent_type, public_ip, doc_id_etag_part=''):
    """
    Return and string like:
    analyse-url-192.168.1.1-https-www.whispersystems.org-signal-privacy-20160613T190136Z.
    """
    urlfilename = url2filenamedashes(url)
    doc_id = '-'.join([agent_type, public_ip, urlfilename, doc_id_etag_part])
    logger.debug('Document id: %s', doc_id)
    return doc_id


# html_utils
#############

def html2md(text, encoding='utf-8'):
    import html2text
    logger.debug('converting to markdown')
    logger.debug('type text %s', type(text))
    h = html2text.HTML2Text()
    h.mark_code = True
    if isinstance(text, unicode):
        return h.handle(text).encode(encoding)
    return h.handle(text)


def generate_sha256(text, encoding='utf-8'):
    import hashlib
    logger.debug('Calculating sha256.')
    logger.debug('Type text %s', type(text))
    if isinstance(text, unicode):
        text = text.encode(encoding)
    sha = hashlib.sha256(text)
    sha_hex = sha.hexdigest()
    logger.debug('sha256 is %s', sha_hex)
    return sha_hex


# document
##########


# def generate_page_data(url, agent_type, page_type, etag='', last_modified='',
#                        xpath='', content='', attribute=''):
#     data = {
#         'entity': url,
#         'attribute': attribute,
#         'value': {
#             'header': {
#                 'etag': etag,
#                 'last_modified': last_modified
#                 }
#             },
#         "context": {
#             'agent_ip':  obtain_public_ip(),
#             'agent_type': agent_type,
#             'page_type': page_type,
#             'timestamp_measurement': nowdt2iso8601str(),
#             'xpath': xpath
#             }
#         }
#     data = AGENT_PAYLOAD % {
#         'entity': url,
#         'attribute': attribute,
#         'etag': etag,
#         'last_modified': last_modified,
#         'agent_ip':  obtain_public_ip(),
#         'agent_type': agent_type,
#         'page_type': page_type,
#         'timestamp_measurement': nowdt2iso8601str(),
#         'xpath': xpath
#     }
#     return data


# requests
###########


def get_etag(url):
    import requests
    r = requests.head(url)
    headers = r.headers
    # logger.debug('response headers %s', headers)
    etag = headers.get('ETag')
    logger.debug('Header response etag: %s', etag)
    last_modified = headers.get("Last-Modified")
    logger.debug('Header response last-modifed: %s', last_modified)
    if last_modified:
        last_modified = last_modified2dtz(last_modified)
        logger.debug('Header response last-modifed as dt: %s', last_modified)
        last_modified = dtz2dtzstr(last_modified)
        logger.debug('Header response last-modifed as str: %s', last_modified)
    if not etag:
        etag = ''
    if not last_modified:
        last_modified = ''
    if etag == last_modified == '':
        logger.debug('URL %s does not return etag nor last_modified', url)
    return etag, last_modified


def get_request(url, keys_indexes=None):
    """
    Request GET a URL. Result might be in json, it's possible to
    specify which keys in the json contain the data.
    """
    import requests
    from requests.exceptions import ConnectionError
    logger.debug('GET url %s', url)
    try:
        r = requests.get(url)
    except ConnectionError as e:
        logger.error(e)
        return None
    logger.info('Response to request GET %s is %s', (url, r))
    try:
        logger.debug('Response content is json.')
        data = r.json()
    except ValueError:
        logger.debug('Response content is not json')
        return r.text
    if keys_indexes:
        logger.debug('Obtaining %s in the response.', keys_indexes)
        data = get_value_from_key_index(data, keys_indexes)
        logger.debug('The value of the key is %s', data)
    return data


def post_store(url, data, only_status_code=False):
    """
    Request POST a URL
    """
    import requests
    from requests.exceptions import ConnectionError
    logger.debug('POST url %s' % url)
    if isinstance(data, dict):
        try:
            r = requests.post(url, json=data)
        except ConnectionError as e:
            logger.error(e)
            return None
    else:
        try:
            r = requests.post(url, data=data)
        except ConnectionError as e:
            logger.error(e)
            return None
    logger.info('Request POST %s returned %s', url, r)
    if only_status_code:
        return r.status_code
    return r


def get_request_etag(url, keys_indexes=['rows', 0, 'value', 'header', 'etag']):
    etag = last_modified = ''
    etag = get_request(url, keys_indexes)
    if etag is None:
        return None, None
    if etag == '':
        last_modified = get_request(url, ['rows', 0, 'value', 'header',
                                        'last_modified'])
    return etag, last_modified

######
# fetch
#######

# file system
###############


def file_exists(filepath):
    """
    """
    from os.path import isfile
    logger.debug('Checking whether %s is in the file system.', filepath)
    if isfile(filepath):
        logger.debug('The file exists.')
        return True
    return False


def write_file(filepath, content, encoding='utf-8'):
    """
    """
    from os.path import isdir, dirname
    from os import makedirs
    logger.debug('Writing content to file %s.', filepath)
    logger.debug('Content type %s.', type(content))
    if not isdir(dirname(filepath)):
        logger.debug('Creating dir %s', dirname(filepath))
        makedirs(dirname(filepath))
    with open(filepath, 'w') as f:
        f.write(content.encode(encoding))
    logger.debug('Written file %s', filepath)


#######
# analyse
##########


# def generate_page_data(dict_data, content, hash_md, agent_type):
#     """
#     {"attribute": "page/content", "context": {"xpath": "//div[@id='body']", "agent_type": "watch", "timestamp_measurement": "2016-08-05T13:21:40.396293Z", "page_type": "tos", "agent_ip": "65.181.112.128"}, "value": {"header": {"last-modified": "Mon, 01 Sep 1997 01:03:33 GMT", "etag": "None"}, "sha256_html": "43fa5a6f123a2cbb7a6c84b6ca9511b26ffef385121d026fdbab2202b7534e1f"}, "entity": "http://www.t-mobile.com/Templates/Popup.aspx?PAsset=Ftr_Ftr_TermsAndConditions&amp;print=true"}
#      {
#          "entity": "%(entity)",
#          "attribute": "page/content",
#          "value": {
#              "header": {
#                  "etag": "%(etag)",
#                  "last-modified": "%(last_modified)"
#              },
#              "content": "%(content)",
#              "sha256_html": "%(sha256_html)",
#              "sha256_md": "%(sha256_md)"
#          },
#          "context": {
#              "timestamp_measurement": "%(timestamp_measurement)",
#              "agent_type": "%(agent_type)",
#              "agent_ip": "%(agent_ip)",
#              "page_type": "%(page_type)",
#              "xpath": "%(xpath)"
#          }
#      }
#     """
#     logger.debug('Generating payload.')
#     dict_data['value']['sha256_md'] = hash_md
#     dict_data['value']['content'] = content
#     dict_data['context']['agent_type'] = agent_type
#     dict_data['context']['timestamp_measurement'] = nowdt2iso8601str()
#     dict_data['context']['agent_ip'] = obtain_public_ip()
#     return dict_data


def read_file(filepath, encoding='utf-8'):
    """
    """
    from os.path import isfile
    import codecs
    logger.debug('Checking whether %s is in the file system.', filepath)
    if isfile(filepath):
        logger.info('The file exists.')
        with codecs.open(filepath, "r", encoding) as f:
            content = f.read()
        return content
    return ''


def get_request_sha256_html(url, keys_indexes=['rows', 0, 'value', 'sha256_html']):
    sha256 = ''
    logger.debug('Checking if sha256_html is in the store for the url %s .',
                 url)
    sha256 = get_request(url, key_indexes)
    return sha256


def get_request_sha256_md(url):
    sha256 = ''
    logger.debug('Checking if sha256_html is in the store for the url %s .',
                 url)
    sha256 = get_request(url, key_indexes)
    return sha256


def scraper_content(xpath, content):
    logger.debug('content type %s', type(content))
    from lxml import html, etree
    tree = html.fromstring(content)
    e = tree.xpath(xpath)
    html_text = etree.tostring(e[0])
    logger.debug('Content type after xpath %s', type(html_text))
    return html_text
