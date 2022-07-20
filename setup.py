import os
from setuptools import setup


def get_description():
    file = os.path.abspath('README.md')
    with open(file, 'r', encoding='utf-8') as f:
        long_description = u'{}'.format(f.read())
        return long_description


setup(
    name='insta-tweet',
    packages=['InstaTweet/core'],
    version='1.1.1',  # yea
    license='MIT',
    description='Automatically Repost Content From Instagram to Twitter',
    long_description= get_description(),
    long_description_content_type='text/markdown',
    author='Adam Korn',
    author_email='hello@dailykitten.net',
    url='https://www.github.com/TDKorn/insta-tweet',
    download_url="https://github.com/TDKorn/insta-tweet/tarball/master",
    keywords=['instagram', 'twitter', 'repost', 'reposter', 'instascrape', 'instagram-repost'],
    install_requires=[
        'beautifulsoup4>=4.11.1',
        'moviepy>=1.0.3',
        'Pillow>=9.2.0',
        'requests>=2.28.1',
        'requests_oauthlib>=1.3.0',
        'tqdm>=4.62.3'
    ]
)
