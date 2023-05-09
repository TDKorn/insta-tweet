import os
from pathlib import Path
from setuptools import setup

LONG_DESCRIPTION_SRC = 'README_PyPi.rst'


def read(file):
    with open(os.path.abspath(file), 'r', encoding='utf-8') as f:
        return f.read()


# Parse version
init = Path(__file__).parent.joinpath("InstaTweet", "__init__.py")
for line in init.read_text().split("\n"):
    if line.startswith("__version__ ="):
        break
version = line.split(" = ")[-1].strip('"')


setup(
    name='insta-tweet',
    packages=['InstaTweet'],
    version=version,
    license='MIT',
    description='Automatically Repost Content From Instagram to Twitter',
    long_description=read(LONG_DESCRIPTION_SRC),
    long_description_content_type="text/x-rst; charset=UTF-8",
    author='Adam Korn',
    author_email='hello@dailykitten.net',
    url='https://www.github.com/TDKorn/insta-tweet/',
    download_url=f"https://github.com/TDKorn/insta-tweet/tarball/master/",
    keywords=['instagram', 'twitter', 'api', 'instagram api', 'twitter api', 'repost', 'instagram repost', 'reposter'],
    install_requires=[
        "requests",
        "tweepy",
        "sqlalchemy",
    ],
)
