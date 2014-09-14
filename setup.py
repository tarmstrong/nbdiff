#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='nbdiff',
    version='1.0.4',
    description='A tool for diffing and merging IPython Notebook files',
    long_description=readme + '\n\n' + history,
    author='Tavish Armstrong',
    author_email='tavisharmstrong@gmail.com',
    url='https://github.com/tarmstrong/nbdiff',
    packages=[
        'nbdiff',
        'nbdiff.server',
        'nbdiff.server.command',
        'nbdiff.server.database',
        'nbdiff.adapter',
    ],
    package_data={
        'nbdiff.server': [
            'templates/*',
            'static/libraries/*',
            'static/image/*',
            'static/js/*',
            'static/css/*',
        ],
    },
    package_dir={'nbdiff': 'nbdiff'},
    entry_points={'console_scripts': [
        'nbdiff = nbdiff.commands:diff',
        'nbmerge = nbdiff.commands:merge',
    ]},
    include_package_data=True,
    install_requires=[
        'flask',
        'jinja2',
        'ipython',
        'python-Levenshtein',
	'python-hglib',
    ],
    license="MIT",
    zip_safe=False,
    keywords='nbdiff',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)
