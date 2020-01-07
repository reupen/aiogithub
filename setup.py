#!/usr/bin/env python3
import sys
import os

from setuptools import setup, find_packages

setup_requires = ['setuptools_scm']
args = frozenset(sys.argv)

is_test = {'pytest', 'test'} & args
is_sphinx = 'build_sphinx' in args
is_flake8 = 'flake8' in args

if is_test:
    setup_requires += (
        'pytest-runner~=2.9',
        'pytest~=3.0'
    )

if is_sphinx:
    setup_requires += (
        'sphinx-rtd-theme',
        'sphinxcontrib-asyncio',
        'Sphinx~=1.4'
    )

if is_flake8:
    setup_requires += (
        'flake8~=3.7',
    )

setup(
    name="aiogithub",
    use_scm_version={
        'write_to': os.path.join('aiogithub', 'version.py')
    },
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'aiohttp~=3.0',
        'async-timeout~=3.0',
        'LinkHeader~=0.4',
        'uritemplate~=3.0',
        'python-dateutil~=2.5'
    ],

    include_package_data=True,

    python_requires='~=3.5',
    setup_requires=setup_requires,
    tests_require=['pytest-asyncio~=0.10.0'],

    author="Reupen Shah",
    description="asyncio-based GitHub API client",
    license="BSD",
    keywords="github api client asyncio",
    url="https://github.com/reupen/aiogithub",

    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Development Status :: 2 - Pre-Alpha'
    ]
)
