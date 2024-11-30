''' setup.py
'''
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='keibascraper',
    version='2.0.0',
    author='new-village',
    url='https://github.com/new-village/KeibaScraper',
    description='keibascraper is a simple scraping library for netkeiba.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['requests', 'beautifulsoup4', 'jq'],
    packages=find_packages(),
    package_data={'': ['config/*.json']},
)
