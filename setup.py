#!/usr/bin/env python3
import sys

from setuptools import setup, find_packages

setup_requires = []
is_test = {'pytest', 'test'} & set(sys.argv)

if is_test:
    setup_requires = [
        'pytest-runner~=2.9',
        'pytest~=3.0'
    ]

setup(
    name="aiogithub",
    version="0.1.dev0",
    packages=find_packages(),
    install_requires=[
        'aiohttp~=1.0',
        'LinkHeader~=0.4',
        'uritemplate~=3.0',
        'python-dateutil~=2.5'
    ],

    include_package_data=True,

    setup_requires=setup_requires,
    tests_require=['pytest-asyncio~=0.5.0'],

    author="Reupen Shah",
    description="asyncio-based GitHub API client",
    license="BSD",
    keywords="github api client asyncio",
    url="https://github.com/reupen/aiogithub",

    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Development Status :: 2 - Pre-Alpha'
    ]
)
