#!/usr/bin/env python

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
doclink = """
Documentation
-------------

The full documentation is at http://pysensu.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='pysensu-ng',
    version='0.11.0',
    description='This is a client to interact with the Sensu API',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Angel Velasquez',
    author_email='avelasquez@sangoma.com',
    url='https://github.com/sangoma/pysensu',
    packages=[
        'pysensu',
    ],
    package_dir={'pysensu': 'pysensu'},
    include_package_data=True,
    install_requires=[
        'requests',
    ],
    license='MIT',
    zip_safe=False,
    keywords='pysensu',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
