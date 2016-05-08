# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PageWatcherScraperItem(scrapy.Item):
    # define the fields for your item here like:
    content = scrapy.Field()
    # FIXME: store in the item the metadata?
    # url = scrapy.Field()
    # file_name = scrapy.Field()
    # organization = scrapy.Field()
    # tool = scrapy.Field()
    # policy_type = scrapy.Field()
    # date_search = scrapy.Field()
