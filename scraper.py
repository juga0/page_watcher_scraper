#!/usr/bin/env python
# -*- coding: utf-8 -*-

# FIXME: move this file outside scrapy project?
from page_watcher import read_yaml, commit, create_policy_file_path, \
    CONFIG_PATH, RULES_PATH, DATA_REPO_PATH

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def main():

    repos = read_yaml(CONFIG_PATH)
    # FIXME: obtain last commit?

    rules = read_yaml(RULES_PATH)
    # FIXME: obtain last commit?

    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())

    for rule in rules:
        policies_path = create_policy_file_path(rule)
        process.crawl(
            'policies', policies_path=policies_path, url=rule['url'],
            xpath=rule['xpath'])
    logger.debug('starting crawler')
    # the script will block here until the crawling is finished
    process.start()
    process.stop()

    for repo in repos:
        commit(DATA_REPO_PATH, repo['url'], repo['name'])

if __name__ == "__main__":
    main()
