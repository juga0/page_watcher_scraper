# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.project import get_project_settings
import os.path

from page_watcher_scraper.items import PageWatcherScraperItem
from page_watcher_scraper.util import save_html, append, now_timestamp, \
    url2filename


settings = get_project_settings()


class PageWatcherSpider(scrapy.Spider):
    handle_httpstatus_list = [403,  404,  503,  502]
    fail_url_path = settings.get('LOG_FAIL_URL_FULLPATH')

    name = "policies"
    # FIXME: created allowed_domains from parsing the url?

    def handle_response(self,  response):
        self.logger.debug('in handle response')
        # FIXME: move to a function in util?
        if not os.path.isdir(settings.get('LOG_PATH')):
            os.makedirs(settings.get('LOG_PATH'))
        if response.status == 200:
            append(settings.get('LOG_OK_URL_FULLPATH'), response.url)
            self.logger.debug('wroten log ok %s' %
                              settings.get('LOG_OK_URL_FULLPATH'))
        else:
            self.logger.debug('error http code: %s',  response.status)
            append(settings.get('LOG_FAIL_URL_FULLPATH'),
                   str(response.status) + ': ' + response.url)

    def __init__(self, policies_path="", url="", xpath="",  *args, **kwargs):
        super(PageWatcherSpider, self).__init__(*args, **kwargs)
        self.logger.debug('in init')
        self.policies_path = policies_path
        self.url = url
        self.xpath = xpath
        self.logger.debug('polices path: %s' % self.policies_path)
        # TODO: add arguments that can be passed by command line
        # FIXME: make this spider to iterate over all urls or leave it in
        #        the external script?

    def start_requests(self):
        yield self.make_requests_from_url(self.url)

    def parse(self, response):
        content = None
        self.handle_response(response)
        if response.xpath(self.xpath).extract():
            content = response.xpath(self.xpath).extract()[0]
        item = PageWatcherScraperItem()
        # FIXME: convert html to markdown here or in the pipeline?
        # FIXME: do something when no content
        item['content'] = content
        # FIXME: store in the item the metadata?
        # the name of the html file is created from these args
        args = {
            'name': self.name,
            'item': url2filename(response.url),
            'time': now_timestamp()
        }
        save_html(response.body, args)
        # TODO: append metadata in other file
        return item
