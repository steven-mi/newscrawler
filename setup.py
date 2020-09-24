#!/usr/bin/env python3
import os
from setuptools import setup

# get key package details from py_pkg/__version__.py
about = {}  # type: ignore
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'newscrawler', '__version__.py')) as f:
    exec(f.read(), about)

# load the README file and use it as the long_description for PyPI
with open('README.md', 'r') as f:
    readme = f.read()

# package configuration - for reference see:
# https://setuptools.readthedocs.io/en/latest/setuptools.html#id9
setup(
    name=about['__title__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=['newscrawler'],
    include_package_data=True,
    python_requires=">=3.5.*",
    install_requires=['requests',
                      'beautifulsoup4',
                      'six',
                      'newspaper3k',
                      'feedparser',
                      'pandas',
                      #'news-please',
                      'goose3'],
    license=about['__license__'],
    zip_safe=False,
    # entry_points={
    #    'console_scripts': ['py-package-template=py_pkg.entry_points:main'],
    # },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='newspaper article crawler'
)
