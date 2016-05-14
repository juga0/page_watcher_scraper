from os.path import dirname, abspath, join

CONFIG_REPO_BRANCH = 'master'
RULES_REPO_BRANCH = 'master'
DATA_REPO_BRANCH = 'master'
GIT_AUTHOR_NAME = "OII Policies Agent"
GIT_AUTHOR_EMAIL = "oii-agents@iilab.org"

# BASE_PATH = dirname(dirname(abspath(__file__)))
# BASE_PATH = dirname(abspath(__file__))
# to be able to run it in morph.io, directories can only be created inside the
# code dir
BASE_PATH = abspath(__file__)
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
CONFIG_REPO_URL = \
    'https://code.iilab.org/openintegrity-agents/page-watcher-config.git'
# CONFIG_REPO_URL = 'https://github.com/juga0/page-watcher-config'
RULES_REPO_URL = \
    'https://code.iilab.org/openintegrity-agents/page-watcher-rules.git'


MORPH_SSH_PRIV_KEY_ENV = 'MORPH_SSH_PRIV_KEY'
MORPH_SSH_PUB_KEY_ENV = 'MORPH_SSH_PUB_KEY'
SSH_DIR = 'ssh'
SSH_PATH = join(ROOT_PATH, SSH_DIR)
SSH_PRIV_KEY_PATH = join(SSH_PATH, 'id_rsa')
SSH_PUB_KEY_PATH = join(SSH_PATH, 'id_rsa.pub')
GIT_SSH_COMMAND = '#!/bin/sh\nssh -i ' + SSH_PRIV_KEY_PATH
GIT_SSH_COMMAND_FILE = 'ssh_command.sh'
GIT_SSH_COMMAND_PATH = join(ROOT_PATH, GIT_SSH_COMMAND_FILE)

try:
    from config_local import *
except:
    print 'Could not import config_local'
