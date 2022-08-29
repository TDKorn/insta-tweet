import os
from setuptools import setup


LONG_DESCRIPTION_SRC = 'README.rst'


def read(file):
    with open(os.path.abspath(file), 'r', encoding='utf-8') as f:
        return f.read()


setup(
    name='insta-tweet',
    packages=['InstaTweet'],
    version='2.0.0b13',
    license='MIT',
    description='Automatically Repost Content From Instagram to Twitter',
    long_description=read(LONG_DESCRIPTION_SRC),
    long_description_content_type="text/x-rst; charset=UTF-8",
    author='Adam Korn',
    author_email='hello@dailykitten.net',
    url='https://www.github.com/TDKorn/insta-tweet/',
    download_url="https://github.com/TDKorn/insta-tweet/tarball/2.0.0/",
    keywords=['instagram', 'twitter', 'repost', 'reposter', 'instascrape', 'instagram-repost'],
    install_requires=[
        "requests",
        "tweepy",
        "psycopg2",
        "sqlalchemy",
    ],
)
