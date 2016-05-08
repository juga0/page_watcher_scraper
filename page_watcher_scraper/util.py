# -*- coding: utf-8 -*-

import os.path
from scrapy.utils.project import get_project_settings
from datetime import datetime
import html2text
import logging
# needed?
import lxml.html
import lxml.etree


utf8_parser = lxml.etree.XMLParser(encoding='utf-8')
settings = get_project_settings()
logger = logging.getLogger(__name__)


def now_timestamp():
    return datetime.utcnow().replace(microsecond=0).isoformat()\
        .replace(':', '-')


def url2filename(text):
    return text.replace(' ', '_').replace('https://', '')\
        .replace('http://', '').replace('/', '_')


def append(file, string):
    file = open(file, 'a')
    file.write(string + "\n")
    file.close()


def save_html(body, args):
    logger.debug(args)
    html_path = (settings.get('HTML_PATH') % args)[:255]
    if not os.path.isdir(settings.get('HTML_PATH')):
        os.makedirs(settings.get('HTML_PATH'))
    with open(html_path,  'w') as f:
        f.write(body)
    logger.debug('saving html %s' % html_path)


def html2md(text):
    h = html2text.HTML2Text()
    h.mark_code = True
    if isinstance(text, unicode):
        return h.handle(text).encode("UTF-8")
    # FIXME: convert to unicode in case it isn't?


# needed?
def parse_from_unicode(unicode_str):
    # FIXME: not needed?
    if isinstance(unicode_str, unicode):
        s = unicode_str.encode('utf-8')
        return lxml.etree.fromstring(s, parser=utf8_parser)
