#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


def get_version(filename):
    content = open(filename).read()
    metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", content))
    return metadata['version']

requires = [
    'pyramid',
    'pyramid_jinja2',
    'pyramid_debugtoolbar',
    'waitress',
    'sqlalchemy',
    'celery',
    'zope.sqlalchemy',
    'mock',
    'nose'
]

setup(name='yodl',
      version=get_version('yodl/__init__.py'),
      description='yodl',
      long_description=readme + '\n\n' + history,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      keywords='web pyramid pylons',
      packages=find_packages(exclude=['supervisor', 'tests', 'tests.*']),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite='nose.collector',
      entry_points={
          b'paste.app_factory': [
              'main = yodl:main',
          ],
      },
      )
