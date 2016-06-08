import ez_setup

ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name="aiogithub",
    version="0.1.dev0",
    packages=find_packages(),
    install_requires=['aiohttp', 'LinkHeader', 'uritemplate',
                      'python-dateutil'],

    include_package_data=True,

    setup_requires=['pytest-runner', 'pytest'],
    tests_require=['pytest-asyncio'],

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
