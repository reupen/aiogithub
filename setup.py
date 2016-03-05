from setuptools import setup, find_packages

setup(
    name="aiogithub",
    version="0.1dev0",
    packages=find_packages(),
    install_requires=['aiohttp', 'LinkHeader', 'uritemplate'],

    package_data={
        '': ['*.txt', '*.rst', '*.md']
    },

    author="Reupen Shah",
    description="asyncio-based GitHub API client",
    license="BSD",
    keywords="github api client asyncio",
    url="https://reupen.github.io/aiogithub"
)
