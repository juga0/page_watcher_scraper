from setuptools import setup, find_packages
setup(
    name='policies_scrapper',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = policies_scrapper.settings']},
)
