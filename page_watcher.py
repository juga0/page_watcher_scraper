# -*- coding: utf-8 -*-

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


def obtain_yaml(repo_path, file_path, repo_url, repo_branch,
                repo_name='origin', git_ssh_command_path=None):
    yaml_data = None

    if isdir(repo_path):
        logger.debug('found dir %s' % repo_path)
        try:
            repo = Repo(repo_path, odbt=GitCmdObjectDB)
            logger.debug('dir is a repo')
            origin = repo.remotes[repo_name]
        # dir exist but is not a repo
        except InvalidGitRepositoryError, e:
            logger.exception(e)
            rmtree(repo_path)
            try:
                repo, origin = clone_repo(repo_url, repo_path, repo_branch,
                                          repo_name, git_ssh_command_path)
            except GitCommandError, e:
                # FIXME: handle in a better way exception
                logger.exception(e)
                logger.debug('cant obtain yaml')
                sys.exit()
        else:
            pull_repo(origin, repo_branch, git_ssh_command_path)
    else:
        try:
            repo, origin = clone_repo(repo_url, repo_path, repo_branch,
                                      repo_name, git_ssh_command_path)
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


def obtain_repo(repo_path, repo_url, repo_name, repo_branch,
                git_ssh_command_path=None):
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
            logger.exception(e)
            rmtree(repo_path)
            try:
                repo, origin = clone_repo(repo_url, repo_path, repo_branch,
                                          repo_name, git_ssh_command_path)
            except GitCommandError, e:
                # FIXME: handle better exception
                repo, origin = create_repo(repo_path, repo_name, repo_url)
        pull_repo(origin, repo_branch, git_ssh_command_path)
        # FIXME: pull fail?
        return repo
    else:
        try:
            repo, origin = clone_repo(repo_url, repo_path, repo_branch,
                                      repo_name, git_ssh_command_path)
        except GitCommandError, e:
            # FIXME: handle better exception
            repo, origin = create_repo(repo_path, repo_name, repo_url)
        return repo


def pull_repo(origin_repo, repo_branch, git_ssh_command_path=None):
    logger.debug("PULLING")
    try:
        if git_ssh_command_path:
            logger.debug('pulling with git_ssh_command_path %s' %
                         git_ssh_command_path)
            with origin_repo.repo.git.custom_environment(
                    GIT_SSH=git_ssh_command_path):
                origin_repo.pull(repo_branch)
        else:
            logger.debug('pulling without git_ssh_command_path')
            origin_repo.pull(repo_branch)
    except GitCommandError, e:
        # FIXME: handle better exception
        logger.exception(e)
        raise e


def clone_repo(repo_url, repo_path, repo_branch, repo_name,
               git_ssh_command_path=None):
    logger.debug("CLONING")
    try:
        if git_ssh_command_path:
            logger.debug('pulling with git_ssh_command_path %s' %
                         git_ssh_command_path)
            repo = Repo.clone_from(repo_url, repo_path, branch=repo_branch,
                                   env={'GIT_SSH': git_ssh_command_path})
        else:
            logger.debug('pulling without git_ssh_command_path')
            repo = Repo.clone_from(repo_url, repo_path, branch=repo_branch)
        origin = repo.remotes['origin']
        origin.rename(repo_name)
        return repo, origin
    except GitCommandError, e:
        # FIXME: handle better exception
        logger.exception(e)
        raise e


def create_repo(repo_path, repo_name, repo_url):
    logger.debug("CREATING REPO")
    repo = Repo.init(repo_path)
    origin = repo.create_remote(repo_name, repo_url)
    return repo, origin


def commit_push(repo, repo_author, repo_email, git_ssh_command_path,
                repo_branch):
    logger.debug("COMMITING AND PUSHING")
    repo.index.add('*')
    logger.debug('added files to repo')
    commit_msg = "Crawl completed at " + time.strftime("%Y-%m-%d-%H-%M-%S")
    environ["GIT_AUTHOR_NAME"] = repo_author
    environ["GIT_AUTHOR_EMAIL"] = repo_email
    # TODO: commit only if diff
    committed = repo.index.commit(commit_msg)
    logger.debug('commited policy data')
    logger.debug(committed)
    # FIXME: there could be more than 1 origin
    origin = repo.remotes[0]
    # origin = repo.remotes[repo_name]
    logger.debug('pushing with git_ssh_command_path %s' % git_ssh_command_path)
    with repo.git.custom_environment(GIT_SSH=git_ssh_command_path):
        try:
            origin.push(repo_branch)
        except GitCommandError, e:
            # FIXME: handle better exception
            logger.exception(e)


def create_data_file_path(rule, data_path):
    data_dir_path = join(data_path,
                         rule.get('organization'),
                         rule.get('tool'))
    if not isdir(data_dir_path):
        makedirs(data_dir_path)
    data_file_path = join(data_dir_path, rule.get('policy') + '.txt')
    return data_file_path


def write_ssh_keys(ssh_dir, ssh_priv_key_env, ssh_pub_key_env,
                   ssh_priv_key_path, ssh_pub_key_path):
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


def write_ssh_command(git_ssh_command_path, git_ssh_command):
    if not isfile(git_ssh_command_path):
        with open(git_ssh_command_path, 'w') as f:
            f.write(git_ssh_command)
        chmod(git_ssh_command_path, 0766)
        logger.debug('wroten %s' % git_ssh_command_path)
        logger.debug('with content %s' % git_ssh_command)


def write_ssh_key_server(ssh_pub_key, ssh_pub_key_path):
    if not isfile(ssh_pub_key_path):
        with open(ssh_pub_key_path, 'w') as f:
            f.write(ssh_pub_key)
        logger.debug('wroten %s' % ssh_pub_key_path)
        logger.debug('with content %s' % ssh_pub_key)
