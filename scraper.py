#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from page_watcher import commit_push_if_changes, create_data_file_path, \
    obtain_yaml, pull_or_clone, write_ssh_keys, write_ssh_command, \
    write_ssh_key_server, check_ssh_keys, ismorpio
from config import CONFIG_PATH, RULES_PATH, DATA_REPO_PATH, CONFIG_REPO_PATH, \
    CONFIG_REPO_URL, CONFIG_REPO_BRANCH, RULES_REPO_PATH, RULES_REPO_URL, \
    RULES_REPO_BRANCH, DATA_REPO_BRANCH, GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL, \
    METADATA_PATH
from config import MORPH_SSH_PRIV_KEY_ENV, MORPH_SSH_PUB_KEY_ENV, \
    SSH_PRIV_KEY_PATH, SSH_PUB_KEY_PATH, GIT_SSH_COMMAND, SSH_DIR, \
    GIT_SSH_COMMAND_PATH, SSH_PUB_KEY_SERVER_PATH, GITHUB_SSH_PUB_KEY, \
    GIT_SSH_COMMAND_MORPHIO
try:
    from config_local import GIT_SSH_COMMAND
except:
    print 'no local git command'


import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def main():

    repos = []
    repos_conf = obtain_yaml(CONFIG_REPO_PATH, CONFIG_REPO_URL,
                             CONFIG_REPO_BRANCH, CONFIG_PATH)

    rules = obtain_yaml(RULES_REPO_PATH, RULES_REPO_URL,
                        RULES_REPO_BRANCH)

    write_ssh_keys(SSH_DIR, MORPH_SSH_PRIV_KEY_ENV, MORPH_SSH_PUB_KEY_ENV,
                   SSH_PRIV_KEY_PATH, SSH_PUB_KEY_PATH)

    if ismorpio():
        write_ssh_command(GIT_SSH_COMMAND_PATH, GIT_SSH_COMMAND_MORPHIO)
    else:
        write_ssh_command(GIT_SSH_COMMAND_PATH, GIT_SSH_COMMAND)

    write_ssh_key_server(GITHUB_SSH_PUB_KEY, SSH_PUB_KEY_SERVER_PATH)

    for repo_conf in repos_conf:
        logger.debug('repo name %s' % repo_conf.get('name'))
        repo = pull_or_clone(DATA_REPO_PATH, repo_conf.get('url'),
                             DATA_REPO_BRANCH, repo_conf.get('name'),
                             GIT_SSH_COMMAND_PATH, False)
        repos.append(repo)

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
        commit_push_if_changes(repo, GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL,
                               GIT_SSH_COMMAND_PATH, DATA_REPO_BRANCH,
                               METADATA_PATH)

    # logger.debug('CHECKING SSH KEYS')
    # logger.debug('===================')
    # for repo in repos:
    #     check_ssh_keys(repo, GIT_SSH_COMMAND_PATH, SSH_PRIV_KEY_PATH,
    #                SSH_PUB_KEY_PATH, SSH_PUB_KEY_SERVER_PATH)

    sys.exit()

if __name__ == "__main__":
    main()
