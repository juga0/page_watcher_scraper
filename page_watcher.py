# -*- coding: utf-8 -*-

# FIXME: move this file outside scrapy project?
from git import Repo, InvalidGitRepositoryError, GitCmdObjectDB, \
    GitCommandError, Git
from os import environ, makedirs, chmod
from os.path import join, isdir, isfile, abspath, dirname
import sys
from shutil import rmtree
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


def obtain_yaml(repo_path, file_path, repo_url, repo_branch, repo_name='origin', git_ssh_command=None):
    # FIXME: pull repo
    yaml_data = None

    if isdir(repo_path):
        logger.debug('found dir %s' % repo_path)
        try:
            repo = Repo(repo_path, odbt=GitCmdObjectDB)
            logger.debug('dir is a repo')
            origin = repo.remotes[repo_name]
        # dir exist but is not a repo
        except InvalidGitRepositoryError, e:
            # FIXME: rm the dir and clone the repo
            logger.exception(e)
            # rmdir and clone repo
            rmtree(repo_path)
            try:
                repo, origin = clone_repo(repo_url, repo_path, repo_branch,
                    repo_name, git_ssh_command)
            except GitCommandError, e:
                # FIXME
                logger.exception(e)
                logger.debug('cant obtain yaml')
                sys.exit()
        else:
            pull_repo(origin, repo_branch, git_ssh_command)
    else:
        try:
            repo, origin = clone_repo(repo_url, repo_path, repo_branch,
                repo_name, git_ssh_command)
        except GitCommandError, e:
            # FIXME
            logger.exception(e)
            logger.debug('cant obtain repo')
            sys.exit()
    try:
        yaml_data = read_yaml(file_path)
    except IOError, e:
        logger.exception(e)
        logger.debug('cant obtain yaml file')
        sys.exit()
    return yaml_data


def obtain_repo(repo_path, repo_url, repo_name, repo_branch, git_ssh_command=None):
    repo = None
    logger.debug("OBTAINING REPO")
    if isdir(repo_path):
        logger.debug('found dir %s' % repo_path)
        try:
            repo = Repo(repo_path, odbt=GitCmdObjectDB)
            logger.debug('dir is a repo')
            origin = repo.remotes[repo_name]
        # dir exist but is not a repo
        except InvalidGitRepositoryError, e:
            # FIXME: rm the dir and clone the repo
            logger.exception(e)
            # rmdir and clone repo
            rmtree(repo_path)
            try:
                repo, origin = clone_repo(repo_url, repo_path, repo_branch,
                    repo_name, git_ssh_command)
            except GitCommandError, e:
                # FIXME
                repo, origin = create_repo(repo_path, repo_name, repo_url)
        pull_repo(origin, repo_branch, git_ssh_command)
        # FIXME: pull fail?
        return repo
    else:
        try:
            repo, origin = clone_repo(repo_url, repo_path, repo_branch,
                repo_name, git_ssh_command)
        except GitCommandError, e:
            # FIXME
            repo, origin = create_repo(repo_path, repo_name, repo_url)
        return repo


def pull_repo(origin_repo, repo_branch, git_ssh_command=None):
    logger.debug("PULLING")
    try:
        if git_ssh_command:
            logger.debug('pulling with git_ssh_command %s' % git_ssh_command)
            with origin_repo.repo.git.custom_environment(GIT_SSH=git_ssh_command):
                origin_repo.pull(repo_branch)
        else:
            logger.debug('pulling without git_ssh_command')
            origin_repo.pull(repo_branch)
    except GitCommandError, e:
        # FIXME
        logger.exception(e)
        raise e


def clone_repo(repo_url, repo_path, repo_branch, repo_name, git_ssh_command=None):
    logger.debug("CLONING")
    try:
        if git_ssh_command:
            repo = Repo.clone_from(repo_url, repo_path, branch=repo_branch, env={'GIT_SSH':git_ssh_command})
        else:
            repo = Repo.clone_from(repo_url, repo_path, branch=repo_branch)
        origin = repo.remotes['origin']
        origin.rename(repo_name)
        return repo, origin
    except GitCommandError, e:
        # FIXME
        logger.exception(e)
        raise e


def create_repo(repo_path, repo_name, repo_url):
    # create dir
    logger.debug("CREATING REPO")
    repo = Repo.init(repo_path)
    origin = repo.create_remote(repo_name, repo_url)
    return repo, origin


def commit_push(repo, repo_author, repo_email, git_ssh_command,
                repo_branch):
    logger.debug("COMMITING AND PUSHING")
    repo.index.add('*')
    logger.debug('added files to repo')
    commit_msg = "Crawl completed at " + time.strftime("%Y-%m-%d-%H-%M-%S")
    environ["GIT_AUTHOR_NAME"] = repo_author
    environ["GIT_AUTHOR_EMAIL"] = repo_email
    committed = repo.index.commit(commit_msg)
    logger.debug('commited policy data')
    logger.debug(committed)
    # FIXME: there could be more than 1 origin
    origin = repo.remotes[0]
    # origin = repo.remotes[repo_name]
    logger.debug('pushing with git_ssh_command %s' % git_ssh_command)
    with repo.git.custom_environment(GIT_SSH=git_ssh_command):
        origin.push(repo_branch)


def create_data_file_path(rule, data_path):
    data_dir_path = join(data_path,
                         rule.get('organization'),
                         rule.get('tool'))
    if not isdir(data_dir_path):
        makedirs(data_dir_path)
    data_file_path = join(data_dir_path, rule.get('policy') + '.txt')
    return data_file_path


def write_ssh_keys(ssh_dir, ssh_priv_key_env, ssh_pub_key_env, ssh_priv_key_path,
                   ssh_pub_key_path):
    ssh_pub_key = environ[ssh_pub_key_env]
    ssh_priv_key = environ[ssh_priv_key_env]
    logger.debug('ssh_dir %s' % ssh_dir)
    if not isdir(ssh_dir):
        makedirs(ssh_dir)
        logger.debug('created dir %s' % ssh_dir)
    if not isfile(ssh_pub_key_path):
        with open(ssh_pub_key_path, 'wb') as f:
            f.write(ssh_pub_key)
        logger.debug('wroten %s' % ssh_pub_key_path)
    if not isfile(ssh_priv_key_path):
        with open(ssh_priv_key_path, 'wb') as f:
            f.write(ssh_priv_key)
        logger.debug('wroten %s' % ssh_priv_key_path)
        chmod(ssh_priv_key_path, 0600)