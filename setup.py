#!/usr/bin/env python3
import sys
import os

from setuptools import setup, find_packages

setup_requires = ['setuptools_scm']
args = set(sys.argv)

is_test = {'pytest', 'test'} & args
is_sphinx = 'build_sphinx' in args

if is_test:
    setup_requires += (
        'pytest-runner~=2.9',
        'pytest~=3.0'
    )

if is_sphinx:
    setup_requires += [
        'sphinx-rtd-theme',
        'sphinxcontrib-asyncio',
        'Sphinx~=1.4.6'
    ]

setup(
    name="aiogithub",
    use_scm_version={
        'write_to': os.path.join('aiogithub', 'version.py')
    },
    packages=find_packages(),
    install_requires=[
        'aiohttp~=1.0',
        'LinkHeader~=0.4',
        'uritemplate~=3.0',
        'python-dateutil~=2.5'
    ],

    include_package_data=True,

    python_requires='~=3.5',
    setup_requires=setup_requires,
    tests_require=['pytest-asyncio~=0.5.0'],

    author="Reupen Shah",
    description="asyncio-based GitHub API client",
    license="BSD",
    keywords="github api client asyncio",
    url="https://github.com/reupen/aiogithub",

    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 2 - Pre-Alpha'
    ]
)
