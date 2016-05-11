# -*- coding: utf-8 -*-

# Scrapy settings for page_watcher_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'page_watcher_scraper'

SPIDER_MODULES = ['page_watcher_scraper.spiders']
NEWSPIDER_MODULE = 'page_watcher_scraper.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'page_watcher_scraper (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
#COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'page_watcher_scraper.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'page_watcher_scraper.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'page_watcher_scraper.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'

# custom
########################################################
from os.path import dirname, join, abspath
from datetime import datetime


BASE_PATH = dirname(dirname(abspath(__file__)))
DATA_DIR = 'data'
DATA_PATH = join(BASE_PATH,  DATA_DIR)
LOG_DIR = 'log'
NOW = datetime.utcnow().replace(microsecond=0).isoformat().replace(':', '-')
LOG_FILENAME =  NOW + '_' + BOT_NAME + '.log'
LOG_PATH = join(BASE_PATH,  LOG_DIR)
LOG_FULLPATH = join(LOG_PATH,  LOG_FILENAME)

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0'

COOKIES_ENABLED = False

# with no default HttpProxyMiddleware, the environment variables will be used
# FIXME: check https with proxy
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 500,
#     # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware':  None,
# }

ITEM_PIPELINES = {
    'page_watcher_scraper.pipelines.PageWatcherScraperPipeline': 300,
}

# HTTPCACHE_ENABLED = True # default False
# HTTPCACHE_DIR = DATA_PATH # default 'httpcache'

# ## extra settings

# FIXME: change in production
#LOG_LEVEL = 'ERROR'
#LOG_FORMAT = "%(levelname)s [%(name)s] ( %(filename)s:%(lineno)s, in %(funcName)s) ______ %(message)s"

#LOG_ENABLED = True
# uncomment to log to file
#LOG_FILE = LOG_FULLPATH

COMPRESSION_ENABLED = False # default True
#DOWNLOAD_DELAY = 2 # default 0
#RANDOMIZE_DOWNLOAD_DELAY = True # default True

## custom variables

HTML_DIR = 'html'
HTML_PATH = join(BASE_PATH, HTML_DIR, "%(time)s-%(name)s-%(item)s.html")
LOG_OK_URL_FILENAME = 'ok_url.log'
LOG_FAIL_URL_FILENAME = 'fail_url.log'
LOG_OK_URL_FILENAME = NOW + '_ok_url.log'
LOG_FAIL_URL_FILENAME = NOW + '_fail_url.log'
LOG_OK_URL_FULLPATH = join(LOG_PATH,  LOG_OK_URL_FILENAME)
LOG_FAIL_URL_FULLPATH = join(LOG_PATH,  LOG_FAIL_URL_FILENAME)

POLICY_TYPES = {
    'terms of service': 'tos',
    'privacy policy': 'privacy_policy'
}

# FIXME: move out of settings?
# CONFIG_REPO_BRANCH = 'master'
# RULES_REPO_BRANCH = 'master'
# GIT_AUTHOR_NAME = "OII Policies Robot"
# GIT_AUTHOR_EMAIL = "robots@oii.org"
# # BASE_PATH = dirname(dirname(abspath(__file__)))
ROOT_PATH = dirname(BASE_PATH)
# CONFIG_REPO = 'page-watcher-config'
# RULES_REPO = 'page-watcher-rules'
DATA_REPO = 'page-watcher-data'
# CONFIG_REPO_PATH = join(ROOT_PATH, 'policies_config')
# RULES_REPO_PATH = join(ROOT_PATH, 'policies_rules')
DATA_REPO_PATH = join(ROOT_PATH, DATA_REPO)
# CONFIG_FILENAME = 'config.yml'
# DATA_FILENAME = 'data.yml'
# RULES_FILENAME = 'rules.yml'
# CONFIG_PATH = join(ROOT_PATH, CONFIG_REPO, CONFIG_FILENAME)
# RULES_PATH = join(ROOT_PATH, RULES_REPO, RULES_FILENAME)

try:
    from settings_local import *
except:
    print 'Could not import settings_local'
