from setuptools import setup, find_packages
setup(
    name='page_watcher_scraper',
    version='1.3',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = page_watcher_scraper.settings']},
)
