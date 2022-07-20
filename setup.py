import os
from setuptools import setup


def get_description():
    file = os.path.abspath('README.md')
    with open(file, 'r', encoding='utf-8') as f:
        long_description = u'{}'.format(f.read())
        return long_description


setup(
    name='insta-tweet',
    packages=['InstaTweet'],
    version='2.0.0b0',
    license='MIT',
    description='Automatically Repost Content From Instagram to Twitter',
    long_description=get_description(),
    long_description_content_type='text/markdown',
    author='Adam Korn',
    author_email='hello@dailykitten.net',
    url='https://www.github.com/TDKorn/insta-tweet/',
    download_url="https://github.com/TDKorn/insta-tweet/tarball/2.0.0-beta/",
    keywords=['instagram', 'twitter', 'repost', 'reposter', 'instascrape', 'instagram-repost'],
    install_requires=["requests", "tweepy", "psycopg2", "sqlalchemy"],
)
