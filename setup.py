import os
import re
from setuptools import setup


LONG_DESCRIPTION_SRC = 'README.rst'


def read(file):
    with open(os.path.abspath(file), 'r', encoding='utf-8') as f:
        return f.read()


def get_pypi_desc(rst_file=LONG_DESCRIPTION_SRC):
    rst = read(rst_file)
    # Replace the "From the Docs..." rst admonition with a screenshot of it
    docs_admonition_regex = r'.. admonition:: From the Docs\.\.\.[\w\W]+https.+\n{3}'
    docs_admonition_img = ".. image:: {}".format(
        "https://user-images.githubusercontent.com/96394652/187158617-f45761ab-3aa9-472f-a6fb-a99cd0ce900c.png\n\n\n"
    )
    return re.sub(
        pattern=docs_admonition_regex,
        repl=docs_admonition_img,
        string=rst
    )


setup(
    name='insta-tweet',
    packages=['InstaTweet'],
    version='2.0.0b36',
    license='MIT',
    description='Automatically Repost Content From Instagram to Twitter',
    long_description=get_pypi_desc(LONG_DESCRIPTION_SRC),
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
