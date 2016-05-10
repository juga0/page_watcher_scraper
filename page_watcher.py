# -*- coding: utf-8 -*-

# FIXME: move this file outside scrapy project?
from git import Repo, InvalidGitRepositoryError, GitCmdObjectDB
from os import environ, makedirs
from os.path import join, isdir, isfile
import sys
import yaml
import time
import logging

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)


def read_yaml(file_path):
    try:
        with open(file_path) as f:
            yaml_data = yaml.safe_load(f)
        logger.debug('yaml data: ')
        logger.debug(yaml_data)
        return yaml_data
    except IOError, e:
        logger.exception(e)
        raise IOError


def obtain_yaml(repo_path, file_path, repo_url, repo_branch):
    # FIXME: pull repo
    yaml_data = None
    try:
        yaml_data = read_yaml(file_path)
    except IOError, e:
        try:
            Repo.clone_from(repo_url,
                            repo_path, branch=repo_branch)
            try:
                yaml_data = read_yaml(file_path)
            except IOError, e:
                pass
        except GitCommandError, e:
            logger.exception(e)
    except:
        logger.info('Cant find configuration')
        sys.exit()
    return yaml_data


def commit_push(repo_path, repo_url, repo_name, repo_branch, repo_author,
                repo_email):
    try:
        repo = Repo(repo_path, odbt=GitCmdObjectDB)
        #repo.index.add(crawl_paths)
    except InvalidGitRepositoryError:
        #FIXME: try clone first
        repo = Repo.init(repo_path)
    try:
        origin = repo.remotes[repo_name]
    except IndexError:
        origin = repo.create_remote(repo_name, repo_url)

    logger.debug('repo working dir %s' % repo.working_dir)

    #with repo.git.custom_environment(GIT_SSH=GIT_SSH_COMMAND):
    origin.pull(repo_branch)

    repo.index.add('*')
    logger.debug('added files to repo')
    commit_msg = "Crawl completed at " + time.strftime("%Y-%m-%d-%H-%M-%S")
    environ["GIT_AUTHOR_NAME"] = repo_author
    environ["GIT_AUTHOR_EMAIL"] = repo_email
    committed = repo.index.commit(commit_msg)
    logger.debug('commited policy data')
    logger.debug(committed)

    #with repo.git.custom_environment(GIT_SSH=GIT_SSH_COMMAND):
    origin.push(repo_branch)


def create_data_file_path(rule, data_path):
    data_dir_path = join(data_path,
                         rule.get('organization'),
                         rule.get('tool'))
    if not isdir(data_dir_path):
        makedirs(data_dir_path)
    data_file_path = join(data_dir_path, rule.get('policy') + '.txt')
    return data_file_path
