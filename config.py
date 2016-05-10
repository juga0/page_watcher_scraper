from os.path import dirname, abspath, join

CONFIG_REPO_BRANCH = 'master'
RULES_REPO_BRANCH = 'master'
DATA_REPO_BRANCH = 'master'
GIT_AUTHOR_NAME = "OII Policies Agent"
GIT_AUTHOR_EMAIL = "oii-agents@iilab.org"

# BASE_PATH = dirname(dirname(abspath(__file__)))
BASE_PATH = dirname(abspath(__file__))
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
