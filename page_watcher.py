# -*- coding: utf-8 -*-

from git import Repo, InvalidGitRepositoryError, GitCmdObjectDB, \
    GitCommandError, Git
from os import environ, makedirs, chmod, listdir, sep
from os.path import join, isdir, isfile, abspath, dirname, splitext
import sys
from shutil import rmtree
import yaml
import time
import logging

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)


def read_yaml(file_path, exit_on_error=False):
    try:
        with open(file_path) as f:
            yaml_data = yaml.safe_load(f)
        logger.debug('yaml data: ')
        logger.debug(yaml_data)
        return yaml_data
    except IOError, e:
        logger.exception(e)
        logger.debug('cant obtain yaml file')
        if exit_on_error:
            sys.exit()
        raise IOError


def pull_or_clone(repo_path, repo_url, repo_branch,
                  repo_name='origin', git_ssh_command_path=None,
                  exit_on_error=True):
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
                # FIXME: handle in a better way exception
                logger.exception(e)
                logger.debug('cant obtain repo')
                if exit_on_error:
                    sys.exit()
                else:
                    repo, origin = create_repo(repo_path, repo_name, repo_url)
        else:
            pull_repo(origin, repo_branch, git_ssh_command_path)
            # FIXME: pull fail?
        return repo
    try:
        repo, origin = clone_repo(repo_url, repo_path, repo_branch,
                                  repo_name, git_ssh_command_path)
    except GitCommandError, e:
    # FIXME: handle better exception
        logger.exception(e)
        logger.debug('cant obtain repo')
        if exit_on_error:
            sys.exit()
        else:
            repo, origin = create_repo(repo_path, repo_name, repo_url)
    return repo


def filelist(dir_path):
    files = []
    for f in listdir(dir_path):
        fulldir = join(dir_path, f)
        if isdir(fulldir):
            flist = [join(fulldir, x) for x in listdir(fulldir) \
                     if isfile(join(fulldir, x)) and x.endswith('.yml')]
            files.extend(flist)
            files.extend(filelist(fulldir))
    return files


def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z


def obtain_policy_type_from_filename(file_path):
    policy_type = None
    logger.debug('file_path %s' % file_path)
    if file_path.endswith('.yml'):
        policy_type = splitext(file_path.lower())[0]
    logger.debug('policy_type %s' % policy_type)
    return policy_type


def obtain_yaml_from_path(repo_path):
    yaml_list = []
    files_path = filelist(repo_path)
    for file_path in files_path:
        path_list = file_path.split(sep)
        path_dict = {
            'policy': obtain_policy_type_from_filename(path_list[-1]),
            'tool': path_list[-2],
            'organization': path_list[-3]
        }
        yaml_data = read_yaml(file_path)
        if yaml_data:
            yaml_dict = merge_two_dicts(yaml_data, path_dict)
            yaml_list.append(yaml_dict)
    logger.debug(yaml_list)
    return yaml_list


def obtain_yaml(repo_path, repo_url, repo_branch, file_path=None,
                repo_name='origin', git_ssh_command_path=None,
                exit_on_error=True):
    logger.debug('repo_name %s' % repo_name)
    pull_or_clone(repo_path, repo_url, repo_branch,
                  repo_name, git_ssh_command_path,
                  exit_on_error)
    if file_path:
        yaml_data = read_yaml(file_path)
        return yaml_data
    yaml_data = obtain_yaml_from_path(repo_path)
    return yaml_data


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
        logger.debug("COMMITING")
        repo.index.add('*')
        logger.debug('added files to repo')
        commit_msg = "Crawl completed at " + time.strftime("%Y-%m-%d-%H-%M-%S")
        environ["GIT_AUTHOR_NAME"] = repo_author
        environ["GIT_AUTHOR_EMAIL"] = repo_email
        # commit only if something changed
        committed = repo.index.commit(commit_msg)
        logger.debug('commited policy data')
        logger.debug(committed)
        logger.debug('PUSHING')
        # FIXME: there could be more than 1 origin
        origin = repo.remotes[0]
        # origin = repo.remotes[repo_name]
        logger.debug('pushing with git_ssh_command_path %s' %
                     git_ssh_command_path)
        # more debugging for morph.io
        with open(git_ssh_command_path) as f:
            logger.debug('ssh command content %s' % f.read())
        with origin.repo.git.custom_environment(GIT_SSH=git_ssh_command_path):
            environ['GIT_SSH'] = git_ssh_command_path
            logger.debug('GIT_SSH %s' % environ.get('GIT_SSH'))
            logger.debug('GIT_SSH_COMMAND %s' % environ.get('GIT_SSH_COMMAND'))
            try:
                origin.push(repo_branch)
            except GitCommandError, e:
                # FIXME: handle better exception
                logger.exception(e)


def check_ssh_keys(repo, git_ssh_command_path, ssh_priv_key_path,
                   ssh_pub_key_path, ssh_pub_key_path_server):

        with open(ssh_pub_key_path, 'r') as f:
            logger.debug('ssh pub key %s' % f.read())
        with open(ssh_priv_key_path, 'r') as f:
            logger.debug('ssh priv key %s' % f.read())
        with open(ssh_pub_key_path_server, 'r') as f:
            logger.debug('ssh pub key server %s' % f.read())
        origin = repo.remotes[0]
        logger.debug('pushing with git_ssh_command_path %s' %
                     git_ssh_command_path)
        # more debugging for morph.io
        with open(git_ssh_command_path) as f:
            logger.debug('ssh command content %s' % f.read())
        logger.debug('MORPH_SSH_PUB_KEY')
        logger.debug(environ.get('MORPH_SSH_PUB_KEY'))
        logger.debug('MORPH_SSH_PRIV_KEY')
        logger.debug(environ.get('MORPH_SSH_PRIV_KEY'))
        with repo.git.custom_environment(GIT_SSH=git_ssh_command_path):
            logger.debug('GIT_SSH %s' % environ.get('GIT_SSH'))
            logger.debug('GIT_SSH_COMMAND %s' % environ.get('GIT_SSH_COMMAND'))
        with origin.repo.git.custom_environment(GIT_SSH=git_ssh_command_path):
            logger.debug('GIT_SSH %s' % environ.get('GIT_SSH'))
            logger.debug('GIT_SSH_COMMAND %s' % environ.get('GIT_SSH_COMMAND'))
        environ['GIT_SSH'] = git_ssh_command_path
        logger.debug('GIT_SSH %s' % environ.get('GIT_SSH'))



