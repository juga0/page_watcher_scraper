#!/usr/bin/env python
# -*- coding: utf-8 -*-

# FIXME: move this file outside scrapy project?
import sys
from page_watcher import commit_push, create_data_file_path, obtain_yaml
from config import CONFIG_PATH, RULES_PATH, DATA_REPO_PATH, CONFIG_REPO_PATH, \
    CONFIG_REPO_URL, CONFIG_REPO_BRANCH, RULES_REPO_PATH, RULES_REPO_URL, \
    RULES_REPO_BRANCH, DATA_REPO_BRANCH, GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def main():

    repos = obtain_yaml(CONFIG_REPO_PATH,
                        CONFIG_PATH, CONFIG_REPO_URL, CONFIG_REPO_BRANCH)

    rules = obtain_yaml(RULES_REPO_PATH,
                        RULES_PATH, RULES_REPO_URL, RULES_REPO_BRANCH)

    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())

    for rule in rules:
        policies_path = create_data_file_path(rule, DATA_REPO_PATH)
        process.crawl(
            'policies', policies_path=policies_path, url=rule['url'],
            xpath=rule['xpath'])
    logger.debug('starting crawler')
    # the script will block here until the crawling is finished
    process.start()
    process.stop()

    for repo in repos:
        commit_push(DATA_REPO_PATH, repo.get('url'), repo.get('name'),
                    DATA_REPO_BRANCH, GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL)
    sys.exit()

if __name__ == "__main__":
    main()
