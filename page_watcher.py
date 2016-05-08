# -*- coding: utf-8 -*-

# FIXME: move this file outside scrapy project?
from git import Repo, InvalidGitRepositoryError, GitCmdObjectDB
from os import environ, makedirs
from os.path import dirname, abspath, join, isdir
import yaml
import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

CONFIG_REPO_BRANCH = 'master'
RULES_REPO_BRANCH = 'master'
GIT_AUTHOR_NAME = "OII Policies Agent"
GIT_AUTHOR_EMAIL = "oii-agents@iilab.org"

BASE_PATH = dirname(dirname(abspath(__file__)))
ROOT_PATH = dirname(BASE_PATH)
CONFIG_REPO = 'page-watcher-config'
RULES_REPO = 'page-watcher-rules'
DATA_REPO = 'page-watcher-data'
CONFIG_REPO_PATH = join(ROOT_PATH, CONFIG_REPO)
RULES_REPO_PATH = join(ROOT_PATH, RULES_REPO)
DATA_REPO_PATH = join(ROOT_PATH, DATA_REPO)
CONFIG_FILENAME = 'config.yml'
RULES_FILENAME = 'rules.yml'
CONFIG_PATH = join(ROOT_PATH, CONFIG_REPO, CONFIG_FILENAME)
RULES_PATH = join(ROOT_PATH, RULES_REPO, RULES_FILENAME)


def read_yaml(file_path):
    with open(file_path) as f:
        yaml_data = yaml.safe_load(f)
    logger.debug('yaml data: ')
    logger.debug(yaml_data)
    return yaml_data


def commit(repo_path, remote_repo_url, remote_repo_name):
    try:
        repo = Repo(repo_path, odbt=GitCmdObjectDB)
        #repo.index.add(crawl_paths)
    except InvalidGitRepositoryError:
        #FIXME: try clone first
        repo = Repo.init(repo_path)
    try:
        origin = repo.remotes[remote_repo_name]
    except IndexError:
        origin = repo.create_remote(remote_repo_name, remote_repo_url)

    logger.debug('repo working dir %s' % repo.working_dir)

    #with repo.git.custom_environment(GIT_SSH=GIT_SSH_COMMAND):
    origin.pull(RULES_REPO_BRANCH)

    repo.index.add('*')
    logger.debug('added files to repo')
    commit_msg = "Crawl completed at " + time.strftime("%Y-%m-%d-%H-%M-%S")
    environ["GIT_AUTHOR_NAME"] = GIT_AUTHOR_NAME
    environ["GIT_AUTHOR_EMAIL"] = GIT_AUTHOR_EMAIL
    committed = repo.index.commit(commit_msg)
    logger.debug('commited policy data')
    logger.debug(committed)

    #with repo.git.custom_environment(GIT_SSH=GIT_SSH_COMMAND):
    origin.push(RULES_REPO_BRANCH)


def create_policy_file_path(rule):
    policy_dir_path = join(DATA_REPO_PATH,
                           rule['organization'],
                           rule['tool'])
    if not isdir(policy_dir_path):
        makedirs(policy_dir_path)
    create_policy_file_path = join(policy_dir_path, rule['policy'] + '.txt')
    return create_policy_file_path