def commit_push_if_changes(repo, repo_author, repo_email, git_ssh_command_path,
                           repo_branch, metadata_path):
    # FIXME: handle changes to be commited
    # if repo.index.diff(repo.head.commit):
    #     logger.debug('there are unpushed changes')
    if repo.index.diff(None) or repo.untracked_files:
        write_metadata_file(metadata_path, repo.working_dir)
        commit_push(repo, repo_author, repo_email, git_ssh_command_path,
                    repo_branch)
    else:
        logger.debug('nothing changed, not committing/pushing')


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


def generate_hash(text):
    import hashlib
    sha = hashlib.sha256(text).hexdigest()
    logger.debug(sha)
    return sha


def obtain_script_version():
    from pkg_resources import get_distribution, DistributionNotFound
    try:
        _dist = get_distribution('page-watcher-scraper')
    except DistributionNotFound:
        __version__ = 'Please install this project with setup.py'
    else:
        __version__ = _dist.version
    logger.debug(__version__)


def obtain_script_commit_hash(script_path):
    # FIXME: ROOT_PATH
    script_repo = Repo(script_path, odbt=GitCmdObjectDB)
    commit_hash = script_repo.head.commit.hexsha
    logger.debug(commit_hash)
    return commit_hash


# def obtain_python_version():
#     import sys
#     python_version = sys.version
#     logger.debug(python_version)


def obtain_uname():
    from os import uname
    kernel_version = ' '.join(uname())
    logger.debug(kernel_version)
    return kernel_version


# def obtain_system_hostname():
#     import socket
#     s = socket.socket()
#     host = socket.gethostname()
#     logger.debug(host)


# def obtain_user():
#     import getpass
#     getpass.getuser()


def obtain_home():
    from os.path import expanduser
    home = expanduser('~')
    logger.debug('home %s' % home)
    return home


def obtain_environ():
    from os import environ
    logger.debug('environ %s' % environ)
    return environ


def ls(dir_path):
    from os import listdir
    ls = listdir(dir_path)
    logger.debug('ls %s' % ls)
    return ls


def generate_host_identifier():
    hostid = generate_hash(obtain_uname())
    logger.debug(hostid)
    return hostid


def obtain_ip():
    import socket
    ip = socket.gethostbyname(socket.gethostname())
    logger.debug('ip %s' % ip)
    return ip


def obtain_public_ip():
    from urllib2 import urlopen
    my_ip = urlopen('http://ip.42.pl/raw').read()
    logger.debug('public ip %s' % my_ip)
    return str(my_ip)


def now():
    from datetime import datetime
    now = datetime.now()
    logger.debug(now)
    return now


def ismorpio():
    if environ['HOME'] == '/app':
        logger.debug('running in morph.io')
        return True
    else:
        logger.debug('not running in morph.io')
        return False


def hasproxy():
    # FIXME: http proxy might not change the public address,
    # assuming it does for now
    if environ.get('HTTP_PROXY'):
        logger.debug('there is an HTTP_PROXY')
        return True
    else:
        logger.debug('there is not an HTTP_PROXY')
        return False


def generate_metadata(repo_path):
    # ADVICE: system information is sensitive
    # in morph.io or running with tor, the ip will change all the time
    # FIXME: in morph.io cant obtain the current git revision this way
    # in morph.io host name will change all the time
    # an env variable that doesnt change is HOME=/app
    if ismorpio():
        ip = obtain_public_ip()
        uname = obtain_uname()
        commit_revision = None
        host = 'morph.io'
    elif hasproxy():
        ip = obtain_public_ip()
        uname = generate_hash(obtain_uname())
        commit_revision = obtain_script_commit_hash(repo_path)
        host = 'local'
    else:
        ip = generate_hash(obtain_public_ip())
        uname = generate_hash(obtain_uname())
        commit_revision = obtain_script_commit_hash(repo_path)
        host = 'dev server'
    metadata = {
        'timestamp': str(now()),
        'ip': ip,
        'uname': uname,
        'commit_revision': commit_revision,
        'host': host
    }
    logger.debug(metadata)
    return metadata


def generate_yaml(dict_data):
    data_yaml = yaml.safe_dump(dict_data)
    logger.debug(data_yaml)
    return data_yaml


# def create_metadata_data_file_path(rule, data_path):
#     data_dir_path = join(data_path,
#                          rule.get('organization'),
#                          rule.get('tool'))
#     if not isdir(data_dir_path):
#         makedirs(data_dir_path)
#     metadata_file_path = join(data_dir_path, rule.get('policy')
#                               + '_metadata.txt')
#     logger.debug('metadata file path %s' % metadata_file_path)
#     return metadata_file_path


def write_metadata_file(metadata_path, repo_path):
    metadata = generate_metadata(repo_path)
    metadata_yaml = generate_yaml(metadata)
    with open(metadata_path, 'w') as f:
        f.write(metadata_yaml)
    logger.debug('wroten %s with %s' % (metadata_path, metadata_yaml))
