#!/usr/bin/env python

from setuptools import setup, find_packages
from snappy_util import __author__, __version__, __license__

setup(name='snappy_util',
      version=__version__,
      description='decoder for snappy-java',
      author=__author__,
      license=__license__,
      author_email='author@fukuda.org',
      url='http://twitter.com/masahif2',
      packages = find_packages(),
      install_requires = ['snappy'],
      
)

