# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os.path
from scrapy.utils.project import get_project_settings
import logging

from page_watcher_scraper.util import html2md


settings = get_project_settings()
logger = logging.getLogger(__name__)


class PageWatcherScraperPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        logger.debug('crawler dir')
        logger.debug(dir(crawler))
        if crawler.spider:
            policies_path = crawler.spider.policies_path
            return cls(policies_path)
        return cls(
            policies_path=crawler.settings.get('DATA_REPO_PATH')
        )

    def __init__(self, policies_path):
        if not os.path.isdir(os.path.dirname(policies_path)):
            os.makedirs(os.path.dirname(policies_path))
        logger.debug('')
        self.policies_path = policies_path

    def open_spider(self, spider):
        logger.debug('opening policy file')
        self.policies = open(self.policies_path, 'w')

    def process_item(self, item, spider):
        # FIXME: log when not content or several
        if item.get('content'):
            md = html2md(item['content'])
            logger.debug('writing policy to file %s' % self.policies_path)
            try:
                self.policies.write(md)
                # logger.debug('wrote content %s' % md)
            except UnicodeEncodeError, e:
                logger.exception(e)
                logger.debug('content not wroten')
            # FIXME: append metadata in other file
        return item

    def close_spider(self, spider):
        logger.debug('closing policy file')
        self.policies.close()
